---

# Investor Updates Database & Dashboard

A comprehensive system for parsing, storing, visualizing, and managing investor email updates.
This tool transforms raw `.eml` files into structured data using AI-powered parsing and provides a web-based dashboard for analysis and editing.

---

## Features

* Parse investor update emails (`.eml`) and PDFs into structured data
* Store results in SQLite, Excel, and JSON formats
* Interactive dashboard for company performance tracking
* AI-powered extraction using OpenAI / Gemini
* Editable records via FastAPI
* Built-in database exploration with Datasette

---

## Project Structure

* **CLI Tool** – Parse, manage, and query investor updates
* **SQLite Database** – Persistent structured storage
* **Streamlit Dashboard** – Interactive analytics & visualizations
* **FastAPI Service** – Edit records and upload individual files
* **Datasette** – Direct SQL access and exploration

---

## Setup Instructions

### 1. Open Terminal

### 2. Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sudo sh
```

### 3. Install Python (if not already installed)

```bash
uv python install --preview
```

### 4. Clone the Repository

```bash
git clone <your-repo>
cd <project-directory>
```

### 5. Install Dependencies

```bash
uv pip install -r requirements.txt
uv project lock
uv pip install -e .
```

### 6. Prepare Input Files

* Create a folder on your Desktop called `email_files`
* Add all downloaded `.eml` files and PDFs to this folder

---

## Environment Configuration

Create an `.env` file in the project root and configure the following:

```env
BASE_DIR=your_pathname_to_folder/email_files
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

FOUNDER_DATA=<base_dir>/founder_data.xlsx
DB_PATH=<base_dir>/investor_updates.db
UPDATED_DB=<base_dir>/updated_investor_updates.db
```

> ⚠️ Make sure `base_dir` is replaced with the actual resolved path.

---

## Usage

### Run Full Workflow (Recommended)

```bash
uv run main.py up
```

This will:

* Parse all `.eml` files in `BASE_DIR`
* Update the database
* Launch all dashboard services

---

### Step-by-Step Workflow

```bash
uv run main.py parse       # Extract and store data
uv run main.py serve-gui   # Launch dashboard
```

---

## CLI Commands

| Command          | Purpose                                          | Example                                          |
| ---------------- | ------------------------------------------------ | ------------------------------------------------ |
| `parse`          | Process `.eml` files and extract structured data | `uv run main.py parse`                           |
| `remove`         | Delete all data for a specific company           | `uv run main.py remove "Company Name" --confirm` |
| `show`           | View details for a single company                | `uv run main.py show "Company Name"`             |
| `list-companies` | List all companies in the database               | `uv run main.py list-companies`                  |
| `serve-gui`      | Launch dashboard services                        | `uv run main.py serve-gui`                       |
| `up`             | Parse data + launch dashboard                    | `uv run main.py up`                              |

---

## Output Files

After parsing, data is saved as:

* **SQLite database**: `investor_updates.db`
* **Excel spreadsheet**: `investor_updates.xlsx`
* **JSON schemas**: `json_schemas/`

---

## Dashboard Services

When running `serve-gui` or `up`, the following services start:

| Service   | Port | Description                 |
| --------- | ---- | --------------------------- |
| Streamlit | 8501 | Interactive dashboard       |
| FastAPI   | 8006 | Edit records & upload files |
| Datasette | 8001 | SQL database exploration    |

---

## Dashboard Features

### Tab 1: Company Overview

* ARR trends
* Churn analysis
* Stale updates (> 4 months)
* Runway alerts (< 6 months)

---

### Tab 2: Company Scoring & Analytics

* ARR + company lowlights per update
* Performance tracking between updates
* Scatter plots of company scores
* Downloadable PNG snapshots
* Trend arrows:

  * 🟢 Improvement vs last update
  * 🔴 Decline vs last update
  * ⚪️ Unchanged score since last update
    
* Heatmap comparing predicted vs actual performance based on pre-defined founder characteristics

#### Model Assumptions

**Top Quartile (score ≥ 4)**

* 2 founders
* Same location (USA)
* Same sex & race
* USA origin
* Ivy League / MIT / Stanford / Berkeley
* Serial entrepreneur (>2 startups)
* Strong founder-market fit
* Previous co-founder experience
* No early warning signs

**Middle Quartile (2 ≤ score < 4)**

* ≥ 3 founders
* Different locations
* Partial demographic alignment
* Non-USA origin
* Top US/UK universities
* Repeat founder (2 startups)
* Partial founder-market fit
* Minor early warning signs

**Bottom Quartile (score < 2)**

* Solo founder
* Overseas / remote
* No demographic alignment
* Geopolitical risk
* No repeat founder history
* Weak founder-market fit
* No prior collaboration
* Major early warning signs

A **green box** in the heatmap indicates alignment between predictions and observed performance.

---

### Tab 3: Explore Raw Data

* JSON record explorer
* CSV export of all records
* Direct link to Datasette for SQL queries

---

## Editing Data

Access FastAPI at:

```
http://localhost:8006
```

Capabilities:

* Upload individual `.eml` files
* Edit existing database records
* Changes persist across all interfaces

---

## Direct Database Access

Access Datasette at:

```
http://localhost:8001
```

* Run custom SQL queries
* Apply filters
* Save common queries

---

## Troubleshooting

### No `.eml` Files Found

* Verify `BASE_DIR` in `.env`
* Ensure files have `.eml` extension
* Check file permissions

### API Errors

* Confirm `OPENAI_API_KEY` / `GEMINI_API_KEY`
* Check API quota and billing
* Verify network connectivity

### Dashboard Won’t Start

* Ensure ports `8000`, `8001`, `8501` are free
* Verify dependencies are installed
* Check terminal logs for errors

### Parsing Failures

* Inspect `failed_gpt_output.json`
* Ensure email format is plain text or HTML
* Verify attached PDFs are accessible

---

## Key URLs

* **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
* **Datasette Database**: [http://localhost:8001](http://localhost:8001)
* **FastAPI Editor**: [http://localhost:8006](http://localhost:8006)

---
