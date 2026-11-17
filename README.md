# 🛡️ Adversarial Metascience Auditor

An automated AI-powered audit engine that moves beyond polite summarization to aggressively hunt for logical gaps, hand-wavy assumptions, and methodological weaknesses in scientific papers—explaining why papers actually face peer-review rejection.

---

## ⚡ The Solution
**Adversarial Auditor:** Acts as a hyper-pedantic, cynical senior reviewer. It forces the extraction of granular claims, aggressively flagging speculative hypotheses, missing statistical evidence, and design intuitions disguised as empirical facts.

---

## 📊 Benchmark Results (Tested Suite)

The audit engine accurately separates foundational engineering rigor from vulnerable or rejected preprints:

| Paper | Rigor Score | Claim Breakdown (Total) | Key Audit Signal |
| :--- | :---: | :---: | :--- |
| **Attention Is All You Need** *(Vaswani et al.)* | **8 / 10** | 8 Strong, 3 Ambiguous, 1 Unsupported *(12)* | High empirical baseline; correctly flags untested architectural hypotheses (e.g., sinusoidal length extrapolation). |
| **A Simple Training-Free Rejection Option** | **6 / 10** | 5 Strong, 1 External, 4 Ambiguous *(10)* | Moderate rigor; strong core metrics undercut by frequent logical ambiguities. |
| **Learning Deliberately, Acting Intuitively** | **5 / 10** | 7 Strong, 4 Ambiguous, 1 Unsupported *(12)* | Mixed rigor; heavy reliance on overgeneralized or unverified claims. |
| **Mechanistic Interpretability of ICL** | **5 / 10** | 5 Strong, 3 Ambiguous, 2 Unsupported *(10)* | Mixed rigor; half of extracted claims lack direct internal proof or rely on speculative leaps. |

---

## 🛠️ Tech Stack & Architecture

* **Python** (Core Pipeline)
* **PyMuPDF (`pymupdf`)** (Robust PDF text extraction)
* **OpenAI Client & Berget AI Gateway** (Powered by `google/gemma-4-31B-it`)
* **FPDF2 (`fpdf2`)** (Automated clean PDF audit report generation)

---
