
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="YC AI Forecasting",
    page_icon="📊",
    layout="wide",
)

BASE_DIR = Path(__file__).parent


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_csv(file_path):
    """Load a CSV file and cache its contents."""
    return pd.read_csv(file_path)


def load_required_csv(filename, required_columns):
    """Load a CSV and validate its required columns."""
    file_path = BASE_DIR / filename

    if not file_path.exists():
        st.error(f"Required file not found: {filename}")
        st.stop()

    try:
        df = load_csv(file_path)
    except Exception as error:
        st.error(f"Could not read {filename}: {error}")
        st.stop()

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            f"{filename} is missing these columns: "
            f"{', '.join(missing_columns)}"
        )
        st.stop()

    return df


forecast_df = load_required_csv(
    "forecast_results.csv",
    [
        "AI Category",
        "Naive",
        "Moving Average",
        "Linear Trend",
    ],
)

mae_df = load_required_csv(
    "model_evaluation.csv",
    [
        "Forecasting Model",
        "MAE (percentage points)",
    ],
)

history_path = BASE_DIR / "historical_category_shares.csv"

if history_path.exists():
    history_df = load_csv(history_path)
else:
    history_df = None


# --------------------------------------------------
# 3. VALIDATE DATA TYPES
# --------------------------------------------------

forecast_columns = [
    "Naive",
    "Moving Average",
    "Linear Trend",
]

for column in forecast_columns:
    forecast_df[column] = pd.to_numeric(
        forecast_df[column],
        errors="coerce",
    )

mae_df["MAE (percentage points)"] = pd.to_numeric(
    mae_df["MAE (percentage points)"],
    errors="coerce",
)

forecast_df = forecast_df.dropna(
    subset=["AI Category"] + forecast_columns
)

mae_df = mae_df.dropna(
    subset=["Forecasting Model", "MAE (percentage points)"]
)


# --------------------------------------------------
# 4. DASHBOARD HEADER
# --------------------------------------------------

st.title("YC AI Startup Trend Forecasting")

st.caption(
    "Exploring historical Y Combinator data "
    "and preliminary 2027 category forecasts."
)

st.info(
    "These estimates represent the share of YC companies "
    "assigned to each category, not investment dollars "
    "or the entire AI startup market."
)


# --------------------------------------------------
# 5. SUMMARY METRICS
# --------------------------------------------------

best_model_row = mae_df.loc[
    mae_df["MAE (percentage points)"].idxmin()
]

best_model = best_model_row["Forecasting Model"]
best_mae = best_model_row["MAE (percentage points)"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "AI Candidates",
        "2,206",
    )

with col2:
    st.metric(
        "Forecast Year",
        "2027",
    )

with col3:
    st.metric(
        "Best Backtested Baseline",
        best_model,
    )

st.divider()


# --------------------------------------------------
# 6. 2027 FORECAST COMPARISON
# --------------------------------------------------

st.subheader("2027 Forecast Comparison")

selected_model = st.selectbox(
    "Select forecasting method",
    options=forecast_columns,
    format_func=lambda model: {
        "Naive": "Naïve Forecast",
        "Moving Average": "Three-Year Moving Average",
        "Linear Trend": "Linear Trend Regression",
    }[model],
)

chart_df = (
    forecast_df[["AI Category", selected_model]]
    .set_index("AI Category")
    .sort_values(selected_model, ascending=True)
)

st.bar_chart(chart_df)

st.subheader("Forecast Data")

display_forecast = forecast_df.copy()

display_forecast = display_forecast.rename(
    columns={
        "Naive": "Naïve (%)",
        "Moving Average": "Moving Average (%)",
        "Linear Trend": "Linear Trend (%)",
    }
)

st.dataframe(
    display_forecast.round(2),
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "Forecasts use historical category shares through 2025. "
    "Model disagreement is not a calibrated confidence interval."
)


# --------------------------------------------------
# 7. HISTORICAL AI CATEGORY TRENDS
# --------------------------------------------------

st.divider()
st.subheader("Historical AI Category Trends")

if history_df is not None:
    if "Batch Year" not in history_df.columns:
        st.error(
            "historical_category_shares.csv must contain "
            "a 'Batch Year' column."
        )
    else:
        history_df["Batch Year"] = pd.to_numeric(
            history_df["Batch Year"],
            errors="coerce",
        )

        history_df = history_df.dropna(
            subset=["Batch Year"]
        )

        history_df["Batch Year"] = (
            history_df["Batch Year"].astype(int)
        )

        history_df = history_df[
            history_df["Batch Year"] <= 2025
        ]

        available_categories = [
            column
            for column in history_df.columns
            if column.startswith("AI ")
            or column == "Generative AI"
        ]

        preferred_categories = [
            "AI Developer Tools",
            "AI Agents & Assistants",
            "Generative AI",
        ]

        default_categories = [
            category
            for category in preferred_categories
            if category in available_categories
        ]

        selected_categories = st.multiselect(
            "Select categories to compare",
            options=available_categories,
            default=default_categories,
        )

        if selected_categories:
            chart_data = (
                history_df[
                    ["Batch Year"] + selected_categories
                ]
                .set_index("Batch Year")
                .sort_index()
            )

            chart_data = chart_data.apply(
                pd.to_numeric,
                errors="coerce",
            )

            st.line_chart(chart_data)

            st.caption(
                "Values are percentages of all YC companies "
                "in each year. Categories may overlap."
            )
        else:
            st.info(
                "Select at least one category to display the chart."
            )
else:
    st.warning(
        "Historical data is unavailable. Place "
        "historical_category_shares.csv beside app.py."
    )


# --------------------------------------------------
# 8. FORECAST MODEL COMPARISON
# --------------------------------------------------

st.divider()
st.subheader("Forecast Model Comparison")

comparison_category = st.selectbox(
    "Choose a category to compare across models",
    options=forecast_df["AI Category"].tolist(),
    key="comparison_category",
)

selected_row = forecast_df.loc[
    forecast_df["AI Category"] == comparison_category
].iloc[0]

comparison_df = pd.DataFrame({
    "Forecasting Model": [
        "Naïve Forecast",
        "Three-Year Moving Average",
        "Linear Trend Regression",
    ],
    "Predicted Share (%)": [
        selected_row["Naive"],
        selected_row["Moving Average"],
        selected_row["Linear Trend"],
    ],
})

st.bar_chart(
    comparison_df.set_index("Forecasting Model")
)

st.dataframe(
    comparison_df.round(2),
    hide_index=True,
    use_container_width=True,
)

spread = (
    comparison_df["Predicted Share (%)"].max()
    - comparison_df["Predicted Share (%)"].min()
)

st.metric(
    "Forecast Spread",
    f"{spread:.2f} percentage points",
)

st.caption(
    "Forecast spread measures disagreement among the three "
    "models. It is not a statistical confidence interval."
)


# --------------------------------------------------
# 9. HISTORICAL MODEL EVALUATION
# --------------------------------------------------

st.divider()
st.subheader("Historical Model Evaluation")

st.write(
    "Mean Absolute Error (MAE) measures the average absolute "
    "difference between predicted and actual category shares. "
    "Lower MAE indicates better historical forecasting performance."
)

mae_df = mae_df.sort_values(
    "MAE (percentage points)",
    ascending=True,
)

best_model_row = mae_df.iloc[0]

best_model = best_model_row["Forecasting Model"]
best_mae = best_model_row["MAE (percentage points)"]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Lowest Backtesting MAE",
        f"{best_mae:.2f} pp",
    )

with col2:
    st.metric(
        "Best Performing Baseline",
        best_model,
    )

mae_chart_df = mae_df.set_index(
    "Forecasting Model"
)[["MAE (percentage points)"]]

st.bar_chart(mae_chart_df)

st.dataframe(
    mae_df.round(2),
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "MAE values are loaded from model_evaluation.csv. "
    "They are previously calculated backtesting results, "
    "not recalculated by this dashboard."
)



# --------------------------------------------------
# 2027 YC OPPORTUNITY SUMMARY
# --------------------------------------------------

st.divider()
st.header("2027 AI Startup Opportunity Outlook")

st.write(
    "Which AI startup categories show the strongest "
    "projected representation among Y Combinator companies?"
)

opportunity_categories = [
    "AI Developer Tools",
    "AI Agents & Assistants",
    "Generative AI",
    "AI Robotics & Hardware",
    "AI Infrastructure & Data",
]

opportunity_df = forecast_df[
    forecast_df["AI Category"].isin(opportunity_categories)
].copy()

opportunity_df["Lowest Forecast (%)"] = (
    opportunity_df[forecast_columns].min(axis=1)
)

opportunity_df["Highest Forecast (%)"] = (
    opportunity_df[forecast_columns].max(axis=1)
)

opportunity_df = opportunity_df.sort_values(
    "Naive",
    ascending=False,
)

for _, row in opportunity_df.iterrows():
    with st.container(border=True):
        st.subheader(row["AI Category"])

        st.write(
            f"Forecast range: "
            f"{row['Lowest Forecast (%)']:.2f}%–"
            f"{row['Highest Forecast (%)']:.2f}%"
        )

        st.progress(
            min(float(row["Naive"]) / 100, 1.0),
            text=f"Naïve baseline: {row['Naive']:.2f}%"
        )

st.warning(
    "These are exploratory forecasts of category representation "
    "among YC companies, not estimates of acceptance probability "
    "or official predictions of YC's selection priorities."
)




# --------------------------------------------------
# 10. PROJECT LIMITATIONS
# --------------------------------------------------

st.divider()
st.subheader("Research Scope and Limitations")

with st.expander("How should these forecasts be interpreted?"):
    st.markdown(
        """
        - The dataset represents companies listed in the
          Y Combinator directory, not the entire AI startup market.
        - Category shares are not investment amounts or funding totals.
        - AI candidate detection uses keyword matching and may
          produce false positives or false negatives.
        - Category assignment uses company tags and may not
          fully reflect the role of AI in each company's product.
        - The incomplete 2026 data is excluded from the main
          forecasting analysis.
        - Forecast spread measures disagreement between models;
          it is not a calibrated confidence interval.
        - The forecasts are exploratory estimates, not guaranteed
          future outcomes.
        """
    )

st.caption(
    "Project: Forecasting AI Startup Category Trends Using "
    "Historical Y Combinator Data."
)

