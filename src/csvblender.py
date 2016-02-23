#!/usr/bin/env python3

# Author      : Ryan Long
# Created    :  2016-02-23
# Last Mod  :   test
# Version     :   1.0

# Scans through a source file for any values missing in merge file based upon a column "KEY".
# Any missing values will be written to the outputfile along with the original values.  Values
# already present in the merge file will not be overwritten, even if the source file contains
# different information.

import sys
import csv
import logging
import argparse


def main():
    """Main execution"""
    def csvToList(csvFilePath):
        """Coverts a csv file into a list of rows, with each row containing a
        dict containing keys as column names and values as field values"""
        outputList = []
        processedRowCount = 0
        try:
            logger.info("Converting file {} to dictionary...".format(csvFilePath))
            with open(csvFilePath, 'r') as csvFile:
                reader = csv.DictReader(csvFile, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
                for row in reader:
                    outputList.append(row)
                    processedRowCount += 1
                logger.info("Processed {} rows from file {}".format(processedRowCount, csvFilePath))
                return outputList
        except PermissionError:
            logger.exception("Check the files referenced are not open or being used by another process")
            sys.exit(1)
        except FileNotFoundError:
            logger.exception("The file \"%s\" could not be found", args.input_csv)
            sys.exit(1)

    def listToCsv(list, fieldnames, csvFilePath):
        """Converts a list of dictionaries into a csv file."""
        with open(csvFilePath, 'w') as outputFile:
                logger.info("Writing dictionary to file {}...".format(csvFilePath))
                writer = csv.DictWriter(
                    outputFile, fieldnames=fieldnames, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
                logger.info("Writing header to file {}...")
                writer.writeheader()
                count = 1
                for row in list:
                    logger.info("Writing row {} to file...".format(count))
                    count += 1
                    writer.writerow(row)

    def getFieldNames(csvFilePath):
        """Gets the fieldnames or column names from a csv file."""
        with open(csvFilePath, 'r') as reader:
            logger.info("Getting header information from {}".format(csvFilePath))
            reader = csv.DictReader(reader, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
            return reader.fieldnames

    def blendFiles(sourceFilePath, mergeFilePath, outputFilePath):
        """Blends two files together and writes the result to an output file.  The source file contains
        the data you wish to extract, while the merge file will be filled with data it is missing that
        exists in the source file."""
        sourceList = csvToList(sourceFilePath)
        mergeList = csvToList(mergeFilePath)
        fieldnames = getFieldNames(mergeFilePath)
        sourceRowCount = mergeRowCount = 0

        for mergeRow in mergeList:
            mergeRowCount += 1
            logger.info("Checking merge row {} ...".format(mergeRowCount))
            for sourceRow in sourceList:
                sourceRowCount += 1
                if mergeRow.get('KEY') == sourceRow.get('KEY'):
                    logger.info("Match found: blending merge: row {} key {} with source: row {} key {}...".format(
                        mergeRowCount, mergeRow['KEY'], sourceRowCount, sourceRow['KEY']))
                    mergeRow.update(sourceRow)
            sourceRowCount = 0

        listToCsv(mergeList, fieldnames, outputFilePath)

    # setup arg parsers
    parser = argparse.ArgumentParser()
    parser.add_argument("sourceCSV", help="the file that contains the data you want lookup")
    parser.add_argument(
        "mergeCSV", help="the file that you wish to merge missing values form the source file with")
    parser.add_argument("outputCSV", help="the output file of the merge")
    parser.add_argument("logFile", help="the path of the log file")
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

    blendFiles(args.sourceCSV, args.mergeCSV, args.outputCSV)

if __name__ == '__main__':
    main()
