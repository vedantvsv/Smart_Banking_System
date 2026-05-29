/* =========================================================
   SMART Banking System — JavaScript
   Handles: form animations, button states, result scroll,
            loan-income-ratio live hint, smooth interactions,
            CSV batch-upload drag-and-drop zone
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* ── Active nav highlighting ───────────────────────── */
    const currentPath = window.location.pathname;
    document.querySelectorAll(".nav-link").forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });

    /* ── Loan form: live ratio hint ─────────────────────── */
    const loanForm = document.getElementById("loanForm");
    if (loanForm) {
        const incomeInput    = document.getElementById("income");
        const loanInput      = document.getElementById("loan_amount");

        function updateRatioHint() {
            const income   = parseFloat(incomeInput?.value);
            const loanAmt  = parseFloat(loanInput?.value);
            if (income > 0 && loanAmt > 0) {
                const ratio = (loanAmt / income * 100).toFixed(2);
                const hint = document.querySelector(".ratio-hint-live");
                if (hint) { hint.textContent = `Loan / Income = ${ratio}%`; }
            }
        }
        if (incomeInput) incomeInput.addEventListener("input", updateRatioHint);
        if (loanInput)   loanInput.addEventListener("input", updateRatioHint);
    }

    /* ── Fraud form: balance sanity hint ───────────────── */
    const fraudForm = document.getElementById("fraudForm");
    if (fraudForm) {
        const oldOrg  = document.getElementById("oldbalanceOrg");
        const newOrig = document.getElementById("newbalanceOrig");

        function checkBalances() {
            const oldB = parseFloat(oldOrg?.value  ?? 0);
            const newB = parseFloat(newOrig?.value ?? 0);
            if (!isNaN(oldB) && !isNaN(newB) && oldB < newB) {
                newOrig.style.borderColor = "var(--warn)";
            } else {
                newOrig.style.borderColor = "";
            }
        }
        oldOrg?.addEventListener("input",  checkBalances);
        newOrig?.addEventListener("input", checkBalances);
    }

    /* ── CSV Upload: drag-and-drop + file name ───────────── */
    const uploadZone   = document.getElementById("uploadZone");
    const csvFileInput = document.getElementById("csvFile");
    const fileNameBadge = document.getElementById("fileNameBadge");

    if (uploadZone && csvFileInput) {
        function setFileName(file) {
            if (!file) { fileNameBadge.classList.remove("visible"); return; }
            fileNameBadge.textContent = "Selected: " + file.name
                + "  (" + (file.size / 1024).toFixed(1) + " KB)";
            fileNameBadge.classList.add("visible");
        }

        csvFileInput.addEventListener("change", () => setFileName(csvFileInput.files[0]));

        uploadZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            uploadZone.classList.add("dragover");
        });
        uploadZone.addEventListener("dragleave", () => {
            uploadZone.classList.remove("dragover");
        });
        uploadZone.addEventListener("drop", (e) => {
            e.preventDefault();
            uploadZone.classList.remove("dragover");
            const file = e.dataTransfer.files[0];
            if (file) {
                csvFileInput.files = e.dataTransfer.files; // HTML5 DataTransferFileList
                setFileName(file);
            }
        });
    }

    /* ── Submit button: disable while submitting ────────── */
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function () {
            const btn = this.querySelector('button[type="submit"]');
            if (!btn) return;
            btn.dataset.original = btn.textContent;   // save label
            btn.disabled = true;
            btn.textContent = "⏳ Processing…";
            setTimeout(() => {
                btn.disabled = false;
                btn.textContent = btn.dataset.original || btn.textContent;
            }, 12000);
        });
    });

    /* ── Smooth scroll to results ───────────────────────── */
    const scrollToResult = () => {
        const el = document.getElementById("resultSection")
                || document.getElementById("fraudResult")
                || document.getElementById("batchResultSection");
        if (el) {
            setTimeout(() => {
                el.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 200);
        }
    };

    if (document.getElementById("resultSection")
            || document.getElementById("fraudResult")
            || document.getElementById("batchResultSection")) {
        scrollToResult();
    }

    /* ── Fade in cards on view ──────────────────────────── */
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            entries => {
                entries.forEach(e => {
                    if (e.isIntersecting) {
                        e.target.classList.add("in-view");
                        observer.unobserve(e.target);
                    }
                });
            },
            { threshold: 0.12 }
        );
        document.querySelectorAll(
            ".feature-card, .metric, .result-card, .summary-card, .results-table"
        ).forEach(el => observer.observe(el));
    }
});
