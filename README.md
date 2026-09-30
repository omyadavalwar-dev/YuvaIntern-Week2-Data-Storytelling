# YuvaIntern Week 2 — Advanced Data Visualization and Storytelling

## Download and run

Download and extract `YuvaIntern_Week2_Complete_Package.zip` before running the analysis. The archive contains all 18 project files, including the required `data/`, `charts/` and `tables/` folders, the report and the submission description. The loose Python and notebook files in this repository are provided for convenient code review.

From the extracted package folder, using Python 3.12:

```sh
python -m pip install -r requirements.txt
python analysis.py
```

For Jupyter, install Jupyter separately, open `analysis.ipynb` from the extracted folder, and run all cells. Notebook outputs start empty. The Python script was executed successfully to generate the supplied figures and tables. It regenerates data and charts, not the Word report.

## Report and five visualizations

The main report is `YuvaIntern_Week2_Report.docx`. It includes methods, captions, visual-selection rationale, insights, limitations and scientific implications.

1. Species-by-island count heatmap.
2. Cumulative body-mass distributions.
3. Sex comparison using box plots and individual points.
4. Within-species flipper–mass relationships.
5. Annual median body mass with sample sizes.

The analysis retains 342 measurement-complete records; the sex comparison uses 333 records with known sex. Display jitter uses seed 42.

## Data source

Horst AM, Hill AP, Gorman KB (2020), palmerpenguins. Data collected by Kristen Gorman and Palmer Station LTER; distributed under CC0.

Documentation: https://allisonhorst.github.io/palmerpenguins/

Source CSV: https://raw.githubusercontent.com/allisonhorst/palmerpenguins/main/inst/extdata/penguins.csv

The source snapshot was downloaded on 30 September 2026 and reused from Week 1. Its checksum is in `tables/audit.json` inside the package. The local `penguins_raw.csv` is the simplified eight-column dataset.

## Validation

Code execution, five embedded figures, notebook syntax, subgroup counts and archive integrity were checked. All five chart images were visually inspected. Automatic DOCX rendering was unavailable, so final Word pagination remains unverified. The internship workload estimate is not a claim of hours worked.
