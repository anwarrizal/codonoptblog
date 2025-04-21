
# Codon Usage Analysis and DNA Sequence Generator

A Python command-line tool for analyzing codon usage patterns in DNA sequences and generating DNA sequences from protein sequences using customizable codon preferences.

## Features

- **Codon Usage Analysis**: Process FASTA files to generate codon usage statistics
- **DNA Sequence Generation**: Create DNA sequences from protein sequences using either preferred or weighted codon selection methods
- **Multiple Variant Generation**: Generate multiple DNA sequence variants for a given protein sequence
- **Visualization**: Generate heatmap visualizations of codon usage patterns

## Installation

```bash
# Clone the repository
git clone [repository-url]
cd [repository-name]
```
# Install required dependencies
```bash
pip install -r requirements.txt 
```

## Usage
The tool provides two main commands: analyze and generate

### Analyzing Codon Usage
```bash
python main.py analyze -f input.fasta -o output.csv [-v heatmap.png]
```
Arguments:

- -f, --fasta: Path to input FASTA file (required)

- -o, --output: Path to output CSV file (required)

- -v, --heatmap: Path to save heatmap visualization (optional, PNG format)


### Generating DNA sequences
```bash
python main.py generate -p PROTEIN -f frequencies.csv [-n num_variants] [--method {preferred,weighted}]
```

Arguments:

- -p, --protein: Input protein sequence (required)

- -f, --frequency_table: Path to frequency table CSV file (required)

- -n, --num_variants: Number of variants to generate (default: 1)

- --method: Method for codon selection (choices: preferred, weighted; default: weighted)

## Examples
1. Analyze codon usage from a FASTA file:
```bash
python main.py analyze -f sequences.fasta -o codon_frequencies.csv -v usage_heatmap.png
```
2. Generate a DNA sequence using preferred codons:
```bash
python main.py generate -p "MATGC" -f codon_frequencies.csv --method preferred
```

3. Generate multiple DNA sequence variants:
```bash
python main.py generate -p "MATGC" -f codon_frequencies.csv -n 5 --method weighted
```


