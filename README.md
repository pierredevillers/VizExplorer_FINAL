# **VizExplorer_FINAL**

A **Visual Natural Language Interface (V-NLI)** application designed for intuitive interaction with financial datasets using natural language queries. This project leverages advanced Text-to-SQL techniques, with performance metrics measured trained on the **BIRD** dataset included for evaluation.

---

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Data and Models](#data-and-models)
4. [Performance and Results](#performance-and-results)
5. [Project Structure](#project-structure)

---

## **Project Overview**

VizExplorer is a **V-NLI application** that enables users to query financial datasets in plain language, automatically translating their input into SQL, executing the query, and visualizing results. The system is optimized for financial analysis tasks and supports database schema generation, and output visualizations.

---

## **Features**

- **Natural Language to SQL**: Seamlessly converts natural language queries to SQL.
- **Interactive Interface**: Built with Streamlit for an intuitive user experience. 
- **Performance Metrics**: Logs and evaluates model outputs trained on the **BIRD** dataset with accuracy.
- **Database Management**: Prepares, validates, and executes queries on PostgreSQL and SQLite.

## **Data and Models**

### **Data**

- **BIRD Dataset**:
  - Location: `data/BIRD_dataset/`
  - Contains database schemas, queries, and evaluation data.

- **Spider Dataset (TEST)**:
  - Location: `data/Spider_dataset_TEST/`
  - Used for additional validation and testing.

- **Actual Data**:
  - Location: `data/actual_data/`
  - Real-world datasets for testing.

### **Models**

- **Output Directory**:
  - Location: `model_output/`
  - Includes:
    - `bird_model_output_formatted.json`: Processed model outputs.
    - `bird_model_output.json`: Raw model predictions.

---

## **Performance and Results**

- **Evaluation Logs**:
  - Location: `logs/`
  - Files: `evaluation_log.log`, `training_log.log`

- **Metrics**:
  - Accuracy, SQL query success rate, and execution time.
  - Visualized in `performance_measure/Perf_measures.png`.

- **Performance Scripts**:
  - Scripts in `performance_measure/` generate and log results.

---

## **Project Structure**

```
VizExplorer_FINAL/
├── README.md                   # Project overview and instructions
├── LICENSE                     # Licensing information
├── .streamlit/                 # Streamlit configuration files
├── data/                       # Dataset-related files
│   ├── BIRD_dataset/           # BIRD-specific data and scripts
│   ├── Spider_dataset_TEST/    # Spider dataset for testing
│   ├── actual_data/            # Real-world testing datasets
│   └── ...
├── logs/                       # Log files for performance tracking
├── model_output/               # Model outputs (formatted and raw)
├── model_training/             # Scripts for training models
├── performance_measure/        # Performance evaluation scripts and results
├── utils/                      # Utility scripts and configuration files
│   ├── .env                    # Environment variables
│   └── app.py                  # Streamlit app entry point
├── requirements.txt            # Python dependencies
```

