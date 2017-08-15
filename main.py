import candlestick
import scraper
import machineleaning
import help


company_code = input("Please enter the code of the company: ")

while True:
    print("Select the mode of the application")
    print("1: Generate Candlestick graph")
    print("2: Generate Correlation map")
    print("3: Generate buy, hold sell")
    print("4: Help")
    a_mode = int(input("Please select application mode: "))

    if a_mode == 1:
        candlestick.candlestick(company_code)
    elif a_mode == 2:
        scraper
    elif a_mode == 3:
        machineleaning
    else:
        help.readfile()
