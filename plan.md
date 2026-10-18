# Plan: Health Correlation Explorer (`app.py`)

## Goal
One Streamlit file, `app.py`, that explores correlations in `nhanes_health.csv` (4,433 adults, NHANES 2017-2018).

## Data rules
- Numeric columns: age, bmi, waist_cm, systolic_bp, diastolic_bp, hba1c, total_chol, hdl_chol, sleep_hours, sedentary_minutes.
- `sex` is text and is never offered in any correlation. It is used only as a filter.
- The file has no missing values, but every r is still computed on rows where both variables are present, and n is reported next to it.

## Build order
1. Load the CSV (relative path `nhanes_health.csv`), cached.
2. Sidebar filters: sex (All / Female / Male) and an age range slider. Both produce one filtered DataFrame that every view reads.
3. Correlation method toggle (Pearson / Spearman) in the sidebar.
4. Data preview tab: short description plus the filtered table.
5. Pairwise tab: X and Y dropdowns, scatter plot, r, n, an overlay (trend line, binned means or none), and an option to color points by a health threshold (SBP ≥ 130, DBP ≥ 80, BMI ≥ 30, HbA1c ≥ 6.5, total cholesterol ≥ 240).
6. Heatmap tab: multiselect of numeric variables, a coefficient in every square, colors fixed from -1 to 1, and n shown below with a per-pair table.
7. Warnings: r near zero does not mean no relationship; correlations describe this sample, not the US population.

## How the filters reach every view
`filter_data(data, sexes, age_range)` runs once at the top. The table, scatter plot, r, n and heatmap all use that same filtered DataFrame.

## Number rules
- r and n come from the filtered data in every view.
- Heatmap uses `vmin=-1`, `vmax=1`, centered at 0.
- Spearman is computed by pandas (`method="spearman"`, needs scipy).

## Constraints
Python, Streamlit, pandas, seaborn/matplotlib, numpy, scipy. One file. No other packages.

## Run command
`uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py`

## Open questions
- Age 80 means "80 or older" in this dataset, so the top of the age range is a pooled group.
