# Prompt log

## Prompt 1 (plan, no code)
Don't write code yet. Read `nhanes_health.csv`, then plan a Streamlit app, `app.py`, with: a data preview, a scatter plot with r and n for any two variables, a correlation heatmap, sidebar filters for sex and age, and a Pearson/Spearman toggle. Keep `sex` out of every correlation, run the heatmap colors from -1 to 1, and show n next to every r. Tell me how the filters feed every view and what is unclear.

## Prompt 2 (build)
The plan is good. Build it one step at a time, starting with the data and filters, and write `requirements.txt`.

## Prompt 3 (fix)
The scatter plot crashed on the deployed app with "x and y must be the same size". Find the cause and fix it.
