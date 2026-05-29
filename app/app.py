import os
import io
import math
import joblib
import pickle
import numpy as np
import pandas as pd
import warnings

from flask import Blueprint, render_template, request, jsonify

bp = Blueprint("main", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
APP_MODELS_DIR = os.path.join(BASE_DIR, "app", "models")

warnings.filterwarnings("ignore")

loan_model    = None
fraud_model   = None
loan_scaler   = None
_loan_load_error  = None
_fraud_load_error = None


def _load_models():
    global loan_model, fraud_model, loan_scaler
    global _loan_load_error, _fraud_load_error

    # ── Loan model ──
    loan_paths = [
        os.path.join(MODELS_DIR, "loan_approval_model.pkl"),
        os.path.join(APP_MODELS_DIR, "loan_approval_model.pkl"),
    ]
    for lp in loan_paths:
        if os.path.exists(lp):
            try:
                with open(lp, "rb") as f:
                    loan_model = joblib.load(f)
                break
            except Exception as e:
                _loan_load_error = str(e)
    if loan_model is None:
        _loan_load_error = _loan_load_error or (
            "Model file not found. Checked: " + ", ".join(loan_paths)
        )

    # ── Loan scaler ──
    scaler_paths = [
        os.path.join(MODELS_DIR, "loan_scaler.pkl"),
        os.path.join(APP_MODELS_DIR, "loan_scaler.pkl"),
    ]
    for sp in scaler_paths:
        if os.path.exists(sp):
            try:
                with open(sp, "rb") as f:
                    loan_scaler = pickle.load(f)
                break
            except Exception as e:
                pass

    #  Fraud model (Pipeline — scaler inside) 
    fraud_paths = [
        os.path.join(MODELS_DIR, "fraud_model.pkl"),
        os.path.join(APP_MODELS_DIR, "fraud_model.pkl"),
    ]
    for fp in fraud_paths:
        if os.path.exists(fp):
            try:
                with open(fp, "rb") as f:
                    fraud_model = joblib.load(f)
                break
            except Exception as e:
                _fraud_load_error = str(e)
    if fraud_model is None:
        _fraud_load_error = _fraud_load_error or (
            "Model file not found. Checked: " + ", ".join(fraud_paths)
        )


_load_models()

# Fraud helpers 

BATCH_REQUIRED_COLS = ["step", "type", "amount", "oldbalanceOrg",
                       "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    amount = df["amount"].astype(float)
    df["amount_log"]      = np.log1p(amount.clip(lower=0))
    df["balanceDropOrig"] = df["oldbalanceOrg"].astype(float) - df["newbalanceOrig"].astype(float)
    df["balanceGainDest"] = df["newbalanceDest"].astype(float) - df["oldbalanceDest"].astype(float)
    df["origBalanceZero"] = (df["newbalanceOrig"].astype(float) == 0).astype(int)
    df["isHighRiskType"]  = df["type"].isin(["CASH_OUT", "TRANSFER"]).astype(int)
    return df


def _predict_fraud_df(df: pd.DataFrame):
    # Fraud pipeline has scaler + encoder inside → feed raw engineered features
    preds      = fraud_model.predict(df)
    probas     = fraud_model.predict_proba(df)
    fraud_probs = [round(float(p[1]) * 100, 4) for p in probas]
    return [bool(int(p)) for p in preds], fraud_probs


def _predict_single(step, tx_type, amount,
                    old_orig, new_orig, old_dest, new_dest):
    amount_log   = math.log1p(amount) if amount >= 0 else 0.0
    balance_drop = old_orig - new_orig
    balance_gain = new_dest - old_dest
    orig_zero    = 1 if new_orig == 0 else 0
    high_risk    = 1 if tx_type in ("CASH_OUT", "TRANSFER") else 0

    df = pd.DataFrame(
        [[step, tx_type, amount,
          old_orig, new_orig, old_dest, new_dest,
          amount_log, balance_drop, balance_gain,
          orig_zero, high_risk]],
        columns=BATCH_REQUIRED_COLS + [
            "amount_log", "balanceDropOrig", "balanceGainDest",
            "origBalanceZero", "isHighRiskType"],
    )
    preds, fraud_probs = _predict_fraud_df(df)
    row = {
        "step": step, "tx_type": tx_type, "amount": amount,
        "amount_log":      round(amount_log, 4),
        "oldbalanceOrg":   old_orig, "newbalanceOrig": new_orig,
        "oldbalanceDest":  old_dest, "newbalanceDest": new_dest,
        "balanceDropOrig": round(balance_drop, 2),
        "balanceGainDest": round(balance_gain, 2),
        "origBalanceZero": orig_zero,
        "isHighRiskType":  high_risk,
        "fraud_prob":      fraud_probs[0],
    }
    return preds[0], fraud_probs[0], row


#Routes 

@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/loan", methods=["GET", "POST"])
def loan():
    result    = None
    error     = None
    form_data = {}

    if request.method == "POST":
        try:
            form_data = {
                "income":         request.form.get("income", ""),
                "credit_score":   request.form.get("credit_score", ""),
                "loan_amount":    request.form.get("loan_amount", ""),
                "years_employed": request.form.get("years_employed", ""),
            }
            income       = float(form_data["income"])
            credit_score = float(form_data["credit_score"])
            loan_amount  = float(form_data["loan_amount"])
            years        = float(form_data["years_employed"])

            if loan_model is None:
                raise RuntimeError(_loan_load_error or "Loan model not loaded.")

            loan_income_ratio = loan_amount / income if income else 0.0

            # Scale features before predicting
            features_raw = np.array(
                [[income, credit_score, loan_amount,
                  years, loan_income_ratio]]
            )

            if loan_scaler is not None:
                features = loan_scaler.transform(features_raw)
            else:
                # Fallback if scaler missing
                features = features_raw

            pred_class = loan_model.predict(features)[0]
            pred_proba = loan_model.predict_proba(features)[0]

            result = {
                "approved":       bool(pred_class),
                "confidence":     round(float(max(pred_proba)) * 100, 2),
                "approval_prob":  round(float(pred_proba[1]) * 100, 2),
                "rejection_prob": round(float(pred_proba[0]) * 100, 2),
                "income":         income,
                "credit_score":   credit_score,
                "loan_amount":    loan_amount,
                "years_employed": years,
                "ratio":          round(loan_income_ratio, 4),
            }

        except Exception as exc:
            error = str(exc)

    return render_template(
        "loan_approval.html",
        result=result, error=error, form_data=form_data,
    )


@bp.route("/fraud", methods=["GET", "POST"])
def fraud():
    result       = None
    error        = None
    batch_result = None
    batch_error  = None
    form_data    = {}

    if request.method == "POST":
        try:
            form_data = {
                "step":           request.form.get("step", ""),
                "tx_type":        request.form.get("tx_type", ""),
                "amount":         request.form.get("amount", ""),
                "oldbalanceOrg":  request.form.get("oldbalanceOrg", ""),
                "newbalanceOrig": request.form.get("newbalanceOrig", ""),
                "oldbalanceDest": request.form.get("oldbalanceDest", ""),
                "newbalanceDest": request.form.get("newbalanceDest", ""),
            }
            step             = float(form_data["step"])
            tx_type          = form_data["tx_type"]
            amount           = float(form_data["amount"])
            old_balance_orig = float(form_data["oldbalanceOrg"])
            new_balance_orig = float(form_data["newbalanceOrig"])
            old_balance_dest = float(form_data["oldbalanceDest"])
            new_balance_dest = float(form_data["newbalanceDest"])

            if fraud_model is None:
                raise RuntimeError(_fraud_load_error or "Fraud model not loaded.")

            is_fraud, fraud_prob, row = _predict_single(
                step, tx_type, amount,
                old_balance_orig, new_balance_orig,
                old_balance_dest, new_balance_dest,
            )
            legit_prob = round(100.0 - fraud_prob, 4)
            confidence = round(max(fraud_prob, 100.0 - fraud_prob), 2)

            result = {
                "is_fraud":    is_fraud,
                "fraud_prob":  fraud_prob,
                "legit_prob":  legit_prob,
                "confidence":  confidence,
                "step":        step,
                "tx_type":     tx_type,
                "amount":      amount,
                "amount_log":  row["amount_log"],
                "balance_drop": row["balanceDropOrig"],
                "balance_gain": row["balanceGainDest"],
                "orig_zero":   row["origBalanceZero"],
                "high_risk":   row["isHighRiskType"],
            }

        except Exception as exc:
            error = str(exc)

    return render_template(
        "fraud_detection.html",
        result=result, error=error, form_data=form_data,
        batch_result=batch_result, batch_error=batch_error,
    )


#Batch Fraud Detection 

@bp.route("/fraud/batch", methods=["POST"])
def fraud_batch():
    batch_result = None
    batch_error  = None

    if fraud_model is None:
        batch_error = _fraud_load_error or "Fraud model not loaded."
        return render_template("fraud_detection.html",
                               result=None, error=None, form_data={},
                               batch_result=batch_result,
                               batch_error=batch_error)

    uploaded = request.files.get("csv_file")

    if not uploaded or uploaded.filename == "":
        batch_error = "No file selected. Please upload a CSV file."
        return render_template("fraud_detection.html",
                               result=None, error=None, form_data={},
                               batch_result=batch_result,
                               batch_error=batch_error)

    if not uploaded.filename.lower().endswith(".csv"):
        batch_error = "Only .csv files are accepted."
        return render_template("fraud_detection.html",
                               result=None, error=None, form_data={},
                               batch_result=batch_result,
                               batch_error=batch_error)

    try:
        raw   = uploaded.read()
        df_in = pd.read_csv(io.BytesIO(raw))

        missing = [c for c in BATCH_REQUIRED_COLS if c not in df_in.columns]
        if missing:
            batch_error = (
                "CSV missing column(s): " + ", ".join(missing) +
                ". Required: " + ", ".join(BATCH_REQUIRED_COLS)
            )
            return render_template("fraud_detection.html",
                                   result=None, error=None, form_data={},
                                   batch_result=batch_result,
                                   batch_error=batch_error)

        df = df_in[BATCH_REQUIRED_COLS].copy()
        for col in BATCH_REQUIRED_COLS:
            if col != "type":
                df[col] = pd.to_numeric(df[col], errors="coerce")

        bad_rows = df[df.isnull().any(axis=1)]
        if len(bad_rows):
            batch_error = (
                f"{len(bad_rows)} row(s) skipped due to invalid values. "
                f"{len(df) - len(bad_rows)} transactions processed."
            )

        df = df.dropna().reset_index(drop=True)
        if df.empty:
            batch_error = "No valid rows remain after validation."
            return render_template("fraud_detection.html",
                                   result=None, error=None, form_data={},
                                   batch_result=batch_result,
                                   batch_error=batch_error)

        # ✅ Fraud pipeline handles scaling internally
        df = _engineer_features(df)
        preds, fraud_probs = _predict_fraud_df(df)

        rows_out = []
        for i, (is_fraud, fp) in enumerate(zip(preds, fraud_probs)):
            rows_out.append({
                "row":       i + 1,
                "step":      int(df.at[i, "step"]),
                "type":      str(df.at[i, "type"]),
                "amount":    float(df.at[i, "amount"]),
                "oldOrig":   float(df.at[i, "oldbalanceOrg"]),
                "newOrig":   float(df.at[i, "newbalanceOrig"]),
                "oldDest":   float(df.at[i, "oldbalanceDest"]),
                "newDest":   float(df.at[i, "newbalanceDest"]),
                "fraud_pct": fp,
                "is_fraud":  is_fraud,
            })

        total     = len(rows_out)
        fraud_cnt = sum(1 for r in rows_out if r["is_fraud"])
        legit_cnt = total - fraud_cnt
        fraud_pct = round(fraud_cnt / total * 100, 2) if total else 0

        batch_result = {
            "total":     total,
            "fraud":     fraud_cnt,
            "legit":     legit_cnt,
            "fraud_pct": fraud_pct,
            "rows":      rows_out,
            "filename":  uploaded.filename,
        }

    except Exception as exc:
        batch_error = f"Failed to process file: {exc}"

    return render_template("fraud_detection.html",
                           result=None, error=None, form_data={},
                           batch_result=batch_result,
                           batch_error=batch_error)