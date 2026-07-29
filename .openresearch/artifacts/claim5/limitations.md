# Claim 5 limitations and deviations

- Route 1 audits reproducibility; it does not train a GAN.
- Aggregate values printed in the paper are author evidence, not reproduction
  evidence.
- No missing implementation choice is silently filled with a convenient
  substitute.
- Route 3 uses synthetic batches and an explicit reference architecture only
  to calibrate CPU cost. It does not test CIFAR-10, STL-10, or Inception Score.
- A local nonmonotone pair does not falsify the paper's stated empirical
  “tendency.” Calling it FALSIFIED would silently strengthen the quantifier.
