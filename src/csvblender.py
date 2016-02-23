# Author    : Ryan Long
# Created   : 12/9/2015
# Last Mod  :
# Version   : 1.0

# Parses a csv file and outputs the results into a destination csv file

import sys
import csv
import logging
import argparse
import importlib
#import csv_rules.test_rules


def main():
    """ Main execution """
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename='log.txt', filemode='w', level=logging.DEBUG)

    # setup arg parsers
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", help="the csv file you want to parse")
    parser.add_argument(
        "output_csv", help="the destination of the csv file to write to")
    parser.add_argument(
        "rules", help="the rules module used to parse the csv file (ie - csv_rules.test_rules)")
    parser.add_argument("logfile", help="the path of the log file")
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create file handler
    handler = logging.FileHandler(args.logfile, "w", encoding=None, delay=True)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # try to import rules module
    try:
        rules_module = importlib.import_module(args.rules)
    except:
        logger.exception(
            "The package.module \"%s\" could not be opened or is missing", args.rules)
        sys.exit(1)
    rules = rules_module.Rules(logger)

    try:
        logger.debug("Opening input file")
        with open(args.input_csv, 'r') as input_file:
            reader = csv.DictReader(input_file)
            logger.debug("Opening output file")
            with open(args.output_csv, 'w') as output_file:
                writer = csv.DictWriter(
                    output_file, fieldnames=reader.fieldnames, dialect='excel', lineterminator='\n', quoting=csv.QUOTE_ALL)
                writer.writeheader()
                logger.debug("Begin processing rows")
                for row in reader:
                    logger.info("Processing row: " + str(reader.line_num))
                    rules.transform_row(row)
                    writer.writerow(row)
        logger.info("Total changes made: %i", rules.get_changes_quantity())

    except PermissionError:
        logger.exception(
            "Check the files referenced are not open or being used by another process")
        sys.exit(1)
    except FileNotFoundError:
        logger.exception("The file \"%s\" could not be found", args.input_csv)
        sys.exit(1)

if __name__ == '__main__':
    main()
