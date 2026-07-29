# Claim 5 source audit

The source audit is executable in `claim5_source_audit.py` and independently
checked by `check_claim5_route1.py`.

The paper discloses the datasets, image sizes, broad architecture families,
learning rate, batch size, momentum comparisons, cumulative gradient metric,
and aggregate Inception Scores. It says the setup “generally follows” improved
WGAN rather than identifying a fixed implementation.

It does not disclose executable author code; exact ResNet/CNN definitions;
preprocessing and splits; latent distribution; critic schedule; gradient
penalty coefficient; Adam epsilon; seeds; main experiment horizon; IS
implementation/sample count; raw gradient curves; or per-seed IS values.

These omissions prevent a unique full-scale reproduction from source alone.
