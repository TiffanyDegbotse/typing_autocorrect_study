import pandas as pd, numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = sorted((ROOT/"data"/"raw").glob("typing_study_trials*.csv"))
if not RAW:
    raise SystemExit("No raw CSV found in data/raw/. Export from the HTML app first.")
df = pd.read_csv(RAW[-1])  # latest run

# Basic types
for col in ["ms","wpm","cer","backspaces","repair_ms","trial"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Clean: drop time or WPM or CER with >3 SD from mean (by condition×difficulty to be fair)
def zcut(sub):
    z = np.abs(stats.zscore(sub[['ms','wpm','cer']], nan_policy='omit'))
    keep = (z < 3).all(axis=1)
    return sub[keep]

clean = (df
         .dropna(subset=['condition','prompt_type','wpm','cer','ms'])
         .groupby(['condition','prompt_type'], group_keys=False)
         .apply(zcut)
         .copy())

# Save cleaned data
ROOT.joinpath("data","clean").mkdir(parents=True, exist_ok=True)
clean_path = ROOT/"data"/"clean"/"typing_clean.csv"
clean.to_csv(clean_path, index=False)
print(f"[ok] Cleaned data saved -> {clean_path}")

# Check balance
counts = clean.groupby(['prompt_type','condition']).size().unstack()
print("\nCounts per cell (after cleaning):\n", counts)

# Pivot to wide by prompt occurrence (align AUTO/OFF pairs within each difficulty)
clean['occ'] = clean.groupby(['prompt','prompt_type','condition']).cumcount()
def mkwide(metric):
    wide = (clean
            .pivot_table(index=['prompt','prompt_type','occ'], columns='condition', values=metric, aggfunc='first')
            .dropna())
    return wide

wide_wpm = mkwide('wpm')
wide_cer = mkwide('cer')

def paired_stats(wide, label):
    a = wide['AUTO'].astype(float); b = wide['OFF'].astype(float)
    diff = a - b
    t,p = stats.ttest_rel(a, b)
    dz = diff.mean() / (diff.std(ddof=1) + 1e-12)
    n = diff.count()
    se = diff.std(ddof=1)/np.sqrt(n)
    ci = stats.t.interval(0.95, n-1, loc=diff.mean(), scale=se)
    print(f"\n== {label} (AUTO - OFF) overall ==")
    print(f"n={n}, mean_auto={a.mean():.3f}, mean_off={b.mean():.3f}")
    print(f"mean_diff={diff.mean():.3f}, t={t:.3f}, p={p:.4f}, dz={dz:.3f}, 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]")
    return {"n":n, "mean_auto":a.mean(), "mean_off":b.mean(), "mean_diff":diff.mean(),
            "t":t, "p":p, "dz":dz, "ci":ci}

# Overall paired comparisons
res_wpm = paired_stats(pd.concat([wide_wpm], axis=1), "WPM")
res_cer = paired_stats(pd.concat([wide_cer], axis=1), "CER")

# Within EASY and HARD
def within(ptype, wide):
    sub = wide.reset_index()
    sub = sub[sub['prompt_type']==ptype].set_index(['prompt','prompt_type','occ'])
    sub = sub[['AUTO','OFF']].dropna()
    return sub

for metric, ww in [("WPM", wide_wpm), ("CER", wide_cer)]:
    for ptype in ['EASY','HARD']:
        sub = within(ptype, ww)
        a = sub['AUTO']; b = sub['OFF']; diff = a-b
        if len(diff) < 2: 
            print(f"\n== {metric} {ptype} has insufficient pairs =="); 
            continue
        t,p = stats.ttest_rel(a,b)
        dz = diff.mean()/(diff.std(ddof=1)+1e-12)
        n = len(diff); se = diff.std(ddof=1)/np.sqrt(n)
        ci = stats.t.interval(0.95, n-1, loc=diff.mean(), scale=se)
        print(f"\n== {metric} {ptype} (AUTO - OFF) ==")
        print(f"n={n}, mean_diff={diff.mean():.3f}, t={t:.3f}, p={p:.4f}, dz={dz:.3f}, CI [{ci[0]:.3f},{ci[1]:.3f}]")

# 2×2 OLS for interaction (within-participant prompt occurrences)
def two_by_two_ols(metric):
    wide = mkwide(metric)
    long = wide.reset_index().melt(id_vars=['prompt','prompt_type','occ'], value_vars=['AUTO','OFF'],
                                   var_name='condition', value_name=metric)
    long['cond_coded'] = (long['condition']=='AUTO').astype(int)
    long['hard_coded'] = (long['prompt_type']=='HARD').astype(int)
    long['interaction'] = long['cond_coded']*long['hard_coded']
    model = ols(f"{metric} ~ cond_coded + hard_coded + interaction", data=long).fit()
    print(f"\n=== OLS 2×2 ({metric}) ===")
    print(model.summary())
    means = long.groupby(['prompt_type','condition'])[metric].mean().unstack()
    print("\nCell means:\n", means.round(3))
    return means

means_wpm = two_by_two_ols('wpm')
means_cer = two_by_two_ols('cer')

# Plots
ROOT.joinpath("figures").mkdir(exist_ok=True)
plt.figure()
clean.boxplot(column='wpm', by=['prompt_type','condition'])
plt.suptitle(""); plt.title("WPM by Difficulty × Condition")
plt.ylabel("WPM")
plt.tight_layout()
plt.savefig(ROOT/"figures"/"wpm_box.png", dpi=200)

plt.figure()
clean.boxplot(column='cer', by=['prompt_type','condition'])
plt.suptitle(""); plt.title("CER by Difficulty × Condition (lower is better)")
plt.ylabel("CER")
plt.tight_layout()
plt.savefig(ROOT/"figures"/"cer_box.png", dpi=200)

plt.figure()
means = means_wpm.stack().reset_index()
pivot = means.pivot(index='prompt_type', columns='condition', values=0)
pivot.plot(kind='bar')
plt.ylabel("Mean WPM"); plt.title("Mean WPM by cell")
plt.tight_layout()
plt.savefig(ROOT/"figures"/"wpm_bar.png", dpi=200)

print("\n[ok] Figures saved -> figures/wpm_box.png, figures/cer_box.png, figures/wpm_bar.png")
print("\nPaste the printed stats into your report's Results section.")
