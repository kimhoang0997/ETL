#!/usr/bin/env python3
from influxdb import InfluxDBClient
import pathlib
import argparse
import os


# You can generate an API token from the "API Tokens Tab" in the UI
# url="http://localhost:8088"
# csv_folder="output"
# database = "worldbank"


def preprocess():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_folder', type=str, help='input folder contain world bank csv file')
    parser.add_argument('database', type=str, help='the database name to store data')
    return parser.parse_args()


def main():
    args = preprocess()
    csv_folder = args.csv_folder
    database = args.database
    path = pathlib.Path(csv_folder)
    for pathfile in path.glob('**/*.csv'):
        client = InfluxDBClient(host='localhost', port=8086, database=database)
        print(os.path.basename(pathfile))
        with open(pathfile) as csv_file:
            points = []
            years = []
            lines = csv_file.readlines()
            for index, line in enumerate(lines):
                cells = line.strip().split('","')
                if index == 2:
                    date_in_string = cells[1].replace('",', "")
                    last_update_value = date_in_string
                elif index == 4:
                    years_in_string = cells[4:]
                    for year in years_in_string:
                        year = year.replace('",', "")
                        years.append(year)
                elif index > 4:
                    country_name = cells[0].replace('"','')
                    country_code = cells[1]
                    indicator_name = cells[2]
                    indicator_code= cells[3]
             
                    for jndex, year in enumerate(years):
                        value_in_string = cells[4 + jndex].replace('"','').replace(",","")
                        if value_in_string:
                            point = {}
                            point["measurement"] = indicator_code
                            point["tags"] = {
                                'country_name': country_name,
                                'country_code': country_code,
                                'indicator_code': indicator_code,
                                'indicator_name': indicator_name,
                                'last_update_value': last_update_value
                            }
                            value = float(value_in_string)
                            point["fields"] = {"value": value}
                            point["time"] = year + "-01-01T00:00:00Z"
                            points.append(point)
        client.write_points(points)
        client.close()
        os.remove(pathfile)




if __name__ == "__main__":
    main()