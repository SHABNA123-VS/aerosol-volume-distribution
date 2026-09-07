"""
Aerosol Volume Distribution During Prescribed Burning Events

This script processes time-resolved particle-size distribution data
and generates a particle-size-resolved aerosol volume distribution
heatmap.

Expected input:
    Excel file containing:
        #YY/MM/DD
        HR:MN:SC
        0.3
        0.5
        1.0
        2.5
        5.0
        10.0

Author:
    Shabna V.S.
    University of Alabama
"""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm


# ================================================================
# Configuration
# ================================================================

INPUT_FILE = Path("data/Book3.xlsx")

PARTICLE_SIZE_COLUMNS = [0.3, 0.5, 1.0, 2.5, 5.0, 10.0]

DP_EDGES = np.array(
    [0.3, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0]
)

DST_START = pd.Timestamp("2026-03-08 01:00:00")

FIGURE_SIZE = (15, 6)
FIGURE_DPI = 600


# ================================================================
# Data Loading
# ================================================================

def load_data(input_file: Path) -> pd.DataFrame:
    """Load the aerosol measurement data from an Excel file."""

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    return pd.read_excel(input_file)


# ================================================================
# Data Cleaning
# ================================================================

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert numeric particle-size column names to floats."""

    df = df.copy()

    cleaned_columns = []

    for column in df.columns:
        column_string = str(column)

        if (
            isinstance(column, (int, float))
            or column_string.replace(".", "").isdigit()
        ):
            try:
                cleaned_columns.append(float(column))
                continue
            except ValueError:
                pass

        cleaned_columns.append(column)

    df.columns = cleaned_columns

    return df


def create_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    """Combine date and time columns into a datetime index."""

    df = df.copy()

    required_columns = ["#YY/MM/DD", "HR:MN:SC"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["datetime"] = pd.to_datetime(
        df["#YY/MM/DD"].astype(str)
        + " "
        + df["HR:MN:SC"].astype(str),
        errors="coerce",
    )

    df = df.dropna(subset=["datetime"])

    return df


def apply_daylight_saving_adjustment(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply the daylight-saving-time adjustment used for the
    March 2026 measurement period.
    """

    df = df.copy()

    mask = df["datetime"] >= DST_START

    df.loc[mask, "datetime"] = (
        df.loc[mask, "datetime"]
        + pd.Timedelta(hours=1)
    )

    return df


# ================================================================
# Particle-Size Data Preparation
# ================================================================

def prepare_particle_size_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Extract and prepare particle-size distribution data."""

    missing_columns = [
        column
        for column in PARTICLE_SIZE_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing particle-size columns: "
            f"{missing_columns}"
        )

    df_conc = df[PARTICLE_SIZE_COLUMNS].copy()

    df_conc.index = df["datetime"]

    return df_conc


# ================================================================
# Visualization
# ================================================================

def create_volume_distribution_plot(
    df_conc: pd.DataFrame,
) -> None:
    """Generate the aerosol volume distribution heatmap."""

    # Matrix for pcolormesh
    z_matrix = df_conc.T.values

    # LogNorm cannot process zero or negative values
    z_matrix = np.where(
        z_matrix <= 0,
        np.nan,
        z_matrix,
    )

    time = df_conc.index

    if len(time) == 0:
        raise ValueError("No valid measurement timestamps found.")

    time_values = mdates.date2num(time)

    start_num = time_values[0]
    end_num = time_values[-1]

    # Create cell edges so the heatmap spans the full
    # measurement period.
    time_edges = np.linspace(
        start_num,
        end_num,
        len(time) + 1,
    )

    # ------------------------------------------------------------
    # Plot formatting
    # ------------------------------------------------------------

    plt.rcParams.update(
        {
            "font.weight": "bold",
            "axes.labelweight": "bold",
            "axes.titleweight": "bold",
            "mathtext.default": "regular",
        }
    )

    fig, ax = plt.subplots(
        figsize=FIGURE_SIZE,
        dpi=FIGURE_DPI,
    )

    valid_values = z_matrix[np.isfinite(z_matrix)]

    if len(valid_values) == 0:
        raise ValueError(
            "No positive particle-size distribution values "
            "are available for plotting."
        )

    mesh = ax.pcolormesh(
        time_edges,
        DP_EDGES,
        z_matrix,
        shading="flat",
        norm=LogNorm(
            vmin=1e-3,
            vmax=np.nanmax(z_matrix),
        ),
        cmap="jet",
    )

    # ------------------------------------------------------------
    # Colorbar
    # ------------------------------------------------------------

    colorbar = plt.colorbar(
        mesh,
        ax=ax,
        pad=0.02,
    )

    colorbar_label = (
        r"$\mathbf{\mathit{dV}/\mathit{d\log\ D_p}}$"
        r"$\mathbf{\ [\mathrm{\mu m^3\ cm^{-3}}]}$"
    )

    colorbar.set_label(
        colorbar_label,
        fontsize=12,
    )

    for label in colorbar.ax.get_yticklabels():
        label.set_fontweight("bold")

    # ------------------------------------------------------------
    # Y-axis
    # ------------------------------------------------------------

    ax.set_yscale("log")
    ax.set_ylim(0.3, 25.0)

    ax.set_yticks(
        [
            0.3,
            0.5,
            1.0,
            2.5,
            5.0,
            10.0,
            25.0,
        ]
    )

    ax.get_yaxis().set_major_formatter(
        ticker.ScalarFormatter()
    )

    # ------------------------------------------------------------
    # X-axis
    # ------------------------------------------------------------

    ax.set_xlim(
        start_num,
        end_num,
    )

    custom_ticks = np.linspace(
        start_num,
        end_num,
        8,
    )

    ax.set_xticks(custom_ticks)

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%m/%d")
    )

    plt.xticks(
        rotation=0,
        ha="center",
        fontsize=10,
        fontweight="bold",
    )

    for label in (
        ax.get_xticklabels()
        + ax.get_yticklabels()
    ):
        label.set_fontweight("bold")

    # ------------------------------------------------------------
    # Labels and title
    # ------------------------------------------------------------

    y_label = r"$\mathit{D_p}$ [$\mathrm{\mu m}$]"

    ax.set_xlabel(
        "Date [MM-DD]",
        fontweight="bold",
        fontsize=12,
    )

    ax.set_ylabel(
        y_label,
        fontweight="bold",
        fontsize=12,
    )

    ax.set_title(
        "Aerosol Volume Distribution: "
        "Prescribed Burning 2026",
        pad=20,
        fontsize=14,
    )

    plt.tight_layout()
    plt.show()


# ================================================================
# Main Workflow
# ================================================================

def main() -> None:
    """Run the complete aerosol volume distribution workflow."""

    df = load_data(INPUT_FILE)

    df = clean_column_names(df)

    df = create_datetime_index(df)

    df = apply_daylight_saving_adjustment(df)

    df_conc = prepare_particle_size_data(df)

    create_volume_distribution_plot(df_conc)


if __name__ == "__main__":
    main()
