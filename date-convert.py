import csv
from datetime import datetime

input_file = "fuel_price_US.csv"
output_file = "fuel_price_US_ordered.csv"
date_column = "observation_date"
date_format = "%Y-%m-%d" #"%Y-%m-%d %H:%M:%S"

with open(input_file, mode="r", encoding="utf-8-sig", newline="") as infile:
    reader = csv.reader(infile)

    # Read and clean headers
    raw_headers = next(reader)
    headers = [h.strip().strip('"').strip() for h in raw_headers]

    # Find the index of the MonthYear column
    date_idx = headers.index(date_column)

    rows = []
    for row in reader:
        if not row:
            continue
        date_str = row[date_idx].strip().strip('"')
        dt = datetime.strptime(date_str, date_format)
        decimal_year = round(dt.year + (dt.month - 1) / 12.0, 4)

        # Overwrite the original date value in the existing row
        row[date_idx] = str(decimal_year)
        rows.append(row)

with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers)
    writer.writerows(rows)