"""Command-line interface for codon usage analysis and DNA sequence generation.

This module provides a command-line tool with two main functions:
- analyze: Process FASTA files to generate codon usage statistics and visualizations
- generate: Create DNA sequences from protein sequences using codon usage preferences

Usage
    analyze:  main.py analyze -f input.fasta [-o output.png]
    generate: main.py generate -p PROTEIN -f frequencies.csv [-n num_variants] [--method {preferred,weighted}]
"""

#!/usr/bin/env python3
import argparse
import pandas as pd
from frequency_table import (
    analyze_codon_counts,
    count_codons,
    create_csv_and_visualization,
    protein_to_dna_preferred,
    protein_to_dna_weighted,
    generate_multiple_variants,
)


def create_parser() -> argparse.ArgumentParser:
    """Create and return configured argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze codon usage and generate DNA sequences from protein sequences"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Parser for analyzing codon frequencies
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze codon frequencies from FASTA file"
    )
    analyze_parser.add_argument(
        "-f", "--fasta", required=True, help="Path to input FASTA file"
    )
    analyze_parser.add_argument(
        "-o", "--output", required=True, help="Path to output csv file "
    )
    analyze_parser.add_argument(
        "-v",
        "--heatmap",
        required=False,
        help="Path to heamap visualization file (PNG format)",
    )

    # Parser for DNA sequence generation
    generate_parser = subparsers.add_parser(
        "generate", help="Generate DNA sequence from protein sequence"
    )
    generate_parser.add_argument(
        "-p", "--protein", required=True, help="Input protein sequence"
    )
    generate_parser.add_argument(
        "-f",
        "--frequency_table",
        required=True,
        help="Path to frequency table CSV file",
    )
    generate_parser.add_argument(
        "-n",
        "--num_variants",
        type=int,
        default=1,
        help="Number of variants to generate (default: 1)",
    )
    generate_parser.add_argument(
        "--method",
        choices=["preferred", "weighted"],
        default="weighted",
        help="Method for codon selection (default: weighted)",
    )

    return parser

# pylint: disable=too-many-branches
def main() -> None:
    """Execute the command-line interface for codon usage analysis and DNA sequence generation.
    
    Processes command-line arguments to either:
    - Analyze FASTA files and generate codon usage statistics
    - Generate DNA sequences from protein sequences using specified codon preferences
    
    Handles errors during execution and displays help information if no valid command is provided.
    """

    parser = create_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        try:
            codon_counts, aa_counts = count_codons(args.fasta)
            create_csv_and_visualization(
                df = analyze_codon_counts(codon_counts, aa_counts),
                csv_output=args.output,
                output_path=args.heatmap)
            print("Analysis complete.")
            # Save the frequency table for later use
            print(f"Frequency table saved to {args.output}")
            if args.heatmap:
                print(f"Visualization is saved to {args.heatmap}")

        except FileNotFoundError as e:
            print(f"Input file not found: {str(e)}")
        except IOError as e:
            print(f"Error reading/writing file: {str(e)}")
        except pd.errors.EmptyDataError:
            print("The input file is empty")
        except ValueError as e:
            print(f"Invalid data format: {str(e)}")

    elif args.command == "generate":
        try:
            # Load frequency table
            frequency_df = pd.read_csv(args.frequency_table)

            if args.method == "preferred":
                dna_sequence = protein_to_dna_preferred(args.protein, frequency_df)
                print(f"Generated DNA sequence (preferred codons):\n{dna_sequence}")
            elif args.num_variants > 1: # weighted
                variants = generate_multiple_variants(
                    args.protein, frequency_df, args.num_variants
                )
                print(f"Generated {args.num_variants} DNA sequence variants:")
                for i, variant in enumerate(variants, 1):
                    print(f"Variant {i}:\n{variant}")
            else:
                dna_sequence = protein_to_dna_weighted(args.protein, frequency_df)
                print(f"Generated DNA sequence (weighted):\n{dna_sequence}")

        except FileNotFoundError:
            print(f"Frequency table file not found: {args.frequency_table}")
        except pd.errors.EmptyDataError:
            print("The frequency table file is empty")
        except ValueError as e:
            print(f"Invalid input data: {str(e)}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
