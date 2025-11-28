#!/bin/bash
python3 mapper-interactive-cli.py ./sample_datasets/Pubchem_sub.csv --intervals 50 --overlap 50 --eps 1.5 --min_samples 2 --filter l2norm -output ./CLI_examples
