#!/usr/bin/env python3

# Author      : Ryan Long
# Created    :  2016-02-23
# Last Mod  :   test
# Version     :   1.0

# Parses a csv file and outputs the results into a destination csv file

import sys
import csv
import logging
import argparse


def main():
    """ Main execution """
    def csvToList(csv_file_path):
        output_list = []
        processed_row_count = 0
        try:
            logger.info("Converting file {} to dictionary...".format(csv_file_path))
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
                for row in reader:
                    output_list.append(row)
                    processed_row_count += 1
                logger.info("Processed {} rows from file {}".format(processed_row_count, csv_file_path))
                return output_list
        except PermissionError:
            logger.exception("Check the files referenced are not open or being used by another process")
            sys.exit(1)
        except FileNotFoundError:
            logger.exception("The file \"%s\" could not be found", args.input_csv)
            sys.exit(1)

    def listToCsv(list, fieldnames, csv_file_path):
        with open(csv_file_path, 'w') as output_file:
                logger.info("Writing dictionary to file {}...".format(csv_file_path))
                writer = csv.DictWriter(
                    output_file, fieldnames=dict['fieldnames'], dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                count = 1
                for row in dict['data']:
                    logger.info("Writing row {} to file...".format(count))
                    count += 1
                    writer.writerow(row)

    def getFieldNames(csv_file_path):
        with open(csv_file_path, 'r') as reader:
            logger.info("Getting header information from {}".format(csv_file_path))
            reader = csv.DictReader(csv_file_path, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
            return reader.fieldnames

    def blendFiles(source_file_path, merge_file_path, output_file_path):
        source_list = csvToList(source_file_path)
        merge_list = csvToList(merge_file_path)
        fieldnames = getFieldNames(merge_file_path)

        source_row_count = merge_row_count = 0
        for merge_row in merge_list:
            merge_row_count += 1
            logger.info("Checking merge row {} ...".format(merge_row_count))
            for source_row in source_list:
                source_row_count += 1
                if merge_row.get('KEY') == source_row.get('KEY'):
                    logger.info("Match found: blending merge: row {} key {} with source: row {} key {}...".format(merge_row_count, merge_row['KEY'], source_row_count, source_row['KEY']))
                    merge_row.update(source_row)
            source_row_count = 0
        listToCsv(merge_list, fieldnames, output_file_path)

    # setup arg parsers
    parser = argparse.ArgumentParser()
    parser.add_argument("source_csv", help="the file that contains the data you want lookup")
    parser.add_argument(
        "merge_csv", help="the file that you wish to merge missing values form the source file with")
    parser.add_argument("output_csv", help="the output file of the merge")
    parser.add_argument("log_file", help="the path of the log file")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename='log.txt', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create file handler
    handler = logging.FileHandler("log.txt", "w", encoding=None, delay=True)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    blendFiles(args.source_csv, args.merge_csv, args.output_csv)

if __name__ == '__main__':
    main()
