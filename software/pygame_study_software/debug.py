import csv


with open('./running_order_table.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

    print(rows[0])