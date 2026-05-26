# Agentic AI - The Reflection Pattern (Module 2)

This repository contains the laboratory materials and implementations for **Module 2 of the DeepLearning.AI Agentic AI Course**, focusing on the **Reflection Pattern**. 

Reflection is a key design pattern in agentic workflows where an AI agent critiques its own intermediate outputs (e.g., draft code, SQL queries, or the results of executing code), identifies errors or visual/semantic gaps, and refines its output to produce a higher-quality final result.

---

## 📂 Repository Structure

The repository is organized into two primary project directories, each exploring a different dimension of the reflection pattern:

### 1. 📈 [01_reflection/](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection) (Multi-Modal Code & Chart Refinement)
* **[m2_ugl_1.ipynb](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/m2_ugl_1.ipynb)**: The main Jupyter notebook orchestrating the end-to-end chart generation, visual critique, and refinement workflow.
* **[utils.py](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/utils.py)**: Helper module containing functions for loading data, encoding/decoding image files, and executing the generated Python scripts within a safe global namespace.
  * Key helper functions include:
    * `[load_and_prepare_data](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/utils.py#L15-L21)`: Reads the dataset and parses date components (year, quarter, month).
    * `[print_html](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/utils.py#L23-L32)`: Renders strings, tables, or images in standard output.
    * `[get_response](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/utils.py#L51-L52)`: Wraps client calls with automatic retry logic for rate limits.
    * `[image_openai_call](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/utils.py#L72-L73)`: Sends base64-encoded image payloads to the multi-modal Gemini model.
* **[coffee_sales.csv](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/coffee_sales.csv)**: A dataset tracking sales quantities and revenue for different coffee products.

### 2. 🗄️ [02_improving_reflection/](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection) (SQL Generation with External Feedback)
* **[M2_UGL_2.ipynb](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection/M2_UGL_2.ipynb)**: Jupyter notebook demonstrating how SQL query generation is improved by reflecting on query execution results (external environment feedback).
* **[utils.py](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection/utils.py)**: Helper script managing the SQLite database environment.
  * Key helper functions include:
    * `[create_transactions_db](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection/utils.py#L5-L49)`: Sets up an SQLite database loaded with mock retail transaction data.
    * `[get_schema](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection/utils.py#L50-L71)`: Extracts table layouts and data types to construct LLM prompts.
    * `[execute_sql](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection/utils.py#L73-L82)`: Safely executes queries and handles syntax errors, returning results as Pandas DataFrames.

---

## 🛠️ Key Workflows

### 1. Multi-Modal Chart Refinement Pipeline
This workflow demonstrates how an agent can visual-critique its own generated charts using a multi-modal LLM:
```
  [User Prompt] ➔ [Gemini 2.5] ➔ [Matplotlib Code (V1)] ➔ [Exec Python Code] ➔ [chart_v1.png]
                                                                                │
  [chart_v2.png] 🠔 [Exec Python Code] 🠔 [Refined Code (V2)] 🠔 [Multi-Modal Critique] 🠔───┘
```
1. **Initial Draft (V1)**: The model processes the data columns description and a natural language request (e.g. *"Create a bar chart comparing coffee sales by year..."*) and outputs Python code.
2. **Execution**: The system extracts the code blocks wrapped in `<execute_python>` tags, executes the code, and saves `chart_v1.png`.
3. **Multi-Modal Reflection**: The agent passes the generated image along with the original code back to the model. The model critiques the chart's readability, formatting, color combinations, and legends.
4. **Refined Draft (V2)**: The model updates the plotting script (applying the feedback) to generate the final chart, `chart_v2.png`.

### 2. SQL Query Refinement with External Feedback
Evaluating the syntax of a SQL query is not enough to verify semantic correctness. This workflow leverages execution feedback:
1. **Initial Query (V1)**: The model translates a business question into SQLite code based on the table schema.
2. **Database Execution**: The query is executed. In this database, sales events represent a negative inventory change (`qty_delta < 0`). 
3. **Identifying Gaps**: The V1 query calculates total sales using `SUM(qty_delta)`, which evaluates to a negative total. While syntactically valid, this is semantically incorrect (sales totals should be positive).
4. **Reflection**: The output DataFrame is fed back to the model. The model discovers that the sign must be inverted (using `ABS()` or `-qty_delta`).
5. **Corrected Query (V2)**: The model produces a refined SQL query that correctly computes positive sales totals.

---

## 🚀 Setup & Execution

### 1. Installation
Clone the repository and install the dependencies listed in **[requirements.txt](file:///home/dac/DacProjects/dl-agentic-ai/requirements.txt)**:
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a **[.env](file:///home/dac/DacProjects/dl-agentic-ai/.env)** file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your-api-key-here
```

### 3. Launching Labs
Open the directory inside your Jupyter notebook server or IDE environment:
```bash
jupyter notebook
```
* To work on the visualization exercise, run the cells in **[01_reflection/m2_ugl_1.ipynb](file:///home/dac/DacProjects/dl-agentic-ai/01_reflection/m2_ugl_1.ipynb)**.
* To work on the SQL generation exercise, run the cells in **[02_improving_reflection/M2_UGL_2.ipynb](file:///home/dac/DacProjects/dl-agentic-ai/02_improving_reflection/M2_UGL_2.ipynb)**.

---

> [!NOTE]
> All LLM prompts in both modules default to Gemini models (such as `gemini-2.5-flash` or `gemini-3.1-pro-preview`) via the standard `google-genai` SDK or `aisuite` interfaces.

> [!TIP]
> Try experimenting with different model engines in the notebook evaluation sections to observe how the quality of the self-reflection critiques changes.
