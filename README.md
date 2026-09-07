# Aerosol Volume Distribution During Prescribed Burning Events

## Overview

This repository contains a Python workflow for processing and visualizing time-resolved particle-size distribution measurements collected during a prescribed burning event.

The workflow generates a **particle-size-resolved aerosol volume distribution heatmap**, allowing changes in the measured aerosol distribution to be examined across the monitoring period.

The analysis is designed for research applications in **aerosol science, air quality, and particulate-matter exposure assessment**.

---

## Research Objective

The primary objective is to characterize the temporal evolution of the measured aerosol particle-size distribution during prescribed burning conditions.

The visualization provides a compact representation of:

* Particle diameter as a function of time
* Temporal variability in measured particle-size concentrations
* Dominant particle-size ranges
* Changes in the aerosol distribution during smoke-impacted periods

---

## Methodology

The workflow consists of the following steps:

1. Load particle-size distribution measurements from an Excel spreadsheet.
2. Standardize particle-size column names.
3. Combine measurement date and time fields into a single datetime variable.
4. Remove records with invalid timestamps.
5. Apply the daylight-saving-time adjustment used for the 2026 monitoring dataset.
6. Extract the particle-size-resolved measurement columns.
7. Treat zero and negative values as missing values for logarithmic visualization.
8. Construct a time-resolved particle-size matrix.
9. Generate a heatmap using logarithmic particle-diameter and color normalization.
10. Format the resulting figure for research and publication use.

---

## Particle-Size Range

The workflow uses the following particle-size bins:

| Particle size | Unit |
| ------------: | :--- |
|           0.3 | µm   |
|           0.5 | µm   |
|           1.0 | µm   |
|           2.5 | µm   |
|           5.0 | µm   |
|          10.0 | µm   |

The visualization extends to an upper particle-size boundary of **25 µm**.

---

## Input Data

The current implementation expects an Excel file containing:

### Required timestamp columns

```text
#YY/MM/DD
HR:MN:SC
```

### Required particle-size columns

```text
0.3
0.5
1.0
2.5
5.0
10.0
```

The current script was developed using an Excel input file named:

```text
Book3.xlsx
```

### Data privacy

The original research dataset is **not included in this public repository**.

The repository is intended to contain the analysis workflow and documentation while protecting unpublished or restricted research data.

Users wishing to reproduce the analysis should provide their own appropriately formatted dataset.

---

## Output

The workflow produces a time-resolved aerosol volume distribution heatmap with:

* **X-axis:** Measurement date
* **Y-axis:** Particle diameter, \(D_p\), in µm
* **Color scale:** Logarithmically normalized measured distribution values
* **Y-axis scale:** Logarithmic

The resulting visualization is intended to facilitate interpretation of particle-size distributions during smoke-impacted periods.

---

## Code Structure

The repository is organized as follows:

```text
aerosol-volume-distribution/
│
├── README.md
│
├── aerosol_volume_distribution.py
│
├── requirements.txt
│
├── data/
│   └── README.md
│
└── figures/
    └── README.md
```

### `aerosol_volume_distribution.py`

Main Python workflow for:

* Loading the dataset
* Cleaning column names
* Creating timestamps
* Applying the dataset-specific time adjustment
* Preparing particle-size data
* Generating the aerosol distribution visualization

### `data/`

Placeholder directory documenting the expected input-data structure.

The original research dataset is intentionally excluded.

### `figures/`

Directory for generated figures that are appropriate for public release.

---

## Requirements

The workflow requires Python 3.x and the following packages:

```text
numpy
pandas
matplotlib
openpyxl
```

Install the dependencies using:

```bash
pip install -r requirements.txt
```

---

## Running the Analysis

1. Clone the repository:

```bash
git clone https://github.com/SHABNA123-VS/aerosol-volume-distribution.git
```

2. Place an appropriately formatted Excel dataset in the designated data location.

3. Update the input-file path in:

```text
aerosol_volume_distribution.py
```

4. Run:

```bash
python aerosol_volume_distribution.py
```

The script will generate the aerosol volume distribution visualization.

---

## Reproducibility

The analysis workflow is structured to support reproducible processing of appropriately formatted particle-size distribution data.

For reproducibility, users should document:

* Data source
* Instrumentation
* Sampling period
* Particle-size bin definitions
* Data preprocessing procedures
* Time-zone and daylight-saving adjustments
* Any subsequent calibration or correction procedures

The repository does not contain the original research dataset because the underlying data may be unpublished or subject to research-data restrictions.

---

## Scientific Context

Time-resolved particle-size distributions provide information about the physical characteristics and temporal evolution of atmospheric aerosols.

Characterizing these distributions during prescribed burning events is particularly relevant to understanding:

* Smoke-derived particulate matter
* Indoor and outdoor particle transport
* Particle infiltration into buildings
* Filtration performance
* Human exposure to combustion-derived aerosols

This repository represents one component of a broader research workflow investigating **air quality and particulate-matter exposure during smoke events**.

---

## Limitations

The current workflow is primarily a **data-processing and visualization workflow**.

It does not independently:

* Calculate particle volume from raw particle counts
* Perform aerosol mass conversion
* Apply an aerosol density assumption
* Perform instrument-specific calibration
* Calculate indoor PM₂.₅ exposure
* Estimate respiratory deposited mass
* Perform indoor mass-balance modeling

Those analyses may be implemented in separate research workflows.

---

## Future Development

Potential extensions include:

* Automated instrument-data quality control
* Additional particle-size bins
* Automated figure export
* Configurable date ranges
* Instrument-specific calibration and correction factors
* Integration with outdoor PM₂.₅ measurements
* Indoor–outdoor particle comparison
* Automated analysis of smoke-event periods
* Integration with indoor PM₂.₅ mass-balance modeling

---

## Author

**Shabna V.S.**
PhD Researcher
University of Alabama

Research interests include:

**Air Quality · Aerosol Science · Indoor Air Quality · PM₂.₅ Exposure · Particle Filtration · Environmental Exposure Assessment**

---

## License

This repository is intended for research and educational use.

A specific open-source license should be selected before the repository is publicly distributed for reuse.

---

## Citation

If this code contributes to research, please cite the associated research publication or repository when a formal citation becomes available.

> Citation information will be added when the associated research work is publicly released.

````

