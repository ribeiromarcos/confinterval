ConfInterval
===

**Table of Contents**

- [Introduction](#introduction)
- [Command Line Usage](#command-line-usage)
- [Example](#example)

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

# Example

Consider the file *input.csv* with the following content:
```
data,        alg1,       alg2,          alg3
  16,     276.078,      0.505,       206.497
  16,     266.870,      0.495,       209.497
  16,     280.123,      0.515,       215.497
  32,    1106.013,      0.877,      9835.530
  32,    1098.654,      0.927,      9885.530
  32,    1126.674,      0.857,      9855.530
  64,    4210.488,      1.740,    149661.814
  64,    4219.987,      1.840,    149681.814
  64,    4212.388,      1.770,    149647.814
 128,   17053.388,      3.475,  10749661.816
 128,   17034.987,      3.575,  10749701.810
 128,   17041.712,      3.415,  10749750.830
 256,   71522.986,      6.938, 199496610.869
 256,   71506.837,      6.738, 199496700.837
 256,   71518.982,      7.038, 199496589.887
 512,  283362.783,     14.395,           nan
 512,  283372.783,     14.295,           nan
 512,  283351.783,     14.895,           nan
1024, 1167750.323,     34.356,           nan
1024, 1167800.323,     35.356,           nan
1024, 1167789.323,     36.356,           nan
```

The calculation of confidence interval can be done by the following command:
```
confinterval.y -i input.csv -k data -o output.csv
```

The content of file *output.csv* is:
```
data,        alg1, alg1_conf,   alg2, alg2_conf,          alg3, alg3_conf
  16,     274.357,     7.686,  0.505,     0.011,       210.497,  5.186
  32,    1110.447,    16.438,  0.887,     0.041,      9858.863, 28.478
  64,    4214.288,     5.688,  1.783,     0.058,    149663.814, 19.337
 128,   17043.362,    10.536,  3.488,     0.092,  10749704.819, 50.450
 256,   71516.268,     9.516,  6.905,     0.173, 199496633.864, 66.697
 512,  283362.450,    11.886, 14.528,     0.364,           nan, nan
1024, 1167779.990,    29.732, 35.356,     1.132,           nan, nan
```
