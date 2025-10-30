# power_paired.py
from statsmodels.stats.power import TTestPower
import numpy as np
import matplotlib.pyplot as plt

# Initialize power analysis for paired t-test
power_analysis = TTestPower()

# Parameters
alpha = 0.05
target_power = 0.80
dz = 0.25  # assumed small within-subject effect size

# Solve required sample size (paired prompts)
n_required = power_analysis.solve_power(effect_size=dz, alpha=alpha, power=target_power, alternative='two-sided')
print(f"Assumed effect size dz={dz:.2f} -> required paired prompts ≈ {n_required:.1f} (≈ {int(n_required*2)} trials total)")

# Optional: visualize how power changes with sample size
sample_sizes = np.arange(20, 300, 5)
powers = [power_analysis.power(effect_size=dz, nobs=n, alpha=alpha, alternative='two-sided') for n in sample_sizes]

plt.plot(sample_sizes, powers, label=f'dz={dz:.2f}')
plt.axhline(target_power, color='red', linestyle='--', label='Target Power=0.80')
plt.xlabel('Number of Paired Prompts')
plt.ylabel('Statistical Power')
plt.title('Power Curve for Paired t-test (Autocorrect Effect)')
plt.legend()
plt.tight_layout()
plt.show()
