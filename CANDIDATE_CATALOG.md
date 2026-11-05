# Analysis code catalog

Version date: 2026-11-04. Five independently usable code-only analysis modules.

Each ZIP archive contains a standalone module directory. Packages contain code, documentation, configuration examples and environment metadata. Experimental data, source data, numerical output snapshots, images and plotting code are excluded. Validation inputs and outputs are kept outside the packages.

| Module | Retained analysis | Manuscript panels | External inputs | Status and selection notes |
|---|---|---|---|---|
|[Spatial profile quantification](01_spatial_profiles_20261104_code_only.zip)|Background correction, smoothing, peak detection, alignment, widths and distances|Fig. 1b,e,f; Fig. 2e,f; Extended Data Fig. 1d|Original ZEN profiles, or external peak measurements and normalized profiles|Execution and numerical comparisons passed. Custom spatial quantification; both source-specific engines retained.|
|[Proteomic screening and interaction comparison](02_proteomics_20261104_code_only.zip)|CF5 screening, enrichment statistics, full-length/N-terminal comparison and numerical QC|Fig. 2b,c; Fig. 3e candidate; Extended Data Fig. 2d and 5f|Vendor exports, sample maps, external annotations and diagnostic tables|Execution and numerical comparisons passed. Tasks can be selected individually. Construct preference remains exploratory pending final author selection.|
|[Localization perturbation and Gower–PCoA](03_localization_pcoa_20261104_code_only.zip)|Status encoding, proportions, Gower distances, clustering and PCoA|Fig. 3b; Extended Data Fig. 3b|Localization workbook/CSV; current Fig. 3b source-data format supported|Execution and numerical comparisons passed. Fixed original genotype cohort and missing-status rules retained.|
|[MCI and positional-class association](04_mci_classes_20261104_code_only.zip)|MCI, cell matching, bins, effect sizes, association models and cumulative distributions|Fig. 5d,e; Extended Data Fig. 7d|Cell-level MCI and positional classes; current Fig. 5d source-data format supported|Execution and numerical comparisons passed. Pooled cell-level models retain their exploratory interpretation.|
|[Conservation and structural scoring](05_conservation_20261104_code_only.zip)|Genus-level presence, module summaries, weighted scores and correlations|Fig. 5f; Extended Data Fig. 7e|Orthogroup presence, module membership and morphology; current Fig. 5f source-data format supported|Execution and numerical comparisons passed. Existing SPM1 dual membership and scoring definitions retained.|

## Selection and execution

- Select the ZIP archive for each desired module. Every extracted package is self-contained and does not require code from another module directory.
- README.md describes the workflow; INPUTS.md defines external inputs; VALIDATION.md records checks and limitations.
- Copy an example configuration outside the package, set external input paths, and run `Rscript /path/to/module/run_analysis.R --config /path/to/config.json --out-dir /path/to/external/results`.
- Source data are distributed separately. Configurations refer to external files without copying them. Some tasks require upstream vendor exports or reference annotations; final-panel summary workbooks alone cannot replace these inputs. See each INPUTS.md.
- Construct-preference analysis remains exploratory. Select the final workflow and version before updating a repository deposit or manuscript Code availability statement. The exploratory interpretation remains explicit in this code version.

## Validation summary

- All 25 R files passed syntax checks; 20 external-input/task configurations ran successfully; 79 numerical/consistency checks and 33 entry-point, invalid-input and workflow-handoff checks passed.
- Comparisons cover approximately 240,000 rows of original numerical exports and more than 1.16 million numerical fields, with separate checks of statistics, selections, missingness and sample identifiers.
- Current MCI source data (153 cells), localization source data and conservation source data were exercised through their respective entry points.
- Validation fixtures, reference results and generated outputs are excluded from the ZIP archives. All 349 external input files retained their pre-run SHA-256 hashes.
- Installed dependency versions were checked. A fresh network-based environment installation was not performed.

The earlier full snapshot has been superseded in the current branch. Original copyright notices are retained.
