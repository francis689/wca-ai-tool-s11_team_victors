# 🇰🇪 RUPSA SACCO AI Assistant (Season 11 Tool Build)

An intelligent, two-stage sequential AI application that helps members and prospective members access accurate RUPSA SACCO information through an interactive visual Streamlit web user interface.

This tool is explicitly built to comply with the Season 11 multi-stage connected API call project framework guidelines.

---

## 🏗️ Core Architecture & Connected Pipeline Flow
The application utilizes a strict, sequential **Two-Stage Connected API Workflow**:
1. **Stage 1: Intent Extraction & JSON Structural Processing** (`src/stage1_analysis.py`)  
   Takes raw user text questions and extracts core variables (category, amounts, status, urgency) into a strict, validated structural JSON layout. It features a resilient failover matrix to bounce calls from OpenAI to Google Gemini automatically upon credit depletion.
2. **Stage 2: Context Grounding & Actionable Response Mapping** (`src/stage2_plan.py`)  
   Consumes the parsed JSON variables, dynamically fetches matching local knowledge data structures (`knowledge/loans.txt`, etc.), and uses a second AI model call to construct a beautifully structured Markdown advisory roadmap for the SACCO member.

---

## 🌟 Key Application Features & Rubric Compliance
- **Two Connected API Calls:** Seamlessly passes parsed structural context downstream between sequential model steps.
- **R-T-C-C-O Prompt Framework:** Both Stage 1 and Stage 2 prompts strictly enforce distinct Roles, Tasks, Contexts, Constraints, and Output blueprint variables.
- **Dual-Engine Failover Resilience:** Automatically handles quota limits by falling back dynamically from OpenAI (`gpt-4o-mini`) to Google Gemini (`gemini-3.6-flash`).
- **Interactive Web App UI:** Completely migrated from terminal inputs to a clean visual dashboard powered by **Streamlit**.
- **Secure Key Engineering:** Strict environmental management utilizing `.env` variable ingestion, safely sandboxed from the cloud by our `.gitignore` configuration.

---

## 📂 Project Directory Map
```text
.
├── knowledge/          # Official RUPSA policy, savings, and loan guidelines
├── data/               # Vector data layouts and storage models
├── outputs/            # Automated historical interaction footprint trace logs
├── src/                # Modular core code scripts directory
│   ├── stage1_analysis.py  # Stage 1 Analytics & Failover Engine (Wilfred)
│   ├── stage2_plan.py      # Stage 2 Grounding & Prompt Strategy (Sarah)
│   └── utils.py            # Data Parser Bridge & Exception Handlers (Nderitu)
├── app.py              # Visual Streamlit Interface Entry Module (Jeff & Francis)
├── .env.example        # Reference environment schema template
├── .gitignore          # Cloud tracking exclusion definitions mapping
└── README.md           # Software capability engineering brief documentation
```

---

## 🚀 Getting Started & Execution

### 1. Repository Setup
```bash
git clone <repository-url>
python -m venv venv
```

### 2. Environment Activation & Dependencies
**Windows Users:**
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```
**Linux / macOS Users:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 3. API Credentials
Create a `.env` file in the root folder using the template and fill out your live credentials:
```text
OPENAI_API_KEY=sk-proj-your_key_here
GEMINI_API_KEY=AQ.AB8RN_your_key_here
```

### 4. Launching the Interface Visual Web App Server
Launch the application panel interface inside your local web browser instance:
```bash
streamlit run app.py
```

---

## 🧑‍💻 Team Roles & Responsibilities (Team Victors)
- **Francis (Project Lead):** Core architecture orchestration & local knowledge schema setup.
- **Wilfred (Stage 1 Developer):** Input parameter variable analytics, R-T-C-C-O framework, & dual-engine fallback scripts.
- **Sarah (Stage 2 Developer):** Actionable report generation prompting & Markdown rule maps.
- **Jeff (UI Developer):** Interactive form component layouts & visual web views.
- **Nderitu (Utils & QA):** JSON data stream translation, validation layers, & IO file writers.
