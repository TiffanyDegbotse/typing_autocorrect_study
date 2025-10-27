# Title: Does Autocorrect Help More on Hard Prompts? A 2×2 Within-Subject Desktop Typing Study

## Abstract
We evaluate whether autocorrect improves desktop typing performance and whether its effect depends on prompt difficulty. In a within-subject 2×2 design (Autocorrect: ON/OFF × Prompt Difficulty: EASY/HARD), a single participant completed N trials per cell (total T trials). Primary outcomes were words per minute (WPM) and character error rate (CER). Autocorrect [increased/decreased/no change in] WPM by Δ (dz=…, 95% CI …, p=…). For CER, autocorrect [reduced/raised/no change] errors by Δ (dz=…, 95% CI …, p=…). We also tested the interaction between autocorrect and difficulty; the interaction was [present/absent] (β_int=…, p=…). Findings suggest that [practical takeaway].  

## 1. Background & Motivation
Prior work on predictive/autocorrect features shows mixed effects on speed and errors, often in **mobile** contexts. Few controlled studies vary **prompt difficulty**. We address this gap on **desktop** with short, fixed prompts and a factorial design. We hypothesize that autocorrect offers larger benefits on **hard** prompts (rare/irregular words).

## 2. Hypotheses
- **H0 (Speed):** μ_WPM(AUTO) = μ_WPM(OFF)
- **H1 (Speed):** μ_WPM(AUTO) > μ_WPM(OFF)
- **H0 (Accuracy):** μ_CER(AUTO) = μ_CER(OFF)
- **H1 (Accuracy):** μ_CER(AUTO) < μ_CER(OFF)
- **Exploratory Interaction:** The effect of autocorrect differs by prompt difficulty (EASY vs HARD).

## 3. Experimental Design
- **Design:** Within-subject; factors: {Autocorrect: ON/OFF} × {Prompt Difficulty: EASY/HARD}.
- **Participant:** Single participant (desktop physical keyboard); inference generalizes over **prompts** for this participant.
- **Stimuli:** Short prompts (EASY: common words; HARD: rare or irregular spellings). Each cell had N trials (balanced).
- **Randomization:** Trials were randomized; equal counts per cell; short practice block preceded the experiment.
- **DVs:** WPM = (chars/5)/minutes; CER = Levenshtein(truth, typed)/len(truth); repair_ms = time from first backspace to Enter (exploratory).
- **Controls:** Same device, environment, and app-based autocorrect; breaks to mitigate fatigue.

## 4. Power Analysis
We assumed a **small** within-subject effect (dz ≈ 0.25) for WPM and planned for ~100 paired prompts total (≈200 trials), evenly split across EASY/HARD. `statsmodels` power calculations indicated ~n=100 pairs for 80% power at α=0.05. We collected [X] pairs ([T] trials). (Include the printed output from `power_paired.py`.)

## 5. Data Collection & Cleaning
- **App:** Custom desktop web app with toggled autocorrect and balanced 2×2 schedule.
- **Logging:** condition, prompt_type, prompt, typed, ms, wpm, cer, backspaces, repair_ms, trial.
- **Cleaning:** Within cell, removed trials with |z|>3 on {ms,wpm,cer}; final counts per cell: (paste table from script).
- **Exclusions:** [describe any skipped/paused trials].

## 6. Statistical Analysis
- **Primary:** Paired t-tests (AUTO vs OFF) for WPM and CER over all prompts; paired tests within EASY and within HARD.
- **Effect Sizes:** Cohen’s dz with 95% CIs.
- **Assumptions Check:** Visual QQ on paired differences; if non-normal, report Wilcoxon as robustness.
- **Interaction:** OLS with coded factors (cond, difficulty, cond×difficulty) on prompt occurrences.

## 7. Results
- **Overall AUTOCORRECT Effect (WPM):** (paste `== WPM (AUTO - OFF) overall ==` block)
- **Overall AUTOCORRECT Effect (CER):** (paste CER block)
- **Within EASY/HARD simple effects:** (paste each)
- **Interaction OLS:** (paste model coefficient table summary; report β, p for interaction)
- **Figures:** Include `figures/wpm_box.png`, `figures/cer_box.png`, `figures/wpm_bar.png`.

## 8. Interpretation
Summarize whether autocorrect meaningfully improved speed/accuracy overall and whether the benefit depends on difficulty. Discuss practical magnitude (e.g., +2 WPM may or may not matter for short prompts).

## 9. Limitations
Single participant; desktop app autocorrect differs from OS/phone keyboards; short prompts (not long-form writing); learned prompts over time possible.

## 10. Conclusion & Recommendations
State actionable takeaways (e.g., enable autocorrect for hard words if it reduced CER without slowing WPM; or caution when prompts are easy if no benefit).

## References
[List 3–5 sources you cite; include URLs/DOIs in report/references.txt]
