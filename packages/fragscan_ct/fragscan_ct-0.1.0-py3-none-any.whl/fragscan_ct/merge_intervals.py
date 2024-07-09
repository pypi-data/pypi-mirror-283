import pandas as pd
import typer
from rich import print
from rich.console import Console
from collections import defaultdict

err_console = Console(stderr=True)


def merge_bed_intervals(bed_file):
    """
    The `merge_bed_intervals` function merges overlapping intervals from a BED file based on chromosome,
    gene, start, end, and strand information.

    :param bed_file: The `bed_file` parameter in the `merge_bed_intervals` function is expected to be a
    file path to a BED file. BED (Browser Extensible Data) format is a widely used file format for
    representing genomic features as intervals. Each line in a BED file represents an interval on a
    chromosome with
    :return: The `merge_bed_intervals` function returns a list of merged intervals from a BED file. Each
    interval is represented as a tuple containing chromosome, start position, end position, gene
    information, a placeholder value of 0, and strand information.
    """
    merged_intervals = defaultdict(list)

    with open(bed_file, "r") as file:
        for line in file:
            fields = line.strip().split("\t")
            if len(fields) < 6:
                err_console.print(
                    "FATAL: Number of columns in input bed file is less than 6",
                    fg=typer.colors.BRIGHT_RED,
                )
                exit(1)
            chrom, start, end, info, score, strand = fields

            gene_info = info.split(":")
            if len(gene_info) < 2:
                gene = "Unknown"
            else:
                gene = gene_info[0]

            merged_intervals[(chrom, gene)].append(
                (int(start), int(end), info, score, strand)
            )

    merged_result = []
    for (chrom, gene), intervals in merged_intervals.items():
        intervals.sort(key=lambda x: x[0])
        prev_start, prev_end, prev_info, prev_score, prev_strand = intervals[0]

        for start, end, info, score, strand in intervals[1:]:
            if end >= prev_end and strand == prev_strand:
                prev_end = max(prev_end, end)
            else:
                merged_result.append(
                    (
                        chrom,
                        prev_start,
                        prev_end,
                        info,
                        prev_score,
                        prev_strand,
                    )
                )
                prev_start, prev_end, prev_info, prev_score, prev_strand = (
                    start,
                    end,
                    info,
                    score,
                    strand,
                )
        merged_result.append(
            (chrom, prev_start, prev_end, prev_info, prev_score, prev_strand)
        )

    return merged_result
