# Claims Intelligence Platform — Static Demo

**Capgemini × Azure AI Foundry | Insurance Claims Processing Demo**

A fully static, hard-coded demonstration of an intelligent multi-agent claims processing system built with **FastAPI** and vanilla JavaScript. No Azure credentials required — all data is pre-populated.

---

## What It Demonstrates

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent Pipeline** | 5-step AI pipeline: Document Intake → OCR (Mistral) → JSON Structuring (GPT-4.1-mini) → Policy Matching (Azure AI Search) → Coverage Validation |
| 📊 **Claims Dashboard** | KPI cards, approval rates, before/after AI comparison |
| 📁 **Claims Management** | All 5 sample claims with filtering and drill-down |
| 🔴 **Live Pipeline Demo** | Animated step-by-step pipeline simulation with real output |
| 📄 **Policy Library** | 5 insurance policies with full coverage details |
| 🏗️ **Architecture View** | System design, Azure services used, and business benefits |

---

## Quick Start

```bash
cd demo-app
pip install -r requirements.txt
python main.py
```

Then open **http://localhost:8080** in your browser.

---

## Sample Claims

| Claim | Claimant | Policy | Decision |
|-------|----------|--------|----------|
| CLM-2025-52814 | John Peterson | LIAB-AUTO-001 | ❌ DENIED |
| CLM-2025-13982 | Samantha Turner | COMM-AUTO-001 | ✅ APPROVED |
| CLM-2025-44278 | Michael Rodriguez | LIAB-AUTO-001 | ❌ DENIED |
| CLM-2025-22097 | Andrea M. Bennett | COMM-AUTO-001 | ✅ APPROVED |
| CLM-2025-33109 | Christopher J. Ryan | COMM-AUTO-001 | ✅ APPROVED |

> **Key insight:** Claims 1 & 3 use a *Liability Only* policy which explicitly does NOT cover own-vehicle damage — the AI agents correctly detect and deny these.

---

## Architecture

```
Image Upload → OCR Agent (Mistral AI) → JSON Structuring (GPT-4.1-mini)
           → Policy Matching (Azure AI Search) → Coverage Validation (GPT-4.1-mini)
           → APPROVED / DENIED Decision Report
```

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JS + Bootstrap 5
- **Branding**: Capgemini

## Project Structure

```
demo-app/
├── main.py            # FastAPI app with all hardcoded data
├── requirements.txt
├── README.md
└── static/
    └── index.html     # Complete single-page application
```
