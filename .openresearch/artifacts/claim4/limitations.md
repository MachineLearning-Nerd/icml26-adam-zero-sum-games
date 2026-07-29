# Claim 4 limitations and deviations

- Section 5 states an experimentally supported thesis, not a universally
  quantified theorem. The result is direct scoped corroboration.
- This route uses an analytic two-dimensional interaction-dominated game, not
  GAN networks. Claim 5 separately audits the paper's GAN evidence.
- Step sizes differ between the beta and rho sweeps, but remain fixed within
  each causal comparison. This avoids changing the named momentum parameter
  and stability scale simultaneously.
- The eight deterministic starts quantify trajectory variation; they are not
  random samples from a population.
- The published rho grid ends at 0.9. The frozen parent shows that the trend
  reverses at 0.95 and 0.99 in this quadratic game, so this evidence must not
  be extrapolated to every rho in `(0,1)`.
