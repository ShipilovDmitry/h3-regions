
import csv

FILENAME_RUSSIA = 'average_russia_7.csv'
FILENAME_CITY = 'cells-kazan-7.txt'
FILENAME_RESULT = 'elevation-kazan-7.csv'

def process_files(city, country, result):
    with open(city, 'r') as city_file, open(country, 'r') as country_file, open(result, 'w', newline='') as result_file:
        file1_lines = set(city_file.read().splitlines())  # Read all lines from file1 into a set for faster lookup
        csv_reader = csv.reader(country_file)
        csv_writer = csv.writer(result_file)

        for row in csv_reader:
            if row[0] in file1_lines:  # Check if the first field of the row exists in file1_lines
                csv_writer.writerow(row)  # Write the whole row to file3

process_files(FILENAME_CITY, FILENAME_RUSSIA, FILENAME_RESULT)
