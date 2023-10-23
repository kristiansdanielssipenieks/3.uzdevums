import csv
from datetime import datetime as dt
import PyPDF2


def calculate_difference(file):
    if not file:
        return 0

    pdf_file = PyPDF2.PdfReader(open(file, "rb"))
    text1 = pdf_file.pages[0].extract_text()
    text2 = pdf_file.pages[1].extract_text()

    kWh_price = text2[text2.find(" kWh ") + 5:text2.find(" kWh ") + 11].replace(",", ".")
    kWhs = text1[text1.find("Elektroenerģijas patēriņš kopā: ") + 32:text1.find(" kWh")].replace(" ", "").replace(",",
                                                                                                                  ".")
    date = dt.strptime(text2[text2.find("Apjoms Mērv.") - 23:text2.find("Apjoms Mērv.") - 12].replace(" ", ""),
                       "%d.%m.%Y")

    total_hours = 0
    total_price = 0
    with open("nordpool.csv", "r") as f:
        nordpool = csv.reader(f, delimiter=',')
        next(nordpool)
        for row in nordpool:
            d1 = dt.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            d2 = dt.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            if date.year == d1.year and date.month == d1.month:
                hours = (d2.hour if d2.hour != 0 else 24) - d1.hour
                total_hours += hours
                total_price += float(row[2]) * hours

    avg_rate = round(total_price / total_hours * 1000) / 1000
    result = (float(kWh_price) - avg_rate) * float(kWhs)

    return round(result, 1) if result != 0 else 0


file_path = input()
try:
    print(calculate_difference(file_path))
except Exception as e:
    print(0)


