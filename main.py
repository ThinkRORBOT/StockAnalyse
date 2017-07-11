import candlestick
import scraper
import machineleaning

company_code = input("Please enter the code of the company: ")
s_date = input("PLease enter the start date of data: (####, ##(month), ##)")
e_date = input("PLease enter the end date of the data: ")

while True:
    print("Select the mode of the application")
    print("1: Generate Candlestick graph")
    print("2: Generate Correlation map")
    print("3: Generate buy, hold sell")
    a_mode = int(input("Please select application mode: "))

    if a_mode == 1:
        candlestick
    elif a_made == 2:
        scraper
    else:
        machineleaning
