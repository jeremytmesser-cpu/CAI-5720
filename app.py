"""Health Correlation Explorer (NHANES 2017-2018).

A Streamlit app for exploring correlations between health measures.
Run with:
    uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

DATA_FILE = "nhanes_health.csv"

# `sex` is text, so it is never offered as a correlation variable.
NUMERIC_COLS = [
    "age",
    "bmi",
    "waist_cm",
    "systolic_bp",
    "diastolic_bp",
    "hba1c",
    "total_chol",
    "hdl_chol",
    "sleep_hours",
    "sedentary_minutes",
]

LABELS = {
    "age": "Age (years)",
    "bmi": "BMI (kg/m²)",
    "waist_cm": "Waist circumference (cm)",
    "systolic_bp": "Systolic BP (mmHg)",
    "diastolic_bp": "Diastolic BP (mmHg)",
    "hba1c": "HbA1c (%)",
    "total_chol": "Total cholesterol (mg/dL)",
    "hdl_chol": "HDL cholesterol (mg/dL)",
    "sleep_hours": "Sleep on workdays (hours)",
    "sedentary_minutes": "Sedentary time (minutes/day)",
}

# Health thresholds used to color points: name -> (column, cutoff)
THRESHOLDS = {
    "High systolic BP (SBP ≥ 130)": ("systolic_bp", 130),
    "High diastolic BP (DBP ≥ 80)": ("diastolic_bp", 80),
    "Obesity (BMI ≥ 30)": ("bmi", 30),
    "Diabetes range (HbA1c ≥ 6.5)": ("hba1c", 6.5),
    "High cholesterol (total ≥ 240)": ("total_chol", 240),
}


# ---------------------------------------------------------------------------
# Calculation functions (no Streamlit calls, so they can be tested alone)
# ---------------------------------------------------------------------------
def load_data(path=DATA_FILE):
    return pd.read_csv(path)


def filter_data(df, sexes, age_range):
    """Keep rows whose sex is in `sexes` and whose age is in [lo, hi]."""
    lo, hi = age_range
    mask = df["sex"].isin(sexes) & df["age"].between(lo, hi)
    return df[mask]


def pair_correlation(df, x, y, method="pearson"):
    """Return (r, n) for two columns, using only rows where both are present."""
    pair = df[list(dict.fromkeys([x, y]))].dropna()
    n = len(pair)
    if n < 3 or pair[x].nunique() < 2 or pair[y].nunique() < 2:
        return float("nan"), n
    if x == y:
        return 1.0, n
    return float(pair[x].corr(pair[y], method=method)), n


def correlation_matrices(df, cols, method="pearson"):
    """Return (r matrix, n matrix) using pairwise-complete observations."""
    sub = df[cols]
    r = sub.corr(method=method)
    present = sub.notna().astype(int)
    n = present.T.dot(present)
    return r, n


def binned_means(df, x, y, bins=10):
    """Mean of x and y inside quantile bins of x, for a binned-means overlay."""
    cols = list(dict.fromkeys([x, y]))
    pair = df[cols].dropna()
    if pair[x].nunique() < 2:
        return pair.iloc[0:0]
    groups = pd.qcut(pair[x], q=min(bins, pair[x].nunique()), duplicates="drop")
    return pair.groupby(groups, observed=True)[cols].mean()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
def fmt_r(r):
    return "undefined" if pd.isna(r) else f"{r:.3f}"


def main():
    st.set_page_config(page_title="Health Correlation Explorer", layout="wide")
    st.title("Health Correlation Explorer")
    st.caption("NHANES 2017-2018 (CDC), adults aged 20 and over.")

    data = st.cache_data(load_data)(DATA_FILE)

    # ---- Sidebar: filters and method (these drive every view) -------------
    st.sidebar.header("Filters")
    sex_choice = st.sidebar.radio("Sex", ["All", "Female", "Male"])
    sexes = ["Female", "Male"] if sex_choice == "All" else [sex_choice]
    age_min, age_max = int(data["age"].min()), int(data["age"].max())
    age_range = st.sidebar.slider(
        "Age range (80 means 80 or older)", age_min, age_max, (age_min, age_max)
    )
    st.sidebar.header("Correlation method")
    method_label = st.sidebar.radio("Method", ["Pearson", "Spearman"])
    method = method_label.lower()
    st.sidebar.caption(
        "Pearson measures straight-line relationships. Spearman measures "
        "whether the two variables rise and fall together, even if not in a "
        "straight line."
    )

    df = filter_data(data, sexes, age_range)
    st.sidebar.markdown(f"**Participants after filters: {len(df):,}**")

    if df.empty:
        st.warning("No participants match these filters. Widen the filters.")
        st.stop()

    st.info(
        "These correlations describe **this sample**, not the US population. "
        "NHANES oversamples some groups."
    )

    tab_data, tab_pair, tab_heat = st.tabs(
        ["Data preview", "Pairwise view", "Correlation heatmap"]
    )

    # ---- 1. Data preview ---------------------------------------------------
    with tab_data:
        st.subheader("Data preview")
        st.write(
            "Each row is one adult from the CDC's 2017-2018 National Health "
            "and Nutrition Examination Survey (NHANES). Columns are age, sex, "
            "body measures (BMI, waist), blood pressure, HbA1c, cholesterol, "
            "self-reported sleep and sitting time. Age 80 means 80 or older. "
            "The table below respects the sidebar filters."
        )
        st.caption(f"Showing {len(df):,} of {len(data):,} participants.")
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ---- 2. Pairwise view --------------------------------------------------
    with tab_pair:
        st.subheader("Pairwise view")
        c1, c2, c3 = st.columns(3)
        x = c1.selectbox(
            "X variable", NUMERIC_COLS, index=NUMERIC_COLS.index("age"),
            format_func=LABELS.get,
        )
        y = c2.selectbox(
            "Y variable", NUMERIC_COLS, index=NUMERIC_COLS.index("systolic_bp"),
            format_func=LABELS.get,
        )
        overlay = c3.selectbox("Overlay", ["Trend line", "Binned means", "None"])
        color_choice = st.selectbox(
            "Color points by health threshold", ["None"] + list(THRESHOLDS)
        )

        r, n = pair_correlation(df, x, y, method)
        m1, m2 = st.columns(2)
        m1.metric(f"{method_label} r", fmt_r(r))
        m2.metric("n (participants)", f"{n:,}")
        if pd.isna(r):
            st.warning("r is undefined here: too few participants or no spread.")
        elif abs(r) < 0.1:
            st.warning(
                "r is near zero. That does not mean there is no relationship: "
                "a U-shaped or curved pattern can give r near zero. Look at "
                "the plot."
            )

        fig, ax = plt.subplots(figsize=(8, 5))
        plot_cols = list(dict.fromkeys([x, y] + [v[0] for v in THRESHOLDS.values()]))
        plot_df = df[plot_cols].dropna(subset=list(dict.fromkeys([x, y])))
        if color_choice == "None":
            ax.scatter(plot_df[x], plot_df[y], s=14, alpha=0.4, color="#3b6ea5")
        else:
            col, cutoff = THRESHOLDS[color_choice]
            flag = plot_df[col] >= cutoff
            ax.scatter(
                plot_df.loc[~flag, x], plot_df.loc[~flag, y], s=14, alpha=0.4,
                color="#3b6ea5", label=f"Below threshold (n={int((~flag).sum()):,})",
            )
            ax.scatter(
                plot_df.loc[flag, x], plot_df.loc[flag, y], s=14, alpha=0.5,
                color="#d1495b", label=f"Meets threshold (n={int(flag.sum()):,})",
            )
            ax.legend(title=color_choice, loc="best")
        if overlay == "Trend line" and plot_df[x].nunique() > 1 and len(plot_df) > 2:
            slope, intercept = np.polyfit(plot_df[x], plot_df[y], 1)
            xs = np.array([plot_df[x].min(), plot_df[x].max()])
            ax.plot(xs, slope * xs + intercept, color="black", linewidth=2,
                    label="Linear trend")
        elif overlay == "Binned means":
            bm = binned_means(plot_df, x, y)
            if not bm.empty:
                ax.plot(bm[x], bm[y], color="black", marker="o", linewidth=2,
                        label="Binned means")
        ax.set_xlabel(LABELS[x])
        ax.set_ylabel(LABELS[y])
        ax.set_title(f"{LABELS[y]} vs {LABELS[x]}  ({method_label} r = {fmt_r(r)}, n = {n:,})")
        sns.despine(ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    # ---- 3. Correlation heatmap -------------------------------------------
    with tab_heat:
        st.subheader("Correlation heatmap")
        chosen = st.multiselect(
            "Variables to include", NUMERIC_COLS, default=NUMERIC_COLS,
            format_func=LABELS.get,
        )
        if len(chosen) < 2:
            st.warning("Pick at least two variables.")
        else:
            r_mat, n_mat = correlation_matrices(df, chosen, method)
            side = max(5, 0.8 * len(chosen))
            fig, ax = plt.subplots(figsize=(side + 1, side))
            sns.heatmap(
                r_mat, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0,
                cmap="coolwarm", square=True, ax=ax,
                cbar_kws={"label": f"{method_label} r"},
            )
            ax.set_title(f"{method_label} correlations (colors fixed from -1 to 1)")
            st.pyplot(fig)
            plt.close(fig)
            lo_n, hi_n = int(n_mat.values.min()), int(n_mat.values.max())
            if lo_n == hi_n:
                st.caption(f"Every coefficient uses n = {lo_n:,} participants.")
            else:
                st.caption(
                    f"Each coefficient uses between {lo_n:,} and {hi_n:,} "
                    "participants (see the table below)."
                )
            with st.expander("n for every pair"):
                st.dataframe(n_mat)
            st.caption(
                "The colors always run from -1 to 1, so a pale square means "
                "weak straight-line (Pearson) or rank (Spearman) association, "
                "not necessarily no relationship."
            )


if __name__ == "__main__":
    main()
