# Claim 3 method

The verifier constructs \(f(x,y)=xy\), checks both real eigenvalue parts and
the discrete bound are zero, then corroborates the certificate on 36
beta/rho/step-size combinations. The result-only checker rejects a perturbed
negative-control spectrum with nonzero real parts.

Raw output is in `../release/raw/baseline_verdict.json`.
