# typing_autocorrect_study
# Typing Autocorrect Study (Desktop): 2×2 Within-Subject

**Design:** Autocorrect (ON/OFF) × Prompt Difficulty (EASY/HARD)  
**Outcomes:** Words per minute (WPM), Character error rate (CER)  
**Scope:** Single participant, many trials (balanced across 4 cells)


## Quick Start

### 1) Prepare prompts
Edit `data/prompts_easy.txt` and `data/prompts_hard.txt` to your liking.

### 2) Collect data
- Open `collect/index.html` in a desktop browser.
- Enter Participant ID, choose target per cell (e.g., 50), and practice count.
- Complete all trials. Click **Download CSV** and save to `data/raw/typing_study_trials_<PID>.csv`.

### 3) Power analysis (optional first)
-cd analyze
-pip install -r requirements.txt
-python power_paired.py

### 4) Clean & analyze
-python clean_and_analyze.py

Outputs:
-Cleaned CSV: data/clean/typing_clean.csv
-Figures: figures/wpm_box.png, figures/cer_box.png, figures/wpm_bar.png

-Console prints: paired test stats, interaction OLS summary

### 5) Reproduce
-Ensure the raw CSV is present in data/raw/.
-Run python analyze/clean_and_analyze.py on a fresh environment to reproduce all stats & figures.

Methods Summary
-Design: 2×2 within-subject; balanced trials across four cells.

-Randomization: Trial order shuffled; practice block before main trials.

-Metrics: WPM = (chars/5)/minutes; CER = Levenshtein(truth,typed)/len(truth); repair_ms = time from first backspace to submit (exploratory).

-Stats: Paired t-tests overall & within difficulty; Cohen’s dz + 95% CI; OLS model for interaction (condition × difficulty).







