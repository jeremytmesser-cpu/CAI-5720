# Prompt log

> DRAFT written by the AI agent for Jeremy to review. Edit these into your own words before submitting, since the assignment asks for your own prompts.

## Prompt 1 (plan mode, no code)

Don't write any code yet. I want a Streamlit app, `app.py`, to explore correlations in `nhanes_health.csv`. Read the CSV first.

It needs five things:
1. A data preview.
2. A scatter plot for any two variables I pick, showing r and n, with a trend line and an option to color points by a health threshold like SBP ≥ 130.
3. A correlation heatmap where I pick the variables.
4. Sidebar filters for sex and age that change every view.
5. A Pearson/Spearman toggle that works on both the scatter plot and the heatmap.

`sex` is text, so keep it out of every correlation. The heatmap colors must run from -1 to 1, and every r needs its n next to it. Use only Python, Streamlit, pandas and seaborn, in one file.

Give me a plan first, not code. Tell me how the filters feed every view, and tell me anything that's unclear.

## Prompt 2 (approve plan, build)

The plan covers all five features. Build the app one step at a time, starting with the data and filters, and write `requirements.txt`.

<!-- Add later prompts below, for example fixes you ask for after testing the running app. -->
