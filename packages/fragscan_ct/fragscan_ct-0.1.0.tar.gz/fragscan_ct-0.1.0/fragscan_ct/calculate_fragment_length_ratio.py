import pysam
import numpy as np
import typer
from rich import print
from rich.console import Console

err_console = Console(stderr=True)

def calculate_fragment_length_ratio(bam_file, reference_file, chromosome, start, end, short_fragment_length, long_fragment_length):
    """
    The function `calculate_fragment_length_ratio` calculates the ratio between counts of fragments
    falling in specified length ranges from a given BAM file.
    
    :param bam_file: The `bam_file` parameter is the path to a BAM file. BAM files are binary files used
    to store DNA sequence alignment data from high-throughput sequencing experiments
    :param reference_file: The `reference_file` parameter in the function
    `calculate_fragment_length_ratio` is the path to a reference file in FASTA format. This file
    contains the reference genome sequence that is used for aligning the reads in the BAM file. The
    reference genome sequence is essential for mapping the reads to the genome
    :param chromosome: The `chromosome` parameter specifies the chromosome or contig from which the
    reads should be fetched. It is a string that represents the name or identifier of the chromosome.
    For example, "chr1" or "2L". This parameter is used to specify the genomic region for which you want
    to
    :param start: The `start` parameter specifies the starting position on the chromosome where you want
    to calculate the fragment length ratio. It is an integer value representing the genomic coordinate
    where you want to start the analysis. For example, if you are interested in a specific region on
    chromosome 1 and want to start the analysis
    :param end: The `end` parameter specifies the end position of the range on the chromosome for which
    you want to calculate the fragment length ratio. It represents the genomic coordinate where the
    range ends
    :param short_fragment_length: The `short_fragment_length` parameter in the
    `calculate_fragment_length_ratio` function represents a tuple containing two values. The first value
    in the tuple is the lower bound of the fragment length range for short fragments, and the second
    value is the upper bound of the fragment length range for short fragments
    :param long_fragment_length: The `long_fragment_length` parameter in the
    `calculate_fragment_length_ratio` function is a tuple that specifies the range of fragment lengths
    considered as long fragments. It is used to filter reads based on their fragment lengths. The
    function will count the number of fragments falling within this specified range and calculate
    various metrics
    :return: The function `calculate_fragment_length_ratio` returns the following values:
    """
    short_fragments_lengths = []
    long_fragments_lengths = []
    gc_content_short_fragments = []
    gc_content_long_fragments = []
    coverage_short_fragments = 0
    coverage_long_fragments = 0
    reference = pysam.FastaFile(reference_file)
    with pysam.AlignmentFile(bam_file, "rb") as bam:
        for read in bam.fetch(chromosome, start, end):
            # if read.is_proper_pair and not read.is_secondary:
            fragment_length = abs(read.template_length)
            # count by binning the fragments
            if fragment_length >= short_fragment_length[0] and fragment_length <= short_fragment_length[1]:
                short_fragments_lengths.append(abs(read.template_length))
                seq = reference.fetch(
                    chromosome, read.reference_start, read.reference_end
                ).upper()
                gc_content = (seq.count("G") + seq.count("C")) / len(seq) * 100
                gc_content_short_fragments.append(gc_content)
                coverage_short_fragments += 1
            elif fragment_length >= long_fragment_length[0] and fragment_length <= long_fragment_length[1]:
                long_fragments_lengths.append(abs(read.template_length))
                seq = reference.fetch(
                    chromosome, read.reference_start, read.reference_end
                ).upper()
                gc_content = (seq.count("G") + seq.count("C")) / len(seq) * 100
                gc_content_long_fragments.append(gc_content)
                coverage_long_fragments += 1

    gc_content_short_fragments = np.array(gc_content_short_fragments)
    avg_gc_content_short_fragments = np.mean(gc_content_short_fragments)
    gc_content_long_fragments = np.array(gc_content_long_fragments)
    avg_gc_content_long_fragments = np.mean(gc_content_long_fragments)

    short_fragments_lengths = np.array(short_fragments_lengths)
    short_fragment_count = len(short_fragments_lengths)
    long_fragments_lengths = np.array(long_fragments_lengths)
    long_fragment_count = len(long_fragments_lengths)

    # Calculate the ratio
    try:
        ratio = short_fragment_count / long_fragment_count
    except ZeroDivisionError as e:
        err_console.print("Warning: Cannot divide by zero", fg=typer.colors.BRIGHT_YELLOW)
        ratio = 0

    return (
        short_fragment_count,
        long_fragment_count,
        ratio,
        coverage_short_fragments,
        coverage_long_fragments,
        avg_gc_content_short_fragments,
        avg_gc_content_long_fragments,
    )