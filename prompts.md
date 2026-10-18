# Prompt log

> DRAFT written by the AI agent for Jeremy to review. Edit these into your own words before submitting, since the assignment asks for your own prompts.

## Prompt 1 (plan mode, no code)

Don't write any code yet. I want to build a Streamlit app, `app.py`, that explores correlations between health measures in `nhanes_health.csv`. Read the CSV first. The app needs five things: a data preview (short description and a table of the rows); a pairwise view where two dropdowns pick X and Y and the app shows a scatter plot, the correlation r and the number of participants n, with a trend line or binned means and an option to color points by a health threshold such as SBP ≥ 130; a correlation heatmap where the user picks which numeric variables to include, every square shows its coefficient, and the color scale is fixed from -1 to 1; sidebar filters for sex and an age range that update every view (table, scatter plot, r, n and heatmap); and a toggle between Pearson and Spearman that applies to both the pairwise view and the heatmap.

Every column is numeric except `sex`, which must never go into any correlation. Compute every r on rows where both variables are present and show n next to every r. The heatmap colors must run from -1 to 1 so it stays honest. Remind the user that an r near zero does not mean no relationship.

Use Python, Streamlit, pandas and seaborn (or plotly), in one file called `app.py`. Don't add other packages without asking. Please give me a plan, not code: the build order, how the filters feed every view, the command to run the app, and anything in my request that is unclear.

## Prompt 2 (approve plan, build)

The plan covers all five features. Build the app one step at a time, starting with the data and filters, and write `requirements.txt`.

<!-- Add later prompts below, for example fixes you ask for after testing the running app. -->
