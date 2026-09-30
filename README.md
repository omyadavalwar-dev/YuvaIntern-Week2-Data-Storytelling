# YuvaIntern Week 2 — Advanced Data Visualization and Storytelling

## Main submission

Upload `YuvaIntern_Week2_Report.docx` to the Week 2 report field. Paste `submission_description.txt` into the description box. Upload this folder's contents to your GitHub project and paste that project's URL into the portal.

## Run

Tested with Python 3.12.14. From this folder:

```sh
python -m pip install -r requirements.txt
python analysis.py
```

The script resolves paths relative to itself. For Jupyter, install Jupyter separately and open `analysis.ipynb` from this folder; run all cells. Notebook outputs start empty. The analysis script was executed successfully to create the included outputs. Running it regenerates figures and CSV tables, not the Word report.

## Five visualizations

1. Annotated species-by-island count heatmap.
2. Cumulative body-mass distributions by species.
3. Sex comparison with box plots and individual points, faceted by species.
4. Flipper–mass scatter plots with descriptive fits and correlations within species.
5. Annual median body mass with sample-size annotations.

`charts/` holds PNGs, `data/` holds source and cleaned CSVs, and `tables/` holds numerical summaries and audit metadata. The analysis uses 342 measurement-complete records, or 333 known-sex records for the sex comparison. Random jitter uses seed 42 and affects display only.

## Source

Horst AM, Hill AP, Gorman KB (2020), palmerpenguins. Data collected by Kristen Gorman and Palmer Station LTER; distributed under CC0.

- Documentation: https://allisonhorst.github.io/palmerpenguins/
- CSV: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv
- Snapshot downloaded on 30 September 2026 for Week 1 and reused here; checksum in `tables/audit.json`.

The local file `penguins_raw.csv` contains the simplified eight-column CSV, not the project's separate 17-column dataset.

## Submission notes

All five chart images were visually checked. The automatic DOCX renderer was unavailable, so final Word pagination remains unverified; check the DOCX layout in Word before uploading. No repository was created or uploaded automatically. The estimated 30–35 hour workload in the task PDF is not a claim of actual time spent.
