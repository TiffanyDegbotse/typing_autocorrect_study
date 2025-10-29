import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.formula.api import ols
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================
# SETUP
# ==========================
ROOT = Path(__file__).resolve().parents[1]
RAW = sorted((ROOT / "data" / "raw").glob("typing_study_trials_Tiffany*.csv"))
if not RAW:
    raise SystemExit("No raw CSV found in data/raw/. Export from the HTML app first.")

df = pd.read_csv(RAW[-1])  # latest run
for col in ["ms", "wpm", "cer", "backspaces", "repair_ms", "trial"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================
# CLEANING
# ==========================
# Drop invalid rows but keep small groups (avoid dropping HARD/OFF)


# Skip cleaning entirely — keep all trials
clean = df.dropna(subset=["condition", "prompt_type", "wpm", "cer", "ms"]).copy()



clean_dir = ROOT / "data" / "clean"
clean_dir.mkdir(parents=True, exist_ok=True)
clean_path = clean_dir / "typing_clean.csv"
clean.to_csv(clean_path, index=False)

# ==========================
# SUMMARY COUNTS
# ==========================
counts = clean.groupby(["prompt_type", "condition"]).size().unstack()
print(f"[ok] Cleaned data saved -> {clean_path}")
print("\nCounts per cell (after cleaning):\n", counts)

# ==========================
# ANALYSIS HELPERS
# ==========================
clean["occ"] = clean.groupby(["prompt", "prompt_type", "condition"]).cumcount()

def mkwide(metric):
    wide = (
        clean.pivot_table(index=["prompt", "prompt_type", "occ"],
                          columns="condition", values=metric, aggfunc="first")
        .dropna()
    )
    return wide

def paired_stats(wide, label):
    a, b = wide["AUTO"], wide["OFF"]
    diff = a - b
    n = len(diff)
    if n < 2:
        return f"\n== {label}: insufficient pairs =="
    t, p = stats.ttest_rel(a, b)
    dz = diff.mean() / (diff.std(ddof=1) + 1e-12)
    se = diff.std(ddof=1) / np.sqrt(n)
    ci = stats.t.interval(0.95, n - 1, loc=diff.mean(), scale=se)
    return (
        f"\n== {label} (AUTO - OFF) overall ==\n"
        f"n={n}, mean_auto={a.mean():.3f}, mean_off={b.mean():.3f}\n"
        f"mean_diff={diff.mean():.3f}, t={t:.3f}, p={p:.4f}, "
        f"dz={dz:.3f}, 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]"
    )

def within(ptype, wide, metric):
    sub = wide.reset_index()
    sub = sub[sub["prompt_type"] == ptype][["AUTO", "OFF"]].dropna()
    a, b = sub["AUTO"], sub["OFF"]
    if len(a) < 2:
        return f"\n== {metric} {ptype}: insufficient pairs =="
    diff = a - b
    t, p = stats.ttest_rel(a, b)
    dz = diff.mean() / (diff.std(ddof=1) + 1e-12)
    n = len(diff)
    se = diff.std(ddof=1) / np.sqrt(n)
    ci = stats.t.interval(0.95, n - 1, loc=diff.mean(), scale=se)
    return (
        f"\n== {metric} {ptype} (AUTO - OFF) ==\n"
        f"n={n}, mean_diff={diff.mean():.3f}, t={t:.3f}, "
        f"p={p:.4f}, dz={dz:.3f}, CI [{ci[0]:.3f}, {ci[1]:.3f}]"
    )

def two_by_two_ols(metric):
    wide = mkwide(metric)
    long = wide.reset_index().melt(
        id_vars=["prompt", "prompt_type", "occ"],
        value_vars=["AUTO", "OFF"],
        var_name="condition",
        value_name=metric,
    )
    long["cond_coded"] = (long["condition"] == "AUTO").astype(int)
    long["hard_coded"] = (long["prompt_type"] == "HARD").astype(int)
    long["interaction"] = long["cond_coded"] * long["hard_coded"]
    model = ols(f"{metric} ~ cond_coded + hard_coded + interaction", data=long).fit()
    means = long.groupby(["prompt_type", "condition"])[metric].mean().unstack()
    return model, means.round(3)

# ==========================
# RUN ANALYSES
# ==========================
wide_wpm, wide_cer = mkwide("wpm"), mkwide("cer")

results_text = []
results_text.append(paired_stats(wide_wpm, "WPM"))
results_text.append(paired_stats(wide_cer, "CER"))

for metric, wide in [("WPM", wide_wpm), ("CER", wide_cer)]:
    for ptype in ["EASY", "HARD"]:
        results_text.append(within(ptype, wide, metric))

for metric in ["wpm", "cer"]:
    model, means = two_by_two_ols(metric)
    results_text.append(f"\n=== OLS 2×2 ({metric}) ===\n" + str(model.summary()))
    results_text.append("\nCell means:\n" + str(means))

# ==========================
# SAVE RESULTS
# ==========================
out_path = ROOT / "data" / "clean" / "typing_results.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(results_text))
print(f"\n[ok] Statistical results saved -> {out_path}")

# ==========================
# PLOTS
# ==========================
fig_dir = ROOT / "figures"
fig_dir.mkdir(exist_ok=True)

plt.figure()
clean.boxplot(column="wpm", by=["prompt_type", "condition"])
plt.suptitle("")
plt.title("WPM by Difficulty × Condition")
plt.ylabel("WPM")
plt.tight_layout()
plt.savefig(fig_dir / "wpm_box.png", dpi=200)

plt.figure()
clean.boxplot(column="cer", by=["prompt_type", "condition"])
plt.suptitle("")
plt.title("CER by Difficulty × Condition (lower is better)")
plt.ylabel("CER")
plt.tight_layout()
plt.savefig(fig_dir / "cer_box.png", dpi=200)

plt.figure()
means = clean.groupby(["prompt_type", "condition"])["wpm"].mean().unstack()
means.plot(kind="bar")
plt.ylabel("Mean WPM")
plt.title("Mean WPM by Cell")
plt.tight_layout()
plt.savefig(fig_dir / "wpm_bar.png", dpi=200)

print(f"[ok] Figures saved -> {fig_dir}")
print(f"[ok] Results written to -> {out_path}")
