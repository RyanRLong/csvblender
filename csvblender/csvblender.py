#!/usr/bin/env python3

# Author      : Ryan Long

# Scans through a source file for any values missing in merge file based upon a column "KEY".
# Any missing values will be written to the outputfile along with the original values.  Values
# already present in the merge file will not be overwritten, even if the source file contains
# different information.

import sys
import csv
import logging
import argparse


class CSVBlender:
    """Main execution"""
    def __init__(self, logger=None):
        if logger == None:
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.NullHandler())
        else:
            self.logger = logger

    def csvToList(self, csvFilePath):
        """Coverts a csv file into a list of rows, with each row containing a
        dict containing keys as column names and values as field values"""
        outputList = []
        processedRowCount = 0
        self.logger.info("Converting file {} to dictionary...".format(csvFilePath))
        with open(csvFilePath, 'r') as csvFile:
            reader = csv.DictReader(csvFile, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
            for row in reader:
                outputList.append(row)
                processedRowCount += 1
            self.logger.info("Processed {} rows from file {}".format(processedRowCount, csvFilePath))
            return outputList

    def listToCsv(self, list, fieldnames, csvFilePath):
        """Converts a list of dictionaries into a csv file."""
        with open(csvFilePath, 'w') as outputFile:
                self.logger.info("Writing dictionary to file {}...".format(csvFilePath))
                writer = csv.DictWriter(
                    outputFile, fieldnames=fieldnames, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
                self.logger.info("Writing header to file {}...")
                writer.writeheader()
                count = 1
                for row in list:
                    self.logger.info("Writing row {} to file...".format(count))
                    count += 1
                    writer.writerow(row)

    def getFieldNames(self, csvFilePath):
        """Gets the fieldnames or column names from a csv file."""
        with open(csvFilePath, 'r') as reader:
            self.logger.info("Getting header information from {}".format(csvFilePath))
            reader = csv.DictReader(reader, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
            return reader.fieldnames

    def blendFiles(self, sourceFilePath, mergeFilePath, outputFilePath):
        """Blends two files together and writes the result to an output file.  The source file contains
        the data you wish to extract, while the merge file will be filled with data it is missing that
        exists in the source file."""
        sourceList = self.csvToList(sourceFilePath)
        mergeList = self.csvToList(mergeFilePath)
        fieldnames = self.getFieldNames(mergeFilePath)

        sourceRowCount = mergeRowCount = 0
        for mergeRow in mergeList:
            mergeRowCount += 1
            self.logger.info("Checking merge row {} ...".format(mergeRowCount))
            for sourceRow in sourceList:
                sourceRowCount += 1
                if mergeRow.get('KEY') == sourceRow.get('KEY'):
                    self.logger.info("Match found: blending merge: row {} key {} with source: row {} key {}...".format(
                        mergeRowCount, mergeRow['KEY'], sourceRowCount, sourceRow['KEY']))
                    mergeRow.update(sourceRow)
            sourceRowCount = 0

        self.listToCsv(mergeList, fieldnames, outputFilePath)

    def main(args=None):
        """Main execution"""
        parser = argparse.ArgumentParser(
            description='''
            CSVBlender searches for values missing from the merge file in the source
            using a KEY to match rows and identical column values to match field values.

            To use, ensure that each csv file has one column header labeled "KEY".  All
            column headers in source file must be present in merge file.
            '''
            )
        parser.add_argument(
            "sourceCSV",
            help="the file that contains the data you want lookup",
            metavar="source_csv"
            )
        parser.add_argument(
            "mergeCSV",
            help="the file that you wish to merge missing values form the source file with",
            metavar="merge_csv"
            )
        parser.add_argument(
            "outputCSV",
            help="the output file of the merge",
            metavar="output_csv"
            )
        parser.add_argument(
            "logFile",
            help="the path of the log file",
            metavar="log_file"
            )
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

        blender = CSVBlender(logger)
        blender.blendFiles(args.sourceCSV, args.mergeCSV, args.outputCSV)

if __name__ == '__main__':
    CSVBlender().main()
