# Claim 6 limitations and deviations

- This is a direct numerical order check, not a formal proof certificate.
- It covers one analytic bounded-derivative loss, four initial points, one
  `(beta, rho, epsilon)` triple, and seven step sizes.
- RK4 with 128 substeps is used as a high-accuracy reference integrator;
  integration error is designed to be negligible relative to the measured
  `h^3` residual.
- The paper does not publish executable reference code, so both the discrete
  update and continuous vector field were independently transcribed from the
  displayed equations and audited against the TeX source.
