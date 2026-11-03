# ICAT manuscript analysis code

Snapshot date: 2026-11-02. Custom R and Python analyses accompanying the ICAT manuscript. Main figures are Fig. 1–5 and Extended Data Fig. 1–7. Historical directory names Fig5 and Fig6 do not correspond directly to the final figure numbering; see CODE_MAP.tsv.

## Download and setup

When distributed on GitHub, download and extract ICAT-analysis-20261102.zip. Keep the directory layout intact. The archive contains the analysis scripts, an R dependency lockfile, numeric inputs and tabular output snapshots. It does not contain raw microscopy, raw mass spectrometry or uncropped western blots.

From the extracted project root, install R and restore the R environment with `renv::restore()` (or install renv first if needed). Original R package versions are recorded in renv.lock. Optional Python components require the packages in requirements.txt; the original project did not supply a Python version lock.

## Analysis entry points

See CODE_MAP.tsv. Run individual scripts from their original relative locations, for example `Rscript --vanilla Fig5_secretion_mechanism/03_code/microneme_spatial_restriction/ICATkd_MIC2_width_ratio.R`. Run the Fig1 shell entry point to rebuild group-level profiles before downstream spatial comparisons. Outputs are written inside the extracted copy.

## Reproducibility limits

This is an analysis snapshot, not a claim that every manually assembled figure can be rebuilt end to end. Some analyses need third-party annotation workbooks or original protein exports absent from this release. Existing processed tables are included as seeds for downstream plots. INPUT_MANIFEST.tsv identifies included numeric inputs; the source-data package provides panel mapping and provenance.

The N/C bait heatmap workflow retains its original exploratory filename because it is a candidate for the final Fig. 3e. Confirm the final heatmap version before treating this as a frozen publication release. Legacy per-figure run_all scripts are preserved only for context; they do not cover every final panel. Fig3's legacy runner contains an incorrect optional PLA subpath; use the script under spatial_relationship directly. The original Fig2 runner also omits its peak-profile analyses.

Publication checks still outstanding: final Fig. 2f cell selection, Fig. 5f figure/legend agreement, ED6 panel numbering and ED7c statistical comparison. These are reported in the attachment audit rather than silently corrected here. The Fig. 3d value is 33.344 ± 13.077 nm after expansion correction, consistent with 33 ± 13 nm in the legend. Fig. 5e bin counts 43/51, 28/51 and 4/51 match the supplied figure.

## Rights and external data

The project's existing all-rights-reserved LICENSE is preserved. No new open-source licence or third-party redistribution permission is asserted. Public code access does not by itself grant an additional software licence. Third-party resources should be obtained from their original cited sources. The reused PXD039434 identifier must not be substituted for the accession for newly generated proteomics.

## Additional numeric exports

Run `python export_submission_tables.py` to export the invasion and egress numerical tables and the paired abundance test stated in the legend. This helper requires Rscript on PATH, plus Python numpy and pandas. It invokes base R t.test for consistency with the original R scripts. Derived tables are written to submission_tables/ and do not change raw inputs. The archived legacy ratio-based abundance tests remain separate.

The Python LFQ pipeline under shared/dda_lfq_pipeline is optional and requires its original external FragPipe inputs. Orthology/network refresh scripts retain their original external-data requirements.
