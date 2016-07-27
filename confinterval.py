#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Module to calculate error based on a confidence interval
'''

import csv


# Default values
DEFAULT_DELIMITER = ','
DEFAULT_CONFIDENCE = 0.95

# Variable identifiers
SUM = '_sum'
COUNT = '_count'
SQUARE_SUM = '_square_sum'
MEAN = '_mean'
VARIANCE = '_variance'
STD_DEVIATION = '_standard_deviation'
CONFIDENCE_INTERVAL = '_conf'

# List of statistics
STAT_LIST = [SUM, COUNT, SQUARE_SUM, MEAN, VARIANCE, STD_DEVIATION,
             CONFIDENCE_INTERVAL]
# List of output statistics
OUT_STAT_LIST = [MEAN, CONFIDENCE_INTERVAL]


class Data(object):
    '''
    Class to store table of data and calculate confidence interval
    '''
    def __init__(self, identifier, field_list):
        # Identifier field
        self._identifier = identifier
        # List of original records
        self._record_list = []
        # Set of fields
        self._field_set = set()
        # Dictionary with a list for each field
        self._values_dict = {}
        # Dictionary with statistics for each field
        self._statistics_dict = {}
        # Add each field
        for field in field_list:
            self._add_field(field)

    def _add_field(self, field):
        '''
        Add new field
        '''
        if field not in self._field_set:
            # Add field to field set
            self._field_set.add(field)
            # Start with an empty list of values
            self._values_dict[field] = []
            # Start statistics
            self._statistics_dict[field] = \
                {SUM: 0,
                 COUNT: 0,
                 SQUARE_SUM: 0,
                 MEAN: float('NaN'),
                 VARIANCE: float('NaN'),
                 STD_DEVIATION: float('NaN')}

    def add_record(self, record):
        '''
        Add a record of values
        '''
        self._record_list.append(record)
        for field in record:
            # Convert value to float
            value = float(record[field])
            # Check if value is valid
            if value != float('NaN'):
                # Add value do list of values
                self._values_dict[field].append(value)
                # Update statistics
                self._statistics_dict[field][SUM] += value
                self._statistics_dict[field][COUNT] += 1
                self._statistics_dict[field][SQUARE_SUM] += value * value

    def print_records(self):
        '''
        Print the list of records
        '''
        for rec in self._record_list:
            print rec

    def update_statistics(self, confidence):
        '''
        Calculate statistics
        '''
        from scipy.stats import norm  # IGNORE:no-name-in-module
        for field in self._field_set:
            fsum = self._statistics_dict[field][SUM]
            fcount = self._statistics_dict[field][COUNT]
            # Calculate mean
            fmean = fsum / fcount
            self._statistics_dict[field][MEAN] = fmean
            # Calculate variance
            fvariance = 0
            for value in self._values_dict[field]:
                fvariance += (value - fmean) ** 2
            fvariance = fvariance / (len(self._values_dict[field]) - 1)
            self._statistics_dict[field][VARIANCE] = fvariance
            # Calculate standard deviation
            fstd_deviantion = fvariance ** 0.5
            self._statistics_dict[field][STD_DEVIATION] = fstd_deviantion
            # Calculate critical z
            critical_z = 1 - ((1 - confidence) / 2)
            critical_z = norm.ppf(critical_z)
            # Calculate confidence interval
            fconf_interval = critical_z * fstd_deviantion / fcount ** 0.5
            self._statistics_dict[field][CONFIDENCE_INTERVAL] = fconf_interval

    def print_statistics(self):
        '''
        Print statistics
        '''
        for field in self._field_set:
            print '  FIELD {f}'.format(f=field)
            stat_dict = self._statistics_dict[field]
            for stat in stat_dict:
                print '    ' + str(stat) + ' = ' + str(stat_dict[stat])

    def get_error(self):
        '''
        Get dictionary from statistics
        '''
        out_dict = {}
        for field in self._field_set:
            out_dict[field] = self._statistics_dict[field][MEAN]
            out_dict[field] = '{:f}'.format(out_dict[field])
            out_dict[field + CONFIDENCE_INTERVAL] = \
                self._statistics_dict[field][CONFIDENCE_INTERVAL]
            out_dict[field + CONFIDENCE_INTERVAL] = \
                '{:f}'.format(out_dict[field + CONFIDENCE_INTERVAL])
        return out_dict


def convert(value):
    '''
    Try to convert value to integer
    '''
    new_value = value
    try:
        new_value = int(value)
        return new_value
    except ValueError:
        return new_value


def read_file(fname, id_field, field_delimiter):
    '''
    Read file content
    '''
    data_dict = {}
    # Open file
    input_file = open(fname, 'r')
    reader = csv.DictReader(input_file, delimiter=field_delimiter,
                            skipinitialspace=True)
    # Get file fields except id_field
    field_list = [field for field in reader.fieldnames if field != id_field]
    # Read file records
    for record in reader:
        # Get identifier value
        id_value = record.pop(id_field)
        id_value = convert(id_value)
        # Check if this identifier is already exists
        if id_value in data_dict:
            # Get existent data structure
            data = data_dict[id_value]
        else:
            # Create a new data structure
            data = Data(id_value, field_list)
            data_dict[id_value] = data
        # Add record to data structure
        data.add_record(record)
    input_file.close()
    return data_dict


def write_file(fname, id_field, record_list,
               field_delimiter=DEFAULT_DELIMITER):
    '''
    Write record_list to file
    '''
    # Check if list of records is not empty
    if len(record_list):
        # Build field list without identifier field
        field_list = [field for field in record_list[0].keys()
                      if field != id_field]
        # Sort field list
        field_list.sort()
        # Insert identifier field in the beginning of the list
        field_list.insert(0, id_field)
        output_file = open(fname, 'w')
        writer = csv.DictWriter(output_file, field_list,
                                delimiter=field_delimiter)
        header = {field: field for field in field_list}
        writer.writerow(header)
        for rec in record_list:
            writer.writerow(rec)
        output_file.close()


def calculate_statistics(in_file, id_field, delimiter=DEFAULT_DELIMITER,
                         confidence=DEFAULT_CONFIDENCE):
    '''
    Calculate confidence interval for a file
    '''
    data_dict = read_file(in_file, id_field, delimiter)
    rec_list = []
    for id_val in data_dict:
        rec = data_dict[id_val]
        rec.update_statistics(confidence)
        stat_rec = rec.get_error()
        stat_rec[id_field] = id_val
        rec_list.append(stat_rec)
    rec_list = sorted(rec_list, key=lambda k: k[id_field])
    return rec_list


def get_arguments():
    '''
    Get arguments
    '''
    import argparse
    parser = argparse.ArgumentParser('stats')
    parser.add_argument('-i', '--input', required=True,
                        help='Input CSV file')
    parser.add_argument('-k', '--key', required=True,
                        help='Key field')
    parser.add_argument('-o', '--output',
                        help='Output file')
    parser.add_argument('-d', '--delimiter',
                        help='Field delimiter',
                        default=DEFAULT_DELIMITER)
    parser.add_argument('-c', '--confidence', type=float,
                        help='Confidence to be used',
                        default=DEFAULT_CONFIDENCE)
    args = parser.parse_args()
    return args


def main():
    '''
    Main routine
    '''
    args = get_arguments()
    in_file = args.input
    id_field = args.key
    delimiter = args.delimiter
    confidence = args.confidence
    out_file = args.output
    rec_list = calculate_statistics(in_file, id_field, delimiter, confidence)
    if out_file is not None:
        write_file(out_file, id_field, rec_list, delimiter)


if __name__ == '__main__':
    main()
