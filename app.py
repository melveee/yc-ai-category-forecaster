"""
YC AI Category Forecaster - Streamlit Web Dashboard
A modern, high-contrast, black-and-white analytics platform for forecasting AI startup representation in YC 2027 batches.
"""

from pathlib import Path
import altair as alt
import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. PAGE CONFIGURATION & THEME ENFORCEMENT
# --------------------------------------------------
st.set_page_config(
    page_title="YC AI Category Forecaster",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Comprehensive Black & White CSS with High Contrast Text Enforcement
st.markdown(
    """
    <style>
    /* ==========================================================================
       GLOBAL RESETS & HIGH-CONTRAST TEXT ENFORCEMENT
       ========================================================================== */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    .stApp {
        background-color: #FFFFFF !important;
        color: #333333 !important;
    }
    
    /* Ensure all headers are explicitly black (#111111) */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #111111 !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Standard text elements */
    p, span, div, li, .stMarkdown p {
        color: #333333;
    }
    
    /* Strong/Bold text in black */
    strong, b {
        color: #111111 !important;
        font-weight: 700 !important;
    }
    
    /* Muted and caption text */
    .stCaption, small, .text-muted {
        color: #64748B !important;
    }
    
    /* Widget Labels & Text Inputs */
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #111111 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E5E7EB !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111111 !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #333333 !important;
    }

    /* ==========================================================================
       HERO HEADER & PROJECT INTRODUCTION
       ========================================================================== */
    .hero-container {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 36px 40px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .hero-eyebrow {
        color: #087EA4;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #111111;
        margin: 0 0 12px 0;
        line-height: 1.15;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 22px;
        font-weight: 500;
        color: #333333;
        margin: 0 0 16px 0;
        line-height: 1.4;
    }
    .hero-supporting {
        font-size: 16px;
        font-weight: 400;
        color: #444444;
        margin: 0 0 24px 0;
        line-height: 1.6;
    }
    .about-panel {
        background-color: #F5F5F5;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 20px 24px;
    }
    .about-heading {
        font-size: 18px;
        font-weight: 700;
        color: #111111;
        margin: 0 0 8px 0;
    }
    .about-body {
        font-size: 15.5px;
        font-weight: 400;
        color: #444444;
        line-height: 1.6;
        margin: 0;
    }

    /* ==========================================================================
       KEY STATISTICS METRIC CARDS
       ========================================================================== */
    .stat-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .stat-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .stat-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111111;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .stat-caption {
        font-size: 0.85rem;
        color: #444444;
        line-height: 1.4;
    }
    .mae-banner {
        background-color: #F5F5F5;
        border-left: 3px solid #087EA4;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 16px 0 28px 0;
        font-size: 0.9rem;
        color: #333333;
        line-height: 1.5;
    }

    /* ==========================================================================
       TOP 5 CARDS
       ========================================================================== */
    .top5-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }
    @media (max-width: 1024px) {
        .top5-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 640px) {
        .top5-container {
            grid-template-columns: 1fr;
        }
    }
    .top5-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        min-height: 250px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .top5-card-leader {
        border: 2px solid #0F9D78;
        background: linear-gradient(180deg, #FAFAFA 0%, #FFFFFF 100%);
    }
    .top5-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        background-color: #F1F5F9;
        color: #333333;
        margin-bottom: 12px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        align-self: flex-start;
    }
    .top5-badge-leader {
        background-color: #0F9D78;
        color: #FFFFFF;
    }
    .top5-cat-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111111;
        margin: 0 0 6px 0;
        line-height: 1.3;
    }
    .top5-cat-share {
        font-size: 2.1rem;
        font-weight: 800;
        color: #111111;
        margin: 0 0 10px 0;
        line-height: 1;
    }
    .top5-cat-share-leader {
        color: #0F9D78;
    }
    .top5-cat-desc {
        font-size: 0.85rem;
        color: #444444;
        line-height: 1.5;
        margin: 0;
    }

    /* ==========================================================================
       SECTION WRAPPERS
       ========================================================================== */
    .section-box {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 32px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .section-title {
        font-size: 26px;
        font-weight: 700;
        color: #111111;
        margin: 0 0 6px 0;
        letter-spacing: -0.01em;
    }
    .section-subtitle {
        font-size: 15px;
        color: #444444;
        margin: 0 0 20px 0;
        line-height: 1.5;
    }

    /* Model comparison cards */
    .model-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px;
        height: 100%;
    }
    .model-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #111111;
        margin-bottom: 4px;
    }
    .model-card-desc {
        font-size: 0.85rem;
        color: #444444;
        line-height: 1.45;
        margin: 0;
    }

    /* Sensitivity card */
    .sensitivity-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px;
        height: 100%;
    }
    .sensitivity-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .sensitivity-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111111;
        margin-bottom: 8px;
    }

    /* Evaluation Insight card */
    .eval-insight-card {
        background-color: #F5F5F5;
        border: 1px solid #E5E7EB;
        border-left: 4px solid #0F9D78;
        border-radius: 0 8px 8px 0;
        padding: 18px 20px;
        height: 100%;
    }
    .eval-insight-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #111111;
        margin-bottom: 6px;
    }
    .eval-insight-desc {
        font-size: 0.88rem;
        color: #333333;
        line-height: 1.5;
        margin: 0;
    }

    /* ==========================================================================
       EXPANDER / ACCORDION STYLING (DARK HEADER, PURE WHITE INTERIOR)
       ========================================================================== */
    div[data-testid="stExpander"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
        overflow: hidden !important;
        margin-bottom: 24px !important;
    }
    div[data-testid="stExpander"] details summary {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        padding: 16px 20px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        border-radius: 0px !important;
    }
    div[data-testid="stExpander"] details summary span,
    div[data-testid="stExpander"] details summary p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    div[data-testid="stExpander"] details summary svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #FFFFFF !important;
        padding: 24px 28px !important;
        border-top: 1px solid #E5E7EB !important;
    }
    div[data-testid="stExpanderDetails"] h1,
    div[data-testid="stExpanderDetails"] h2,
    div[data-testid="stExpanderDetails"] h3,
    div[data-testid="stExpanderDetails"] h4 {
        color: #111111 !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
    }
    div[data-testid="stExpanderDetails"] p,
    div[data-testid="stExpanderDetails"] li {
        color: #333333 !important;
        font-size: 15px !important;
        line-height: 1.65 !important;
    }
    div[data-testid="stExpanderDetails"] strong,
    div[data-testid="stExpanderDetails"] b {
        color: #111111 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpanderDetails"] em,
    div[data-testid="stExpanderDetails"] i {
        color: #444444 !important;
    }
    div[data-testid="stExpanderDetails"] ol {
        color: #111111 !important;
        padding-left: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).resolve().parent

FORECAST_COLUMNS = ["Naive", "Moving Average", "Linear Trend"]
MODEL_LABELS = {
    "Naive": "Naïve Forecast",
    "Moving Average": "Three-Year Moving Average",
    "Linear Trend": "Linear Trend Regression",
}

# Plain-English Category Descriptions
CATEGORY_DESCRIPTIONS = {
    "AI Developer Tools": "Developer platforms, AI coding assistants, automated testing, and CI/CD tools that accelerate software engineering.",
    "AI Agents & Assistants": "Autonomous agents, virtual employees, and multi-step conversational workflows that perform complex digital tasks.",
    "AI Robotics & Hardware": "Physical autonomous robots, computer vision systems, drone automation, and dedicated AI hardware devices.",
    "Generative AI": "Core foundation models, multimodal media generators, synthetic voice/video, and generative design platforms.",
    "AI Infrastructure & Data": "High-performance vector databases, GPU cloud orchestration, data labeling pipelines, and scalable model serving.",
    "AI Healthcare & Biotech": "Clinical diagnostic imaging, healthcare record intelligence, biotechnology research, and medical automation.",
    "AI Productivity & Workflow": "Workplace intelligence tools for enterprise search, automated meeting summaries, and document synthesis.",
    "AI Automation": "Robotic process automation (RPA) and intelligent workflow engines replacing repetitive administrative business tasks.",
    "AI FinTech": "Algorithmic underwriting, real-time fraud prevention, automated portfolio intelligence, and regulatory banking technology.",
    "AI Sales & Customer Support": "Conversational customer service bots, outbound prospecting intelligence, and CRM pipeline automation.",
    "AI Marketing & E-commerce": "AI copywriting, automated advertising campaign optimization, and dynamic personalized recommendation engines.",
    "AI Analytics & Business Intelligence": "Natural language database querying, automated executive dashboards, and real-time business anomaly detection.",
    "AI Supply Chain & Logistics": "Predictive inventory management, route optimization, warehouse automation, and freight dispatching.",
    "AI Security": "Autonomous cyber-defense systems, API vulnerability detection, and adversarial AI threat monitoring.",
    "AI Education & Learning": "Personalized digital tutors, automated grading, adaptive study plans, and student learning optimization.",
    "AI Legal & Compliance": "Automated contract review, legal discovery, regulatory policy compliance, and audit preparation tools.",
    "AI HR & Recruiting": "Intelligent candidate resume matching, automated talent sourcing, and employee onboarding workflows.",
    "AI Drug Discovery": "Computational molecular screening, protein structure simulations, target validation, and biochemical synthesis modeling.",
}


# --------------------------------------------------
# 2. DATA LOADING & VALIDATION (PRESERVED)
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
        column for column in required_columns if column not in dataframe.columns
    ]
    if missing_columns:
        st.error(
            f"`{filename}` is missing required columns: {', '.join(missing_columns)}"
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
# 3. CLEAN AND VALIDATE VALUES (PRESERVED)
# --------------------------------------------------
forecast_df["AI Category"] = forecast_df["AI Category"].astype("string").str.strip()

for column in FORECAST_COLUMNS:
    forecast_df[column] = pd.to_numeric(forecast_df[column], errors="coerce")

forecast_df = forecast_df.dropna(subset=["AI Category", *FORECAST_COLUMNS])
forecast_df = forecast_df[forecast_df["AI Category"] != ""]

if forecast_df.empty:
    st.error("No valid forecast rows were found in `forecast_results.csv`.")
    st.stop()

if forecast_df["AI Category"].duplicated().any():
    forecast_df = forecast_df.drop_duplicates(subset=["AI Category"], keep="first")

mae_df["Forecasting Model"] = mae_df["Forecasting Model"].astype("string").str.strip()
mae_df["MAE (percentage points)"] = pd.to_numeric(
    mae_df["MAE (percentage points)"], errors="coerce"
)
mae_df = mae_df.dropna(subset=["Forecasting Model", "MAE (percentage points)"])

if mae_df.empty:
    st.error("No valid MAE results were found in `model_evaluation.csv`.")
    st.stop()

best_model_row = mae_df.loc[mae_df["MAE (percentage points)"].idxmin()]
best_model = str(best_model_row["Forecasting Model"])
best_mae = float(best_model_row["MAE (percentage points)"])

best_model_column = {
    "Naive": "Naive",
    "Naïve": "Naive",
    "Naïve Forecast": "Naive",
    "Three-Year Moving Average": "Moving Average",
    "Moving Average": "Moving Average",
    "Linear Trend": "Linear Trend",
    "Linear Trend Regression": "Linear Trend",
}.get(best_model, "Naive")

if history_df is not None:
    if "Batch Year" not in history_df.columns:
        history_df = None
    else:
        history_df["Batch Year"] = pd.to_numeric(history_df["Batch Year"], errors="coerce")
        history_df = history_df.dropna(subset=["Batch Year"]).copy()
        history_df["Batch Year"] = history_df["Batch Year"].astype(int)
        history_df = history_df[history_df["Batch Year"] <= 2025].copy()
        for column in history_df.columns:
            if column != "Batch Year":
                history_df[column] = pd.to_numeric(history_df[column], errors="coerce")


# --------------------------------------------------
# 4. PREPARE PRIMARY RANKING & SPREAD (PRESERVED)
# --------------------------------------------------
forecast_df["Forecast Spread (pp)"] = (
    forecast_df[FORECAST_COLUMNS].max(axis=1) - forecast_df[FORECAST_COLUMNS].min(axis=1)
)

ranking_df = forecast_df[["AI Category", best_model_column, "Forecast Spread (pp)"]].copy()
ranking_df = ranking_df.rename(columns={best_model_column: "Predicted Share (%)"})

# Add 2023-to-2025 historical change where supported
ranking_df["Historical Change 2023–2025 (pp)"] = pd.NA

if history_df is not None and {2023, 2025}.issubset(set(history_df["Batch Year"].tolist())):
    hist_by_year = history_df.set_index("Batch Year")
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

ranking_df = ranking_df.sort_values("Predicted Share (%)", ascending=False).reset_index(drop=True)
ranking_df["Rank"] = [f"#{i+1}" for i in range(len(ranking_df))]


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
with st.sidebar:
    st.markdown("### Navigation")
    st.markdown(
        """
        - [Introduction](#yc-ai-category-forecaster)
        - [Key Statistics](#key-project-statistics)
        - [Top 5 Categories](#top-5-ai-categories-for-2027)
        - [Complete Ranking](#complete-ai-category-ranking-all-18-categories)
        - [Historical Trends](#historical-ai-category-trends)
        - [Model Comparison](#forecast-model-comparison)
        - [Category Inspection](#category-level-model-inspection)
        - [Model Evaluation](#historical-model-evaluation-accuracy)
        - [Research Scope & Limitations](#research-scope-methodology-and-limitations)
        """
    )
    st.divider()
    st.markdown("### Benchmark Snapshot")
    st.markdown(f"**Primary Model:** {MODEL_LABELS.get(best_model_column, best_model)}")
    st.markdown(f"**Historical MAE:** {best_mae:.2f} percentage points")
    st.markdown("**Dataset Window:** 2005–2025")
    st.markdown("**Forecast Year:** 2027")


# --------------------------------------------------
# SECTION 4: HEADER AND PROJECT INTRODUCTION
# --------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-eyebrow">Y COMBINATOR · AI STARTUP ANALYTICS</div>
        <h1 class="hero-title">YC AI Category Forecaster</h1>
        <div class="hero-subtitle">Exploring the future of AI startups in Y Combinator.</div>
        <p class="hero-supporting">
            Discover how AI startup categories have evolved across Y Combinator companies and explore their forecast representation for 2027.
        </p>
        <div class="about-panel">
            <div class="about-heading">About This Project</div>
            <p class="about-body">
                This project analyses historical Y Combinator startup data to identify AI-related companies, organise them into 18 categories, and understand how these categories have changed over time.
                <br><br>
                Using three forecasting approaches, it estimates the expected representation of each AI category in 2027.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SECTION 5: KEY PROJECT STATISTICS
# --------------------------------------------------
st.markdown('<div id="key-project-statistics"></div>', unsafe_allow_html=True)
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown(
        """
        <div class="stat-card">
            <div>
                <div class="stat-label">AI Candidates</div>
                <div class="stat-value">2,206</div>
            </div>
            <div class="stat-caption">Identified via keyword matching across tags and company descriptions</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat_col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div>
                <div class="stat-label">AI Categories</div>
                <div class="stat-value">{len(forecast_df)}</div>
            </div>
            <div class="stat-caption">Predefined taxonomy tracking specialized and horizontal AI sectors</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat_col3:
    st.markdown(
        """
        <div class="stat-card">
            <div>
                <div class="stat-label">Forecast Year</div>
                <div class="stat-value">2027</div>
            </div>
            <div class="stat-caption">Forward-looking batch cycle based on historical YC batch progression</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with stat_col4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div>
                <div class="stat-label">Best Backtested MAE</div>
                <div class="stat-value">{best_mae:.2f} pp</div>
            </div>
            <div class="stat-caption">Achieved by the {MODEL_LABELS.get(best_model_column, best_model)} baseline</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="mae-banner">
        <strong>Understanding MAE:</strong> <em>Mean Absolute Error (MAE)</em> measures forecast accuracy in simple terms: on average across our historical backtests, predictions differed from actual observed batch shares by only <strong>1.03 percentage points</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SECTION 6: TOP 5 AI CATEGORIES FOR 2027
# --------------------------------------------------
st.markdown('<div id="top-5-ai-categories-for-2027"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="margin-bottom: 14px;">
        <h2 class="section-title">Top 5 AI Categories for 2027</h2>
        <p class="section-subtitle">
            These five categories hold the highest projected representation among AI startups in the 2027 Y Combinator batches.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top5_data = ranking_df.head(5).copy()
top_cols = st.columns(5)

for idx, (_, row) in enumerate(top5_data.iterrows()):
    cat_name = str(row["AI Category"])
    pred_share = float(row["Predicted Share (%)"])
    cat_desc = CATEGORY_DESCRIPTIONS.get(cat_name, "Specialized AI startup sector.")
    is_leader = (idx == 0)

    card_class = "top5-card top5-card-leader" if is_leader else "top5-card"
    badge_class = "top5-badge top5-badge-leader" if is_leader else "top5-badge"
    badge_text = "🥇 #1 Category Leader" if is_leader else f"Rank #{idx + 1}"
    share_class = "top5-cat-share top5-cat-share-leader" if is_leader else "top5-cat-share"

    with top_cols[idx]:
        st.markdown(
            f"""
            <div class="{card_class}">
                <div>
                    <span class="{badge_class}">{badge_text}</span>
                    <h3 class="top5-cat-name">{cat_name}</h3>
                    <div class="{share_class}">{pred_share:.2f}%</div>
                </div>
                <p class="top5-cat-desc">{cat_desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# SECTION 7: COMPLETE AI CATEGORY RANKING
# --------------------------------------------------
st.markdown('<div id="complete-ai-category-ranking-all-18-categories"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-box">
        <h2 class="section-title">Complete AI Category Ranking — All 18 Categories</h2>
        <p class="section-subtitle">
            All 18 categories are ranked below by projected batch representation. 
            A higher forecast share means the category is estimated to represent a larger proportion of companies in the available YC directory data.
            <em>Note: Category representation reflects batch share, not an individual startup's acceptance probability.</em>
        </p>
    """,
    unsafe_allow_html=True,
)

# Custom High-Contrast Horizontal Altair Bar Chart
chart_df = ranking_df.copy()
chart_df["Label"] = chart_df["Predicted Share (%)"].map(lambda v: f"{v:.2f}%")

bars = alt.Chart(chart_df).mark_bar(cornerRadiusEnd=4, color="#087EA4").encode(
    x=alt.X(
        "Predicted Share (%):Q",
        title="Predicted Share (% of Total YC Batch)",
        axis=alt.Axis(
            grid=True,
            gridColor="#F1F5F9",
            domainColor="#E5E7EB",
            labelColor="#333333",
            titleColor="#111111",
            labelFontSize=11,
            titleFontSize=12,
        ),
    ),
    y=alt.Y(
        "AI Category:N",
        sort=alt.EncodingSortField(field="Predicted Share (%)", order="descending"),
        title=None,
        axis=alt.Axis(
            labelLimit=360,
            labelFontSize=12,
            labelFontWeight="bold",
            labelColor="#111111",
            domainColor="#E5E7EB",
        ),
    ),
    tooltip=[
        alt.Tooltip("Rank:N", title="Rank"),
        alt.Tooltip("AI Category:N", title="Category"),
        alt.Tooltip("Predicted Share (%):Q", title="Predicted Share", format=".2f"),
        alt.Tooltip("Forecast Spread (pp):Q", title="Forecast Spread (pp)", format=".2f"),
    ],
)

text_labels = bars.mark_text(
    align="left",
    baseline="middle",
    dx=6,
    fontSize=11,
    fontWeight="bold",
    color="#111111",
).encode(
    text="Label:N"
)

horizontal_chart = (
    (bars + text_labels)
    .properties(
        height=540,
        width="container",
        background="#FFFFFF",
    )
    .configure_view(strokeWidth=0, fill="#FFFFFF")
)

st.altair_chart(horizontal_chart, width="stretch")

st.markdown("<h4 style='font-size: 16px; margin: 20px 0 8px 0; color: #111111;'>Ranking &amp; Signals Table</h4>", unsafe_allow_html=True)
ranking_table = ranking_df[
    ["Rank", "AI Category", "Predicted Share (%)", "Forecast Spread (pp)", "Historical Change 2023–2025 (pp)"]
].copy()

for col in ["Predicted Share (%)", "Forecast Spread (pp)", "Historical Change 2023–2025 (pp)"]:
    ranking_table[col] = pd.to_numeric(ranking_table[col], errors="coerce").round(2)

st.dataframe(
    ranking_table,
    hide_index=True,
    width="stretch",
)

st.markdown(
    """
    <p style="font-size: 0.85rem; color: #64748B; margin-top: 8px;">
        📌 <strong>Reading Signals:</strong> <em>Forecast Spread</em> is the difference between the maximum and minimum forecast among the three models (indicating model consensus, not confidence intervals). 
        <em>Historical Change (2023–2025)</em> reflects recent category momentum in percentage points.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SECTION 8: HISTORICAL AI CATEGORY TRENDS
# --------------------------------------------------
st.markdown('<div id="historical-ai-category-trends"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-box">
        <h2 class="section-title">Historical AI Category Trends</h2>
        <p class="section-subtitle">
            Track multi-year category representation across observed historical Y Combinator batches (2010–2025).
            <br>
            <strong>How to interpret:</strong> Upward trends indicate increasing category representation in historical YC company data. 
            Downward or flat trends indicate slower growth or declining representation relative to emerging sectors.
        </p>
    """,
    unsafe_allow_html=True,
)

if history_df is not None:
    available_categories = [
        col for col in history_df.columns
        if col != "Batch Year" and (col.startswith("AI ") or col == "Generative AI")
    ]

    preferred_defaults = [
        "AI Developer Tools",
        "AI Agents & Assistants",
        "AI Robotics & Hardware",
        "Generative AI",
        "AI Infrastructure & Data",
    ]
    default_selection = [c for c in preferred_defaults if c in available_categories]

    selected_categories = st.multiselect(
        "Select categories to display on the historical chart:",
        options=available_categories,
        default=default_selection,
        help="Select any combination of categories to inspect their annual representation shares.",
    )

    if selected_categories:
        # Filter strictly for observed historical years 2010 through 2025
        observed_history = history_df[
            (history_df["Batch Year"] >= 2010) & (history_df["Batch Year"] <= 2025)
        ]
        
        melted_history = observed_history.melt(
            id_vars=["Batch Year"],
            value_vars=selected_categories,
            var_name="Category",
            value_name="Share (%)",
        )

        trend_chart = (
            alt.Chart(melted_history)
            .mark_line(point=True)
            .encode(
                x=alt.X(
                    "Batch Year:O",
                    title="Observed Historical Batch Year (2010–2025)",
                    axis=alt.Axis(
                        labelAngle=0,
                        labelColor="#333333",
                        titleColor="#111111",
                        gridColor="#F1F5F9",
                        domainColor="#E5E7EB",
                    ),
                ),
                y=alt.Y(
                    "Share (%):Q",
                    title="Category Share (% of YC Companies in Year)",
                    axis=alt.Axis(
                        labelColor="#333333",
                        titleColor="#111111",
                        gridColor="#F1F5F9",
                        domainColor="#E5E7EB",
                    ),
                ),
                color=alt.Color(
                    "Category:N",
                    title="AI Category",
                    scale=alt.Scale(scheme="category10"),
                ),
                tooltip=[
                    alt.Tooltip("Batch Year:O", title="Year"),
                    alt.Tooltip("Category:N", title="Category"),
                    alt.Tooltip("Share (%):Q", title="Observed Share", format=".2f"),
                ],
            )
            .properties(
                height=380,
                width="container",
                background="#FFFFFF",
            )
            .configure_view(strokeWidth=0, fill="#FFFFFF")
            .configure_legend(
                labelColor="#111111",
                titleColor="#111111",
                fillColor="#FFFFFF",
                strokeColor="#E5E7EB",
                labelFontSize=11,
            )
        )

        st.altair_chart(trend_chart, width="stretch")
        st.caption(
            "Shares are calculated as category counts divided by all YC companies in each year. "
            "Data reflects verified historical years (2010–2025). The partial 2026 year and future 2027 projections are not plotted as historical observations."
        )
    else:
        st.info("Select at least one category above to display the historical trend line.")
else:
    st.warning("Historical category share data is unavailable.")

st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# SECTION 9: FORECAST MODEL COMPARISON
# --------------------------------------------------
st.markdown('<div id="forecast-model-comparison"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-box">
        <h2 class="section-title">Forecast Model Comparison</h2>
        <p class="section-subtitle">
            Compare predictions across the three evaluated time-series baseline approaches.
        </p>
    """,
    unsafe_allow_html=True,
)

m_col1, m_col2, m_col3 = st.columns(3)

with m_col1:
    st.markdown(
        """
        <div class="model-card">
            <div class="model-card-title">1. Naïve Forecast (Selected Primary)</div>
            <p class="model-card-desc">Assumes the upcoming batch will continue the latest observed annual share (2025). Achieved the lowest error in historical testing.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col2:
    st.markdown(
        """
        <div class="model-card">
            <div class="model-card-title">2. Three-Year Moving Average</div>
            <p class="model-card-desc">Takes the arithmetic mean of the past three completed years (2023–2025) to smooth out short-term fluctuations and anomalies.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col3:
    st.markdown(
        """
        <div class="model-card">
            <div class="model-card-title">3. Linear Trend Regression</div>
            <p class="model-card-desc">Fits an ordinary least squares regression line across historical annual shares and extrapolates the trajectory forward to 2027.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

model_selector_col, _ = st.columns([1, 1])
with model_selector_col:
    selected_model = st.selectbox(
        "Choose a forecasting model to inspect category distribution:",
        options=FORECAST_COLUMNS,
        format_func=lambda model: MODEL_LABELS[model],
        index=FORECAST_COLUMNS.index(best_model_column),
    )

# Horizontal bar chart for the selected model
sel_model_data = (
    forecast_df[["AI Category", selected_model]]
    .sort_values(selected_model, ascending=False)
    .rename(columns={selected_model: "Share (%)"})
)
sel_model_data["Label"] = sel_model_data["Share (%)"].map(lambda v: f"{v:.2f}%")

model_bars = alt.Chart(sel_model_data).mark_bar(cornerRadiusEnd=4, color="#111111").encode(
    x=alt.X(
        "Share (%):Q",
        title=f"Forecast Share (%) — {MODEL_LABELS[selected_model]}",
        axis=alt.Axis(grid=True, gridColor="#F1F5F9", domainColor="#E5E7EB", labelColor="#333333", titleColor="#111111"),
    ),
    y=alt.Y(
        "AI Category:N",
        sort=alt.EncodingSortField(field="Share (%)", order="descending"),
        title=None,
        axis=alt.Axis(labelLimit=360, labelFontSize=11, labelFontWeight="bold", labelColor="#111111", domainColor="#E5E7EB"),
    ),
    tooltip=[
        alt.Tooltip("AI Category:N", title="Category"),
        alt.Tooltip("Share (%):Q", title="Share (%)", format=".2f"),
    ],
)

model_text = model_bars.mark_text(
    align="left",
    baseline="middle",
    dx=6,
    fontSize=11,
    fontWeight="bold",
    color="#111111",
).encode(text="Label:N")

model_chart = (
    (model_bars + model_text)
    .properties(height=480, width="container", background="#FFFFFF")
    .configure_view(strokeWidth=0, fill="#FFFFFF")
)

st.altair_chart(model_chart, width="stretch")

st.markdown("<h4 style='font-size: 16px; margin: 20px 0 8px 0; color: #111111;'>Multi-Model Comparison Table</h4>", unsafe_allow_html=True)
display_forecast = forecast_df[
    ["AI Category", *FORECAST_COLUMNS, "Forecast Spread (pp)"]
].rename(
    columns={
        "Naive": "Naïve (%)",
        "Moving Average": "3-Yr Moving Avg (%)",
        "Linear Trend": "Linear Trend (%)",
    }
).sort_values("Naïve (%)", ascending=False)

st.dataframe(
    display_forecast.round(2),
    hide_index=True,
    width="stretch",
)

st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# SECTION 10: CATEGORY-LEVEL MODEL INSPECTION
# --------------------------------------------------
st.markdown('<div id="category-level-model-inspection"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-box">
        <h2 class="section-title">Category-Level Model Inspection</h2>
        <p class="section-subtitle">
            Inspect any individual AI category to understand how the three forecasting approaches project its future share, 
            and evaluate the sensitivity between models.
        </p>
    """,
    unsafe_allow_html=True,
)

inspect_cat = st.selectbox(
    "Select an AI category to inspect:",
    options=forecast_df["AI Category"].tolist(),
    key="cat_inspect_select",
)

selected_cat_row = forecast_df.loc[forecast_df["AI Category"] == inspect_cat].iloc[0]

comp_col1, comp_col2 = st.columns([3, 2])

with comp_col1:
    cat_models_df = pd.DataFrame(
        {
            "Forecasting Approach": [MODEL_LABELS[col] for col in FORECAST_COLUMNS],
            "Forecasted Share (%)": [float(selected_cat_row[col]) for col in FORECAST_COLUMNS],
        }
    )
    cat_models_df["Label"] = cat_models_df["Forecasted Share (%)"].map(lambda v: f"{v:.2f}%")

    inspect_bars = alt.Chart(cat_models_df).mark_bar(cornerRadiusEnd=4, color="#087EA4").encode(
        x=alt.X(
            "Forecasted Share (%):Q",
            title="Predicted Share (%)",
            axis=alt.Axis(grid=True, gridColor="#F1F5F9", domainColor="#E5E7EB", labelColor="#333333", titleColor="#111111"),
        ),
        y=alt.Y(
            "Forecasting Approach:N",
            title=None,
            axis=alt.Axis(labelColor="#111111", labelFontSize=12, labelFontWeight="bold", domainColor="#E5E7EB"),
        ),
        tooltip=["Forecasting Approach", alt.Tooltip("Forecasted Share (%):Q", format=".2f")],
    )

    inspect_text = inspect_bars.mark_text(
        align="left",
        baseline="middle",
        dx=6,
        fontSize=11,
        fontWeight="bold",
        color="#111111",
    ).encode(text="Label:N")

    inspect_chart = (
        (inspect_bars + inspect_text)
        .properties(height=200, width="container", background="#FFFFFF")
        .configure_view(strokeWidth=0, fill="#FFFFFF")
    )
    
    st.altair_chart(inspect_chart, width="stretch")

with comp_col2:
    spread_val = float(selected_cat_row["Forecast Spread (pp)"])
    st.markdown(
        f"""
        <div class="sensitivity-card">
            <div class="sensitivity-label">Forecast Spread (Model Disagreement)</div>
            <div class="sensitivity-value">{spread_val:.2f} pp</div>
            <p style="font-size: 0.88rem; color: #333333; line-height: 1.5; margin-bottom: 12px;">
                {"🟢 <strong>High Model Consensus:</strong> All three models project very similar shares (spread ≤ 2.0 pp)." if spread_val <= 2.0 else "🟡 <strong>Sensitivity to Trajectory:</strong> Estimates differ moderately because recent momentum extrapolates higher than the rolling baseline."}
            </p>
            <p style="font-size: 0.85rem; color: #444444; line-height: 1.45; margin: 0;">
                <strong>About this sector:</strong><br>{CATEGORY_DESCRIPTIONS.get(inspect_cat, '')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# SECTION 11: HISTORICAL MODEL EVALUATION
# --------------------------------------------------
st.markdown('<div id="historical-model-evaluation-accuracy"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-box">
        <h2 class="section-title">Historical Model Evaluation &amp; Accuracy</h2>
        <p class="section-subtitle">
            Models were evaluated using chronological backtesting on historical YC batch data (2018–2025). 
            Predictions were generated from earlier years and evaluated against subsequently observed shares.
        </p>
    """,
    unsafe_allow_html=True,
)

eval_col1, eval_col2 = st.columns([3, 2])

sorted_mae_df = mae_df.sort_values("MAE (percentage points)", ascending=True).reset_index(drop=True)
sorted_mae_df["Label"] = sorted_mae_df["MAE (percentage points)"].map(lambda v: f"{v:.2f} pp")

with eval_col1:
    mae_bars = alt.Chart(sorted_mae_df).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X(
            "MAE (percentage points):Q",
            title="Mean Absolute Error (percentage points — lower is better)",
            axis=alt.Axis(grid=True, gridColor="#F1F5F9", domainColor="#E5E7EB", labelColor="#333333", titleColor="#111111"),
        ),
        y=alt.Y(
            "Forecasting Model:N",
            sort="x",
            title=None,
            axis=alt.Axis(labelFontSize=12, labelFontWeight="bold", labelColor="#111111", domainColor="#E5E7EB"),
        ),
        color=alt.condition(
            alt.datum["Forecasting Model"] == best_model,
            alt.value("#0F9D78"),  # Highlight winning model in success green
            alt.value("#087EA4"),  # Others in accent blue
        ),
        tooltip=["Forecasting Model", alt.Tooltip("MAE (percentage points):Q", format=".2f")],
    )

    mae_text = mae_bars.mark_text(
        align="left",
        baseline="middle",
        dx=6,
        fontSize=11,
        fontWeight="bold",
        color="#111111",
    ).encode(text="Label:N")

    mae_chart = (
        (mae_bars + mae_text)
        .properties(height=180, width="container", background="#FFFFFF")
        .configure_view(strokeWidth=0, fill="#FFFFFF")
    )
    st.altair_chart(mae_chart, width="stretch")

with eval_col2:
    st.markdown(
        """
        <div class="eval-insight-card">
            <div class="eval-insight-title">Evaluation Key Takeaway</div>
            <p class="eval-insight-desc">
                <strong>Mean Absolute Error (MAE)</strong> measures how far historical model predictions were from actual results on average.
                <br><br>
                <strong>Lower error indicates better historical performance on the evaluated periods.</strong> 
                The Naïve baseline achieved the lowest error (<strong>1.03 pp</strong>), making it the most defensible choice for our primary 2027 forecast. This historical accuracy does not guarantee identical performance in future batches.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<h4 style='font-size: 16px; margin: 16px 0 8px 0; color: #111111;'>Evaluation Metrics Table</h4>", unsafe_allow_html=True)
st.dataframe(
    sorted_mae_df[["Forecasting Model", "MAE (percentage points)"]].round(2),
    hide_index=True,
    width="stretch",
)

st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# SECTION 12: RESEARCH SCOPE, METHODOLOGY & LIMITATIONS
# --------------------------------------------------
st.markdown('<div id="research-scope-methodology-and-limitations"></div>', unsafe_allow_html=True)
with st.expander("📚 Research Scope, Methodology & Technical Limitations", expanded=False):
    st.markdown(
        """
        ### Methodology & Technical Considerations
        
        1. **Dataset Scope:** The dataset reflects startups listed in the public Y Combinator directory (2005–2026), representing YC investments rather than the entire global startup universe.
        2. **Keyword Candidate Identification:** 2,206 AI candidates were identified using regex matching on keywords such as *AI*, *Artificial Intelligence*, *Machine Learning*, *Deep Learning*, *Generative AI*, *NLP*, and *LLM*.
        3. **Taxonomy & Category Assignment:** Predefined rules mapped 1,478 companies to at least one of 18 categories (~67.0% assignment coverage).
        4. **Overlapping Categories:** Categories are non-mutually exclusive. A company building an AI coding assistant may be classified under both *AI Developer Tools* and *AI Agents & Assistants*. Therefore, category shares do not sum to 100%.
        5. **Exclusion of Partial 2026 Batches:** 2026 batch records were incomplete at the time of export and were excluded from time-series backtesting and forecast training to avoid historical distortion.
        6. **Category Representation vs. Acceptance Odds:** Projected percentages indicate the estimated proportion of YC batch companies in a category. They do **not** represent an individual applicant's probability of acceptance.
        7. **Forecast Uncertainty:** Projections are exploratory baseline estimates. Model spread highlights sensitivity to methodology rather than a calibrated statistical confidence interval.
        """
    )

st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 24px 0 16px 0;">
        YC AI Category Forecaster • Data Science Portfolio Project • 2027 Forward Projections
    </div>
    """,
    unsafe_allow_html=True,
)
