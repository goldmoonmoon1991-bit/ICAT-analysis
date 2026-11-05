# ICAT key-analysis code

Version date: 2026-11-04. Five standalone R analysis packages accompanying the ICAT manuscript. Each archive contains code, English documentation, example input configurations, a dependency lockfile and the original copyright notice. Experimental data, source data, observed input matrices, result snapshots, images and plotting code are excluded.

## Packages

| Code package | Manuscript panels |
|---|---|
| [Spatial profile quantification](01_spatial_profiles_20261104_code_only.zip) | Fig. 1b,e,f; Fig. 2e,f; Extended Data Fig. 1d |
| [Proteomic screening and interaction comparison](02_proteomics_20261104_code_only.zip) | Fig. 2b,c; Fig. 3e candidate; Extended Data Fig. 2d and 5f |
| [Localization perturbation and Gower–PCoA](03_localization_pcoa_20261104_code_only.zip) | Fig. 3b; Extended Data Fig. 3b |
| [MCI and positional-class association](04_mci_classes_20261104_code_only.zip) | Fig. 5d,e; Extended Data Fig. 7d |
| [Conservation and structural scoring](05_conservation_20261104_code_only.zip) | Fig. 5f; Extended Data Fig. 7e |

See [CANDIDATE_CATALOG.md](CANDIDATE_CATALOG.md) for workflow scope, external input requirements and interpretation limits. Archives are independently usable; extract only the modules you need. Each extracted package contains README.md, INPUTS.md, VALIDATION.md, SOURCE_PROVENANCE.json, renv.lock, LICENSE and a single run_analysis.R entry point.

## Setup and execution

Install R 4.5.0 and renv, then restore the selected package environment with `renv::restore(lockfile="renv.lock", prompt=FALSE)` from its extracted directory. Copy an example configuration outside the package and set the external input paths and field mappings.

```sh
Rscript /path/to/module/run_analysis.R --config /path/to/config.json --out-dir /path/to/external/results
```

Relative input paths resolve against the configuration file. Numerical outputs must be outside the code package and input locations. Missing files or required fields produce explicit errors; the code does not generate substitute observations or modify inputs. Data are distributed separately; upstream vendor exports and reference annotations are required for some tasks. See INPUTS.md for the exact schema.

## Validation and interpretation

All 25 R files passed syntax checks. Twenty external-input/task configurations, 79 numerical/consistency checks and 33 entry-point, invalid-input and workflow-handoff checks passed. Validation preserved all 349 original external input files. SHA256SUMS.txt records the checksums of the five archives. A fresh network-based dependency installation was not performed.

The construct-preference branch remains exploratory pending author confirmation of the final Fig. 3e workflow. MCI association models retain the original pooled cell-level interpretation. Existing SPM1 dual module membership and scientific scoring definitions are unchanged. The localization package pins the tested cluster 2.1.8.1 environment; the earlier full-project lockfile recorded 2.1.8.2. Details and per-module numerical comparisons are documented in VALIDATION.md.

## Rights and versioning

The original all-rights-reserved LICENSE is retained. No additional software licence or third-party data redistribution permission is asserted. This code-only version supersedes the earlier full snapshot in the current branch. Git commit history remains available for provenance.
