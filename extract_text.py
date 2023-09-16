import sys
import re
from pathlib import Path
from PyPDF2 import PdfReader

#
# Regex for a month date at the beginning of a line /^[0-1][0-9]\/[0-3][0-9]
#
# Regex for a number with , separating evry three digits and two digits after
# the decimla point
#                    ([0-9]{1,3},?)+\.[0-9][0-9]
#  
def main(argv):

    file_list = []
    lines = ""
    if len(argv) == 1:
    #
    #  No files were passed
    #     
        print("No files given to analyze. Analyzing the example.\n")
        file_list.append("example.pdf")
    elif len(argv) > 1:
        file_list = validate_input(argv[1:])

    for filename in file_list: 
        reader = PdfReader(filename)
        for page in reader.pages:  ## pages is a list like object
            lines += page.extract_text()
            print(page.extract_text())

#
#  Check that filenames passed to the program exist. Return those that are good.
#
def validate_input(list):
    good_files = [] 
    for filename in list:
        if Path(filename).is_file():
            good_files.append(filename)

    return good_files



if __name__ == "__main__": 
    main(sys.argv)

