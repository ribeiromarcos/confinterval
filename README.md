ConfInterval
===

**Table of Contents**

- [Introduction](#introduction)
- [Command Line Usage](#command-line-usage)

# Introduction

ConfInterval is a tool for calculation of confidence interval over experiments results.
The experiment results must be in a text file containing one experiment result per line.
The text file must have a header with field names and one field must be the key field.
The confidence interval is calculated over the key field.

# Command Line Usage

The command line parameters of IncSimpleGen are:
- -h/--help: Show help message
- -i/--input: Input data file
- -k/--key: Key field
- -o/--output: Output result file
- -d/--delimiter: field delimiter (default: ,)
- -c/--confidence: Confidence (default: 0.95)
