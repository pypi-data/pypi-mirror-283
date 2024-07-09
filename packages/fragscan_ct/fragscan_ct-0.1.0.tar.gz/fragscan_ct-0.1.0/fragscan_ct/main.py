from pathlib import Path
import typer
from typing import List, Optional, Tuple
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
from rich.console import Console
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
from fragscan_ct.read_bed import read_bed
from fragscan_ct.merge_intervals import merge_bed_intervals
from fragscan_ct.lowess import perform_lowess
from fragscan_ct.pad_coordinates import pad_coordinates
from fragscan_ct.calculate_fragment_length_ratio import calculate_fragment_length_ratio

err_console = Console(stderr=True)
app = typer.Typer()


@app.command()
def generate_fragment_ratios(
    reference_file: Path = typer.Option(
        ...,
        "--reference-file",
        "-r",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Input reference genome FASTA file to be used while traversing the BAM file",
    ),
    input_bed: Path = typer.Option(
        ...,
        "--input-bed",
        "-i",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Input BED file to be used to traverse the BAM file",
    ),
    input_bam: Path = typer.Option(
        ...,
        "--input-bam",
        "-bam",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Input BAM file to be used to calculate fragment length",
    ),
    output_txt: str = typer.Option(
        "fragment_counts.txt",
        "--output-txt",
        "-o",
        help="Output TXT file after traversing the BAM file",
    ),
    sample_id: str = typer.Option(
        ...,
        "--sample-id",
        "-id",
        help="Sample Identifier",
    ),
    merge_interval: bool = typer.Option(
        False,
        "--merge-interval",
        "-m",
        help="Merge interval in the BED file by splitting the 4th column with `:` and using the first value",
    ),
    split_interval: bool = typer.Option(
        False,
        "--split-interval",
        "-s",
        help="Split the BED interval based on the BIN size specified in the `bin_size` option.",
    ),
    short_fragment_length: Tuple[int, int] = typer.Option(
        [100, 150],
        "--short-fragment-length",
        "-sfl",
        help="Define which fragments should be called as short fragment, provide two integers separated by a comma, the first value in the tuple is the lower bound of the fragment length range for short fragments, and the second value is the upper bound of the fragment length range for short fragments",
    ),
    long_fragment_length: Tuple[int, int] = typer.Option(
        [151, 220],
        "--long-fragment-length",
        "-lfl",
        help="Define which fragments should be called as long fragment, provide two integers separated by a comma, the first value in the tuple is the lower bound of the fragment length range for long fragments, and the second value is the upper bound of the fragment length range for long fragments",
    ),
    bin_size: int = typer.Option(
        50,
        "--bin-size",
        "-b",
        help="Bin size to split the BED file, only used when `split_interval` is True",
    ),
    pad_size: int = typer.Option(
        50,
        "--pad-size",
        "-p",
        help="Pad the coordinates with the given pad size in the BED file, before binning",
    ),
    lowess_fraction: float = typer.Option(
        0.75,
        "--lowess-fraction",
        "-l",
        help="When running lowess GC correction of coverage, the fraction of the data used when estimating each y-value",
    ),
):
    """
    The `generate_fragment_ratios` function calculates fragment ratios from a BAM file using input BED
    and reference genome files, with options for interval manipulation and GC correction.

    :param reference_file: The `reference_file` parameter is the input reference genome FASTA file that
    will be used while traversing the BAM file. This file contains the reference genome sequences that
    will be used for alignment and analysis in the process of calculating fragment ratios
    :type reference_file: Path
    :param input_bed: The `input_bed` parameter is used to specify the input BED file that will be used
    to traverse the BAM file. The BED file contains genomic intervals that define regions of interest
    for analysis. This parameter expects a valid path to an existing BED file that is readable
    :type input_bed: Path
    :param input_bam: The `input_bam` parameter in the `generate_fragment_ratios` function is used to
    specify the input BAM file that will be used to calculate fragment length. This BAM file contains
    the aligned sequencing reads from a sequencing experiment, typically aligned to a reference genome.
    The function will traverse this BAM file
    :type input_bam: Path
    :param output_txt: The `output_txt` parameter in the `generate_fragment_ratios` function is used to
    specify the name of the output TXT file that will be generated after processing the input files and
    calculating the fragment ratios. This file will contain the results of the analysis, including
    information such as chromosome, start and end
    :type output_txt: str
    :param sample_id: The `sample_id` parameter is used to specify the sample identifier for the data
    being processed. This identifier will be included in the output file to associate the results with a
    specific sample
    :type sample_id: str
    :param merge_interval: The `merge_interval` parameter is a boolean option that determines whether to
    merge intervals in the BED file by splitting the 4th column with `:` and using the first value. If
    set to `True`, the intervals will be merged before processing. If set to `False`, the intervals will
    not
    :type merge_interval: bool
    :param split_interval: The `split_interval` parameter is a boolean option that determines whether to
    split the BED interval based on the specified `bin_size`. If `split_interval` is set to `True`, the
    BED interval will be divided into bins of size `bin_size`. Each bin will then be used to calculate
    fragment
    :type split_interval: bool
    :param short_fragment_length: The `short_fragment_length` parameter in the
    `generate_fragment_ratios` function is used to define the range of fragment lengths that should be
    considered as short fragments during the analysis. It expects two integers separated by a comma
    within a tuple
    :type short_fragment_length: Tuple[int, int]
    :param long_fragment_length: The `long_fragment_length` parameter in the `generate_fragment_ratios`
    function is used to define the range of fragment lengths that should be considered as long
    fragments. It expects a tuple of two integers separated by a comma. The first value in the tuple
    represents the lower bound of the fragment length range
    :type long_fragment_length: Tuple[int, int]
    :param bin_size: The `bin_size` parameter specifies the size of the bins used to split the BED file
    when the `split_interval` option is set to True. This parameter determines the interval size for
    dividing the genomic regions in the BED file for further analysis. In your function
    `generate_fragment_ratios`, the `
    :type bin_size: int
    :param pad_size: The `pad_size` parameter in the `generate_fragment_ratios` function specifies the
    size by which the coordinates in the BED file should be padded before binning. This padding helps in
    extending the interval boundaries by a specified amount to capture additional genomic regions around
    the original coordinates. The padded coordinates are then
    :type pad_size: int
    :param lowess_fraction: The `lowess_fraction` parameter specifies the fraction of the data used when
    estimating each y-value during the process of running lowess GC correction of coverage. This
    parameter controls the smoothing factor for the lowess algorithm, influencing how much weight is
    given to nearby data points when estimating the corrected coverage values
    :type lowess_fraction: float
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        print("\n")
        progress.add_task(description="Processing\n", total=None)

        chromosome_location = []
        start_location = []
        end_location = []
        info_location = []
        strand_location = []
        score_location = []
        short_fragment_counts = []
        long_fragment_counts = []
        raw_ratio = []
        coverage_short_fragments = []
        coverage_long_fragments = []
        gc_content_short_fragments = []
        gc_content_long_fragments = []

        if merge_interval and split_interval:
            err_console.print(
                "FATAL: Both `merge_interval` and `split_interval` options cannot be true",
                fg=typer.colors.BRIGHT_RED,
            )
            exit(1)
        if pad_size > 0:
            print("[green]INFO:[/green] We will pad intervals before analyzing.")
        if split_interval:
            print("[green]INFO:[/green] We will split intervals before analyzing.")
        if merge_interval:
            print("[green]INFO:[/green] Merging intervals before analyzing.")
            bed_data = merge_bed_intervals(input_bed)
        else:
            bed_data = read_bed(input_bed)
        for chromosome, start, end, info, score, strand in bed_data:
            # Pad the coordinates
            if pad_size > 0:
                padded_start, padded_end = pad_coordinates(start, end, pad_size)
            else:
                padded_start = start
                padded_end = end
            if split_interval:
                # Calculate the number of bins based on the padded coordinates
                num_bins = (padded_end - padded_start) // bin_size
                for i in range(num_bins):
                    bin_start = padded_start + (i * bin_size)
                    bin_end = bin_start + bin_size
                    # Calculate the fragment length for reads falling in the specified ranges from a BAM file and calculate the ratio
                    (
                        short_fragments,
                        long_fragments,
                        ratio,
                        coverage_short_fragment,
                        coverage_long_fragment,
                        avg_gc_content_short_fragment,
                        avg_gc_content_long_fragment,
                    ) = calculate_fragment_length_ratio(
                        input_bam,
                        reference_file,
                        chromosome,
                        bin_start,
                        bin_end,
                        short_fragment_length,
                        long_fragment_length,
                    )
                    chromosome_location.append(chromosome)
                    start_location.append(bin_start)
                    end_location.append(bin_end)
                    info_location.append(info)
                    strand_location.append(strand)
                    score_location.append(score)
            else:
                (
                    short_fragments,
                    long_fragments,
                    ratio,
                    coverage_short_fragment,
                    coverage_long_fragment,
                    avg_gc_content_short_fragment,
                    avg_gc_content_long_fragment,
                ) = calculate_fragment_length_ratio(
                    input_bam,
                    reference_file,
                    chromosome,
                    padded_start,
                    padded_end,
                    short_fragment_length,
                    long_fragment_length,
                )
                chromosome_location.append(chromosome)
                start_location.append(padded_start)
                end_location.append(padded_end)
                info_location.append(info)
                strand_location.append(strand)
                score_location.append(score)

            if short_fragments > 0 or long_fragments > 0:
                short_fragment_counts.append(short_fragments)
                long_fragment_counts.append(long_fragments)
                raw_ratio.append(ratio)
                coverage_short_fragments.append(coverage_short_fragment)
                coverage_long_fragments.append(coverage_long_fragment)
                gc_content_short_fragments.append(avg_gc_content_short_fragment)
                gc_content_long_fragments.append(avg_gc_content_long_fragment)
            else:
                short_fragment_counts.append(np.nan)
                long_fragment_counts.append(np.nan)
                raw_ratio.append(np.nan)
                coverage_short_fragments.append(np.nan)
                coverage_long_fragments.append(np.nan)
                gc_content_short_fragments.append(np.nan)
                gc_content_long_fragments.append(np.nan)

        short_fragment_counts = np.array(short_fragment_counts)
        long_fragment_counts = np.array(long_fragment_counts)
        short_fragment_zscore = stats.zscore(short_fragment_counts, nan_policy="omit")
        long_fragment_zscore = stats.zscore(long_fragment_counts, nan_policy="omit")
        zscore_ratio = np.divide(
            short_fragment_zscore,
            long_fragment_zscore,
            out=np.zeros_like(short_fragment_zscore),
            where=long_fragment_zscore != 0,
        )
        lowess_normalized_coverage_short_fragments = perform_lowess(
            gc_content_short_fragments, coverage_short_fragments, lowess_fraction
        )
        lowess_normalized_coverage_long_fragments = perform_lowess(
            gc_content_long_fragments, coverage_long_fragments, lowess_fraction
        )
        coverage_short_fragments = np.array(coverage_short_fragments)
        coverage_long_fragments = np.array(coverage_long_fragments)
        mean_coverage_short_fragments = np.nanmean(coverage_short_fragments)
        mean_coverage_long_fragments = np.nanmean(coverage_long_fragments)
        gc_corrected_coverage_short_fragments = np.subtract(
            coverage_short_fragments, lowess_normalized_coverage_short_fragments
        )
        gc_corrected_coverage_long_fragments = np.subtract(
            coverage_long_fragments, lowess_normalized_coverage_long_fragments
        )
        final_coverage_short_fragments = np.add(
            gc_corrected_coverage_short_fragments, mean_coverage_short_fragments
        )
        final_coverage_long_fragments = np.add(
            gc_corrected_coverage_long_fragments, mean_coverage_long_fragments
        )
        final_ratio = np.divide(
            final_coverage_short_fragments,
            final_coverage_long_fragments,
            out=np.zeros_like(final_coverage_short_fragments),
            where=final_coverage_long_fragments != 0,
        )
        output_file = open(output_txt, "w")
        output_file.write(
            "Chromosome\tStart_Position\tEnd_Position\tName\tScore\tStrand\tSample_Id\tShort_Fragments\tLong_Fragments\tRaw_Ratio\tShort_Fragments_Zscore\tLong_Fragments_Zscore\tZscore_Ratio\tCoverage_Short_Fragments\tCoverage_Long_Fragments\tCoverage_Ratio\n"
        )
        for i, chrom in enumerate(chromosome_location):
            short_counts = short_fragment_counts[i]
            long_counts = long_fragment_counts[i]
            short_zscores = np.array2string(
                short_fragment_zscore[i], precision=5, floatmode="fixed"
            )
            long_zscores = np.array2string(
                long_fragment_zscore[i], precision=5, floatmode="fixed"
            )
            zscore_ratios = np.array2string(
                zscore_ratio[i], precision=5, floatmode="fixed"
            )
            final_short_coverage = np.array2string(
                final_coverage_short_fragments[i], precision=5, floatmode="fixed"
            )
            final_long_coverage = np.array2string(
                final_coverage_long_fragments[i], precision=5, floatmode="fixed"
            )
            final_ratios = np.array2string(
                final_ratio[i], precision=5, floatmode="fixed"
            )
            output_line = f"{chrom}\t{start_location[i]}\t{end_location[i]}\t{info_location[i]}\t{score_location[i]}\t{strand_location[i]}\t{sample_id}\t{short_counts}\t{long_counts}\t{raw_ratio[i]}\t{short_zscores}\t{long_zscores}\t{zscore_ratios}\t{final_short_coverage}\t{final_long_coverage}\t{final_ratios}\n"
            output_file.write(output_line)

        output_file.close()

        typer.echo(f"New TXT file generated: {output_txt}")


@app.command()
def plot_fragment_ratios(
    list_of_files: Path = typer.Option(
        None,
        "--list",
        "-l",
        help="File of files, List of txt files to be used for plotting",
    ),
    input_txt: Optional[List[Path]] = typer.Option(
        None,
        "--input-txt",
        "-i",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help="Input TXT file that was generated using generate_fragment_counts",
    ),
    output_prefix: str = typer.Option(
        "fragment_counts",
        "--output-prefix",
        "-o",
        help="Output HTML file prefix for the line and box plot",
    ),
):
    """
    The `plot_fragment_ratios` function takes in a file of files or a list of input TXT files, reads the
    data from the files into a Pandas DataFrame, and plots a line plot of the "Ratio" column against the
    "Id" column, with different colors for each "Sample_Id". The resulting plot is saved as an HTML
    file.

    :param list_of_files: A file that contains a list of text files to be used for plotting. Each text
    file should contain data in a specific format
    :type list_of_files: Path
    :param input_txt: The `input_txt` parameter is an optional list of input TXT files that were
    generated using the `generate_fragment_counts` function. These files contain the data needed for
    plotting the line plot
    :type input_txt: Optional[List[Path]]
    :param output_html: The `output_html` parameter is a string that specifies the name of the output
    HTML file that will be generated with the line plot. By default, it is set to
    "fragment_counts.html". You can provide a different name for the output file by specifying it using
    the `--output-html` or
    :type output_html: str
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        print("\n")
        progress.add_task(description="Processing\n", total=None)
        if not list_of_files:
            typer.secho(
                "File are not provided as file of files.", fg=typer.colors.BRIGHT_YELLOW
            )
            if not input_txt:
                typer.secho(
                    "File were not provided via command line as well",
                    fg=typer.colors.BRIGHT_RED,
                )
                raise typer.Abort()
        # Read file of files
        if not input_txt:
            input_txt = [line.strip() for line in open(list_of_files, "r")]
        dfs = []
        for txt_file in input_txt:
            if Path(txt_file).is_file():
                typer.secho(f"Reading: {txt_file}", fg=typer.colors.BRIGHT_GREEN)
                # Read the file into a data frame
                df = pd.read_csv(txt_file, delimiter="\t")
                # Append the data frame to the list
                dfs.append(df)
        # Concatenate all data frames into a single data frame
        combined_df = pd.concat(dfs, ignore_index=True)

        combined_df["Id"] = [
            "_".join(i)
            for i in zip(
                combined_df["Chromosome"].map(str),
                combined_df["Start_Position"].map(str),
                combined_df["End_Position"].map(str),
            )
        ]
        # Create line plot using Plotly
        fig = px.line(
            combined_df,
            x="Id",
            y="Raw_Ratio",
            color="Sample_Id",
            hover_name="Sample_Id",
            hover_data=["Name", "Raw_Ratio"],
        )
        # Customize the layout
        fig.update_layout(
            title="Line plots of Ratio by Chromosome",
            xaxis_title="Chromosome",
            yaxis_title="Raw_Ratio",
        )
        # Save the plot as an interactive HTML file
        output_line = output_prefix + "_" + "line.html"
        fig.write_html(output_line)

        # Create side-by-side boxplots using Plotly
        fig = px.box(
            combined_df,
            x="Chromosome",
            y="Raw_Ratio",
            facet_row="Sample_Id",
            hover_name="Sample_Id",
            hover_data=["Chromosome", "Name", "Raw_Ratio"],
        )
        # Customize the layout
        fig.update_layout(
            title="Box plots of Ratio by Chromosome",
            xaxis_title="Chromosome",
            yaxis_title="Ratio",
        )
        # Save the plot as an interactive HTML file
        output_box = output_prefix + "_" + "box.html"
        fig.write_html(output_box)
    typer.echo(f"HTML line plot file generated: {output_line}")
    typer.echo(f"HTML box plot file generated: {output_box}")


#if __name__ == "__main__":
#    app()
