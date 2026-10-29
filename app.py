from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="YC AI Category Forecaster",
    page_icon="📊",
    layout="wide",
)

BASE_DIR = Path(__file__).parent

FORECAST_COLUMNS = ["Naive", "Moving Average", "Linear Trend"]
MODEL_LABELS = {
    "Naive": "Naïve Forecast",
    "Moving Average": "Three-Year Moving Average",
    "Linear Trend": "Linear Trend Regression",
}


# --------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# --------------------------------------------------
@st.cache_data
def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file and cache its contents."""
    return pd.read_csv(file_path)


def load_required_csv(filename: str, required_columns: list[str]) -> pd.DataFrame:
    """Load a required CSV and validate its columns."""
    file_path = BASE_DIR / filename

    if not file_path.exists():
        st.error(f"Required file not found: `{filename}`")
        st.stop()

    try:
        dataframe = load_csv(str(file_path))
    except Exception as error:
        st.error(f"Could not read `{filename}`: {error}")
        st.stop()

    missing_columns = [
        column for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        st.error(
            f"`{filename}` is missing required columns: "
            f"{', '.join(missing_columns)}"
        )
        st.stop()

    return dataframe


forecast_df = load_required_csv(
    "forecast_results.csv",
    ["AI Category", *FORECAST_COLUMNS],
)

mae_df = load_required_csv(
    "model_evaluation.csv",
    ["Forecasting Model", "MAE (percentage points)"],
)

history_path = BASE_DIR / "historical_category_shares.csv"
history_df = load_csv(str(history_path)) if history_path.exists() else None


# --------------------------------------------------
# 3. CLEAN AND VALIDATE VALUES
# --------------------------------------------------
forecast_df["AI Category"] = forecast_df["AI Category"].astype("string").str.strip()

for column in FORECAST_COLUMNS:
    forecast_df[column] = pd.to_numeric(forecast_df[column], errors="coerce")

forecast_df = forecast_df.dropna(
    subset=["AI Category", *FORECAST_COLUMNS]
)
forecast_df = forecast_df[forecast_df["AI Category"] != ""]

if forecast_df.empty:
    st.error("No valid forecast rows were found in `forecast_results.csv`.")
    st.stop()

# Ensure each category appears only once in the forecast table.
if forecast_df["AI Category"].duplicated().any():
    st.warning(
        "Duplicate AI Category rows were found in `forecast_results.csv`. "
        "The first row for each category will be used."
    )
    forecast_df = forecast_df.drop_duplicates(
        subset=["AI Category"], keep="first"
    )

mae_df["Forecasting Model"] = mae_df["Forecasting Model"].astype("string").str.strip()
mae_df["MAE (percentage points)"] = pd.to_numeric(
    mae_df["MAE (percentage points)"], errors="coerce"
)
mae_df = mae_df.dropna(
    subset=["Forecasting Model", "MAE (percentage points)"]
)

if mae_df.empty:
    st.error("No valid MAE results were found in `model_evaluation.csv`.")
    st.stop()

best_model_row = mae_df.loc[
    mae_df["MAE (percentage points)"].idxmin()
]
best_model = str(best_model_row["Forecasting Model"])
best_mae = float(best_model_row["MAE (percentage points)"])

# Match the winning backtested model to the forecast column.
best_model_column = {
    "Naive": "Naive",
    "Naïve": "Naive",
    "Naïve Forecast": "Naive",
    "Three-Year Moving Average": "Moving Average",
    "Moving Average": "Moving Average",
    "Linear Trend": "Linear Trend",
    "Linear Trend Regression": "Linear Trend",
}.get(best_model)

# The supplied evaluation CSV currently reports Naive as best.
# If its label cannot be mapped, use Naive as the documented baseline.
if best_model_column not in FORECAST_COLUMNS:
    best_model_column = "Naive"
    st.warning(
        f"The best model label `{best_model}` could not be matched to a "
        "forecast column. The dashboard is using the Naïve baseline as "
        "the primary ranking; please check `model_evaluation.csv`."
    )

# Historical shares are expected to use a Batch Year column and category
# names as columns. Exclude incomplete 2026 data from historical plots.
if history_df is not None:
    if "Batch Year" not in history_df.columns:
        st.warning(
            "`historical_category_shares.csv` has no `Batch Year` column. "
            "Historical trend charts are unavailable."
        )
        history_df = None
    else:
        history_df["Batch Year"] = pd.to_numeric(
            history_df["Batch Year"], errors="coerce"
        )
        history_df = history_df.dropna(subset=["Batch Year"]).copy()
        history_df["Batch Year"] = history_df["Batch Year"].astype(int)
        history_df = history_df[history_df["Batch Year"] <= 2025].copy()

        for column in history_df.columns:
            if column != "Batch Year":
                history_df[column] = pd.to_numeric(
                    history_df[column], errors="coerce"
                )


# --------------------------------------------------
# 4. PREPARE PRIMARY RANKING AND SUPPORTING SIGNALS
# --------------------------------------------------
forecast_df["Forecast Spread (pp)"] = (
    forecast_df[FORECAST_COLUMNS].max(axis=1)
    - forecast_df[FORECAST_COLUMNS].min(axis=1)
)

ranking_df = forecast_df[
    ["AI Category", best_model_column, "Forecast Spread (pp)"]
].copy()

ranking_df = ranking_df.rename(
    columns={best_model_column: "Predicted Share (%)"}
)

# Add 2023-to-2025 historical change where the historical file supports it.
ranking_df["Historical Change 2023–2025 (pp)"] = pd.NA

if history_df is not None and {2023, 2025}.issubset(
    set(history_df["Batch Year"].tolist())
):
    hist_by_year = history_df.set_index("Batch Year")
    if 2023 in hist_by_year.index and 2025 in hist_by_year.index:
        for idx, category in ranking_df["AI Category"].items():
            if (
                category in hist_by_year.columns
                and pd.notna(hist_by_year.loc[2023, category])
                and pd.notna(hist_by_year.loc[2025, category])
            ):
                ranking_df.loc[idx, "Historical Change 2023–2025 (pp)"] = (
                    float(hist_by_year.loc[2025, category])
                    - float(hist_by_year.loc[2023, category])
                )

ranking_df = ranking_df.sort_values(
    "Predicted Share (%)", ascending=False
).reset_index(drop=True)


# --------------------------------------------------
# 5. DASHBOARD HEADER AND SUMMARY METRICS
# --------------------------------------------------
st.title("YC AI Category Forecaster")
st.caption(
    "Forecasting which AI startup categories may be most represented "
    "in the next Y Combinator batch year."
)

st.info(
    "The forecasts estimate category shares among companies in the "
    "available YC directory data. They do not estimate acceptance "
    "probabilities, investment dollars, or trends across the entire AI market."
)

metric1, metric2, metric3, metric4 = st.columns(4)
with metric1:
    st.metric("AI Candidates", "2,206")
with metric2:
    st.metric("Forecast Year", "2027")
with metric3:
    st.metric("Categories Forecast", f"{len(forecast_df)}")
with metric4:
    st.metric("Best Backtested MAE", f"{best_mae:.2f} pp")

st.caption(
    f"Primary ranking model: {MODEL_LABELS.get(best_model_column, best_model)}. "
    "The model was selected using the supplied historical MAE comparison."
)
st.divider()


# --------------------------------------------------
# 6. PRIMARY CATEGORY RANKING
# --------------------------------------------------
st.header("Predicted AI Category Ranking for 2027")
st.write(
    "Categories are ranked by the primary model's forecasted share. "
    "A higher share means the category is estimated to represent a larger "
    "portion of YC companies in the forecast year; it is not a probability "
    "of YC selecting a startup in that category."
)

top_n = st.slider(
    "Number of categories to display",
    min_value=5,
    max_value=min(18, len(ranking_df)),
    value=min(10, len(ranking_df)),
)

top_ranking = ranking_df.head(top_n).copy()

st.bar_chart(
    top_ranking.set_index("AI Category")[["Predicted Share (%)"]]
)

ranking_display = top_ranking.copy()
for column in [
    "Predicted Share (%)",
    "Forecast Spread (pp)",
    "Historical Change 2023–2025 (pp)",
]:
    ranking_display[column] = pd.to_numeric(
        ranking_display[column], errors="coerce"
    ).round(2)

st.dataframe(
    ranking_display,
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "Forecast spread is the maximum minus the minimum of the three model "
    "estimates. It indicates model disagreement, not a confidence interval."
)
st.divider()


# --------------------------------------------------
# 7. COMPARE ALL THREE FORECASTING MODELS
# --------------------------------------------------
st.header("Forecast Model Comparison")

selected_model = st.selectbox(
    "Choose a forecasting model",
    options=FORECAST_COLUMNS,
    format_func=lambda model: MODEL_LABELS[model],
    index=FORECAST_COLUMNS.index(best_model_column),
)

selected_model_df = (
    forecast_df[["AI Category", selected_model]]
    .sort_values(selected_model, ascending=False)
    .set_index("AI Category")
)

st.bar_chart(selected_model_df)

display_forecast = forecast_df[
    ["AI Category", *FORECAST_COLUMNS, "Forecast Spread (pp)"]
].rename(
    columns={
        "Naive": "Naïve (%)",
        "Moving Average": "Three-Year Moving Average (%)",
        "Linear Trend": "Linear Trend (%)",
    }
)

st.dataframe(
    display_forecast.round(2),
    hide_index=True,
    use_container_width=True,
)
st.caption(
    "The 2027 forecasts were exported from the analysis notebook. "
    "The Naïve forecast carries forward the latest available historical "
    "share; the other models provide alternative estimates."
)
st.divider()


# --------------------------------------------------
# 8. HISTORICAL CATEGORY TRENDS
# --------------------------------------------------
st.header("Historical AI Category Trends")

if history_df is not None:
    available_categories = [
        column for column in history_df.columns
        if column != "Batch Year"
        and (
            column.startswith("AI ")
            or column == "Generative AI"
        )
    ]

    preferred_categories = [
        "AI Developer Tools",
        "AI Agents & Assistants",
        "Generative AI",
        "AI Infrastructure & Data",
        "AI Robotics & Hardware",
    ]
    default_categories = [
        category for category in preferred_categories
        if category in available_categories
    ]

    selected_categories = st.multiselect(
        "Select categories to compare",
        options=available_categories,
        default=default_categories,
    )

    if selected_categories:
        chart_data = (
            history_df[["Batch Year", *selected_categories]]
            .sort_values("Batch Year")
            .set_index("Batch Year")
        )
        st.line_chart(chart_data)
        st.caption(
            "Shares are calculated as category counts divided by all YC "
            "companies in each year. Categories may overlap. The incomplete "
            "2026 data is excluded from this chart."
        )
    else:
        st.info("Select at least one category to display the historical chart.")
else:
    st.warning(
        "Historical data is unavailable. Place "
        "`historical_category_shares.csv` beside `app.py`."
    )

st.divider()


# --------------------------------------------------
# 9. CATEGORY-LEVEL MODEL COMPARISON
# --------------------------------------------------
st.header("Inspect a Category Across Models")

comparison_category = st.selectbox(
    "Choose a category",
    options=forecast_df["AI Category"].tolist(),
    key="comparison_category",
)

selected_row = forecast_df.loc[
    forecast_df["AI Category"] == comparison_category
].iloc[0]

comparison_df = pd.DataFrame(
    {
        "Forecasting Model": [
            MODEL_LABELS[column] for column in FORECAST_COLUMNS
        ],
        "Predicted Share (%)": [
            float(selected_row[column]) for column in FORECAST_COLUMNS
        ],
    }
)

st.bar_chart(comparison_df.set_index("Forecasting Model"))
st.dataframe(
    comparison_df.round(2),
    hide_index=True,
    use_container_width=True,
)

category_spread = (
    comparison_df["Predicted Share (%)"].max()
    - comparison_df["Predicted Share (%)"].min()
)
st.metric("Forecast Spread", f"{category_spread:.2f} pp")
st.caption(
    "A large spread means the estimated share is sensitive to model choice. "
    "It does not quantify the probability that a forecast is wrong."
)
st.divider()


# --------------------------------------------------
# 10. HISTORICAL MODEL EVALUATION
# --------------------------------------------------
st.header("Historical Model Evaluation")

st.write(
    "Mean Absolute Error (MAE) is the average absolute difference between "
    "predicted and observed category shares during historical backtesting. "
    "Lower values indicate better performance on the evaluated periods."
)

mae_df = mae_df.sort_values(
    "MAE (percentage points)", ascending=True
).reset_index(drop=True)

mae_chart_df = mae_df.set_index("Forecasting Model")[
    ["MAE (percentage points)"]
]

st.bar_chart(mae_chart_df)
st.dataframe(
    mae_df.round(2),
    hide_index=True,
    use_container_width=True,
)
st.caption(
    "MAE values are read from `model_evaluation.csv`; this dashboard does "
    "not recalculate the historical backtest."
)
st.divider()


# --------------------------------------------------
# 11. RESEARCH SCOPE AND LIMITATIONS
# --------------------------------------------------
st.header("Research Scope and Limitations")

with st.expander("How should these forecasts be interpreted?"):
    st.markdown(
        """
        - The dataset represents companies listed in the available
          Y Combinator directory, not all startups or the entire AI market.
        - Category share is not investment amount, funding total, or an
          individual startup's acceptance probability.
        - AI candidate identification uses keyword matching and may produce
          false positives or false negatives.
        - The current rule-based taxonomy assigned at least one category to
          1,478 of 2,206 AI candidates (approximately 67.0% coverage).
        - Categories may overlap, so their shares are not mutually exclusive.
        - The incomplete 2026 data is excluded from the main backtesting,
          forecast training, and historical trend chart.
        - The naïve model had the lowest MAE in the supplied backtesting
          results (1.03 percentage points), but this does not guarantee it
          will be best in the future.
        - Forecast spread describes disagreement between models; it is not
          a calibrated confidence interval.
        - The forecasts are exploratory estimates, not guaranteed outcomes
          or official predictions of YC selection priorities.
        """
    )

st.caption(
    "Project: Forecasting AI Startup Category Representation Using "
    "Historical Y Combinator Data."
)
