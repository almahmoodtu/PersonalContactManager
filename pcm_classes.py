'''---------------------------------
PERSONAL CONTACT MANAGER (PCM)
THIS FILE CONTAINS - CLASSES
---------------------------------'''

import csv
from csv import DictWriter


class DataSource:
    '''This helps to read and update CSV files using dictionaries'''


    def __init__(self, name: str, file_name: str, fields: list, sort_by: str) -> None:
        '''Defining variables used throughout the class'''
        self.name = name
        self.file_name = file_name
        self.fields = fields
        self.sort_by = sort_by
        self.delimiter = ';'
        self.data_dictionary = {}


    def csv_to_dictionary(self) -> dict:
        '''Extracting data from a CSV file into a dictionary'''
        with open(self.file_name, 'r') as file:
            csv_file = csv.DictReader(file, delimiter=self.delimiter)
            index = 1
            for row in csv_file:
                self.data_dictionary[index] = dict(row)
                index += 1
        self.data_dictionary = dict(sorted(self.data_dictionary.items(),
                                           key=lambda element: element[1][self.sort_by]))
        return self.data_dictionary


    def csv_update_preparation(self, data: list) -> dict:
        '''Combine field list with data into a dictionary'''
        result = {}
        for x in range(len(self.fields)):
            result[self.fields[x]] = data[x]
        return result


    def csv_add_row(self, data: dict) -> None:
        '''Add a row (dictionary entry) to the last row of CSV (used for ADD RECORD)'''
        with open(self.file_name, 'a+', newline='') as file:
            dict_writer = DictWriter(file,
                                     fieldnames=self.fields, delimiter=self.delimiter)
            dict_writer.writerow(data)


    def csv_overwrite(self, data: dict) -> None:
        '''Overwrite CSV with updated dictionary (used for EDIT/DELETE RECORD)'''
        with open(self.file_name, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file,
                                         fieldnames=self.fields, delimiter=self.delimiter)
            dict_writer.writeheader()
            for value in data.values():
                dict_writer.writerow(value)