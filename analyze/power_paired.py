from statsmodels.stats.power import TTestPower

# Assume small effect (dz ~ 0.27) for the main effect of AUTOCORRECT (within-subject)
power = TTestPower()
dz=0.27
n = power.solve_power(effect_size=dz, alpha=0.05, power=0.80, alternative='two-sided')
print(f"dz={dz:.2f} -> required paired n (prompts per condition): ~{n:.1f}")


