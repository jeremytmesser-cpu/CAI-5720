# Verification

"App shows" was read from the deployed app (Pearson, age range 20-80). "pandas gives" was computed independently with the snippet in the code check below.

| # | Check | App shows | pandas gives | Match? |
|---|---|---|---|---|
| 1 | r for `age` vs `systolic_bp`, all participants | r = 0.463 (n = 4,433) | r = 0.4627 (n = 4,433) | Yes |
| 2 | r for `bmi` vs `waist_cm`, all participants | r = 0.903 (n = 4,433) | r = 0.9026 (n = 4,433) | Yes |
| 3 | r for `waist_cm` vs `hdl_chol`, all participants | r = -0.335 (n = 4,433) | r = -0.3350 (n = 4,433) | Yes |
| 4 | r and n for `age` vs `systolic_bp`, **Female only** | r = 0.555, n = 2,263 | r = 0.5553, n = 2,263 | Yes |
| 5 | r and n for `age` vs `systolic_bp`, **Male only** | r = 0.351, n = 2,170 | r = 0.3507, n = 2,170 | Yes |
| 6 | With the filter set to Female, does the heatmap's `age`/`systolic_bp` square match row 4? | 0.56 | 0.56 (row 4: 0.5553) | Yes |

The app rounds r to 3 decimals, the heatmap to 2, so each "App shows" value equals the pandas value after rounding.

## The M9 trap
An r near zero does not mean "no relationship". In this data, `sleep_hours` vs `systolic_bp` has r = 0.007 (n = 4,433), yet the binned means curve upward at both ends: about 129 mmHg for the shortest sleepers, about 125 mmHg around 7 to 7.5 hours, and about 129 mmHg for the longest sleepers. The straight-line r misses that U shape.

## Code check
```python
import pandas as pd
df = pd.read_csv("nhanes_health.csv")
f = df[(df["sex"] == "Female") & df["age"].between(40, 59)]
f["age"].corr(f["systolic_bp"]), len(f)   # (0.2867, 750)
```
