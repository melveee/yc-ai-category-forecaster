# Forecasting AI Startup Categories at Y Combinator (2027)

A Data Science project analyzing historical Y Combinator startup data to identify AI categories that may gain representation in future batches.

## Overview

Which AI startup categories are likely to receive greater attention in Y Combinator's 2027 batches?

This project analyzes historical Y Combinator company data, identifies potential AI-related startups using keyword-based text matching, groups companies into predefined AI categories, and compares multiple forecasting baselines to estimate category representation for 2027.

The project combines exploratory data analysis, data preprocessing, rule-based text classification, time-aware backtesting, forecasting, and an interactive Streamlit dashboard.

**Important:** The forecasts estimate category representation among companies in the available Y Combinator dataset. They do not directly predict investment dollars, acceptance probabilities, or trends across the entire AI startup ecosystem.

## Research Question

Based on historical Y Combinator startup data, which AI startup categories may have greater representation in 2027?

## Dataset

- **Source:** [Y Combinator Directory Dataset — Kaggle](https://www.kaggle.com/datasets/yuhesh/y-combinator-directory-2005-2026)
- **File:** `yc_startups_dataset.csv`
- **Dataset size:** 5,785 rows and 18 columns
- **Historical coverage:** 2005–2026
- **Main fields:** Company Name, Batch Year, Tags, Sub-Industry, and Company Description

The dataset contains historical company-directory information. It does not provide a complete record of investor funding amounts or rejected YC applications.

## Methodology

### 1. Data Understanding and Cleaning

- Inspected dataset dimensions, column types, and missing values.
- Checked for duplicate records and duplicate company identifiers.
- Examined missing values in important fields.
- Reviewed the available historical coverage.

### 2. AI Candidate Identification

Used keyword-based matching across company tags and descriptions to identify potential AI-related companies.

The matching terms included Artificial Intelligence, Machine Learning, Deep Learning, Generative AI, NLP, LLM, and related expressions.

This produced **2,206 AI candidates**.

Candidate identification is rule-based and has not been independently verified for every company. Therefore, these records should be interpreted as potential AI candidates rather than a perfectly classified AI dataset.

### 3. AI Category Assignment

Mapped startup tags to 18 predefined AI categories, including:

- AI Developer Tools
- Generative AI
- AI Agents & Assistants
- AI Infrastructure & Data
- AI Robotics & Hardware
- AI Healthcare & Biotech
- AI Automation
- AI Security

The taxonomy uses rule-based tag matching and permits a company to belong to multiple categories.

Of the 2,206 AI candidates, **1,478 were assigned at least one category**, giving a category-assignment coverage of approximately **67.0%**. The remaining 728 candidates were not assigned a category by the current rules.

Coverage measures whether a category was assigned; it does not establish classification accuracy.

### 4. Historical Trend Analysis

Calculated annual category shares using the total number of Y Combinator companies in each year as the denominator.

This allows category representation to be compared across years with different numbers of companies.

Categories can overlap, so their shares should not be added together as though they were mutually exclusive.

The 2026 data is partial and was excluded from the main 2018–2025 forecasting backtest and the forecast training data.

### 5. Forecasting Models

Compared three baseline approaches:

- **Naïve:** Uses the latest available historical category share.
- **Three-Year Moving Average:** Uses the average of the latest three annual category shares.
- **Linear Trend:** Fits a linear regression model to historical annual category shares and extrapolates forward.

The models were evaluated using time-aware backtesting, with forecasts generated from earlier years and compared with subsequently observed shares. A random train-test split was not used.

### 6. Model Evaluation

The primary evaluation metric is Mean Absolute Error (MAE), expressed in percentage points.

| Forecasting model | Overall MAE |
|---|---:|
| Naïve | **1.03 pp** |
| Linear Trend | 1.14 pp |
| Three-Year Moving Average | 1.23 pp |

The naïve baseline achieved the lowest overall MAE among the three evaluated models. This result supports using it as the main baseline for comparison, but does not establish that it will always outperform the other approaches.

### 7. Forecast Comparison for 2027

The following figures are the arithmetic averages of the three model forecasts. They are exploratory comparison estimates, not validated probabilities.

| AI category | Average forecast |
|---|---:|
| AI Developer Tools | 12.03% |
| Generative AI | 9.87% |
| AI Agents & Assistants | 8.28% |
| AI Healthcare & Biotech | 6.51% |
| AI Productivity & Workflow | 5.95% |
| AI Infrastructure & Data | 5.84% |
| AI Robotics & Hardware | 5.71% |
| AI Automation | 5.54% |

Forecasts from the three models differ, especially for categories with substantial changes in recent years. Model disagreement is reported as the maximum forecast minus the minimum forecast; it is not a statistical confidence interval.

### 8. Historical Findings: 2023–2025

Two notable changes in category representation were:

- **AI Robotics & Hardware:** increased by 5.79 percentage points.
- **AI Infrastructure & Data:** increased by 2.53 percentage points.

In contrast:

- **Generative AI:** decreased by 9.92 percentage points.
- **AI Healthcare & Biotech:** decreased by 1.99 percentage points.
- **AI Sales & Customer Support:** decreased by 1.98 percentage points.

AI Developer Tools had the highest average 2027 forecast despite a 1.28-percentage-point decline in its historical share between 2023 and 2025. This illustrates why forecast levels and historical momentum should be interpreted separately.

## Interactive Dashboard

The Streamlit dashboard provides:

- A comparison of the three 2027 forecasting models.
- Historical category-share trends.
- Category-level forecast comparisons.
- Forecast disagreement analysis.
- Historical model MAE comparisons.

The dashboard reads the exported CSV files so that results can be inspected without rerunning the entire analysis notebook.

## Project Structure

```text
DS-YC-AI_Investment-Forecasting/
├── app.py
├── README.md
├── yc_startup_dataset.ipynb
├── historical_category_shares.csv
├── forecast_results.csv
├── model_evaluation.csv
└── archive/
```

- `yc_startup_dataset.ipynb` — data preparation, exploratory analysis, category assignment, historical trends, backtesting, and forecasting.
- `app.py` — Streamlit dashboard.
- `historical_category_shares.csv` — exported annual category-share data.
- `forecast_results.csv` — exported forecast comparisons.
- `model_evaluation.csv` — exported model evaluation metrics.
- `archive/` — supporting or previous project files.

## Run Locally

### Prerequisites

- Python installed.
- Git, if cloning the repository.
- The project files and CSV exports in the project directory.

### Installation

1. Clone the repository or download the project.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment if desired.
4. Install Streamlit and the other Python packages imported by `app.py`.
5. Launch the dashboard:

```bash
streamlit run app.py
```

If the dashboard reports missing packages, install the required dependencies. A `requirements.txt` file can be added to make environment setup reproducible.

## Limitations

1. **Dataset scope:** The analysis covers companies represented in the available Y Combinator directory data, not every AI startup or investor.
2. **No funding amounts:** Category shares do not measure investment capital, valuations, or investor returns.
3. **Keyword-based AI identification:** Keyword matching may miss relevant companies or include false positives.
4. **Incomplete category assignment:** Only 67.0% of identified candidates received at least one category under the current rules.
5. **Rule-based taxonomy:** Category mapping depends on predefined tags and may not accurately capture every company's primary business.
6. **Overlapping categories:** A company may belong to multiple categories, so shares are not mutually exclusive.
7. **Partial 2026 data:** The incomplete 2026 year was excluded from the main historical backtesting and forecast training.
8. **Limited forecasting methods:** Only three baseline models were evaluated.
9. **Historical dependence:** Changes in YC's batch composition, selection practices, and startup terminology may affect the results.
10. **Forecast uncertainty:** The forecasts are exploratory estimates. Model disagreement does not provide a formal prediction interval.

## Conclusion

This project establishes a reproducible baseline workflow for examining historical AI startup-category representation in Y Combinator data.

AI Developer Tools has the highest average forecast across the three evaluated models, while AI Robotics & Hardware shows the strongest increase in historical category share between 2023 and 2025. AI Infrastructure & Data also exhibits positive historical momentum.

However, the findings should be interpreted as exploratory forecasts of YC company-category representation rather than predictions of investment dollars or the overall AI startup market.

Future improvements could include stronger manual validation of AI candidates, improved category classification, dynamically calculated backtesting metrics, additional forecasting methods, and more extensive historical validation.

## Technologies Used

- Python
- Pandas
- Jupyter Notebook
- Scikit-learn
- Streamlit
- Exploratory Data Analysis
- Rule-Based Text Matching
- Time-Series Backtesting
- Forecast Evaluation

## Author

Developed as a Data Science portfolio project focused on historical startup data, forecasting, and interactive data visualization.
