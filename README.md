![alt text][python] [![Twitter URL](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/saltycatfish)
# CSV-Blender
A python3 script that blends two csv files together, filling in data found in a source csv file that is missing in a merge file.

The script works by receiving two files; a source file and a merge file.

The merge file is the file which is missing values in its rows.  The source file is the file you believe contains some or all of those missing values.  CSV-Blender take each row from the merge file and compares it against each row in the source file, looking for a *KEY* match.  If CSV-Blender finds a match, it will copy any values found in the source file row into the merge file row based upon matching column header values.  **CSV-Blender does not overwrite pre-existing values.**  It will only fill in blank values.

> **IMPORTANT** Both merge and source files must contain one column with the header "KEY".  This will be used as the lookup to match merge file rows with source file rows.

CSV-Blender takes 4 positional arguments:
* **source file** - the path of the file that potentially contains values missing from the merge file.  
* **merge file** - the path of the file which is missing values that could be found in the source file.
* **output file** - the path of the file to write the final results to
* **log file** - the path of the file to write the log to

> **NOTE** CSV-Blender uses only native Python libraries.  There are no external dependecies.

## TODO
* Verify that the headers in the source file are all contained in the merge file.
* Option of overwriting pre-existing values in a merge file.

## Changelog

[python]: https://img.shields.io/badge/Python-3.4-blue.svg
