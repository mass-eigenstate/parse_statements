import sys
import re
import datetime
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
            ## print(page.extract_text())

    list_lines = lines.split("\n")
    #
    #   Find the statement period in the form of two dates
    #
    for line in list_lines:
        #print(line)
        period = re.search(r"(\d{2}/\d{2}/20\d{2}) to(\d{2}/\d{2}/20\d{2})", line)
        #print(period)
        if period:
            start_string = period.group(1)
            end_string = period.group(2)
            # print(f"Start date: {start_string} End date: {end_string}")
            break
    
    start_date = date_from_string(start_string)
    end_date = date_from_string(end_string)
    # print(f"Start date: {start_date} End date: {end_date}")
    #
    #   Find the lines with transactions 
    #
    dep_types = [r"Deposit", r"Interest Payment", r"Transfer From", 
                 r"Surcharge Reimbursement", r"Debit Card Credit"] 
    with_types = [r"Web Pmt", r"Transfer To", r"Card Purchase", r"Withdrawal",
                  r"Direct Payment", r"Online.* Pmt", r"Ret Dep Item", 
                  r"POS Purchase", r"Fee", r"Zel To", r"Recurring Debit Card",
                  r"E-Check Check Pymt"]
    for line in list_lines:
        #print(f"{line} ") 
        transaction = re.search(r"^([0-1][0-9])/([0-3][0-9]) (([0-9]{1,3},?)+\.[0-9][0-9])(.*)$", line)
        if transaction: 
            month = int(transaction.group(1))
            day = int(transaction.group(2))
            #
            #  Only the month and date is provided. Statements with a start_date
            #  in December will have different years for December and January
            #  dates.
            #
            if start_date.month == 12: 
                year = start_date.year
            else: 
                year = end_date.year
            trans_date = datetime.date(year, month, day)
            trans_amount = float(transaction.group(3).replace(",",""))
            trans_desc = transaction.group(5)
            #
            #  Determine the type of transaction either deposit or withdrawal
            #
            # print(f"Amount: {transaction.group(3)}")
            type = 0 
            for dt in dep_types:
                if re.search(dt, trans_desc): type = 1
            for wt in with_types:
                if re.search(wt, trans_desc): type = -1 
            if type == 0: 
                print (f"Unable to determine transaction type: {trans_desc}")
            trans_amount = type*trans_amount
            print(f" Date: {trans_date} Amount: {trans_amount:9.2f} Description: {trans_desc}")

        elif re.search(r"^Daily Balance", line):
            break                               # There are no more transactions after Daily Balance
#
#  Check that filenames passed to the program exist. Return those that are good.
#
def validate_input(list):
    good_files = [] 
    for filename in list:
        if Path(filename).is_file():
            good_files.append(filename)

    return good_files
#
#   Parse a date string in the form mm/dd/yyyy and return a datetime.date object.
#
def date_from_string(string):
    dateparts = re.search(r"(\d{2})/(\d{2})/(\d{4})", string)
    if dateparts:
        year = int(dateparts.group(3))      # Datetime accepts integer arguments.
        month = int(dateparts.group(1))
        day = int(dateparts.group(2))
        return datetime.date(year, month, day)
    else:
        return None

if __name__ == "__main__": 
    main(sys.argv)

