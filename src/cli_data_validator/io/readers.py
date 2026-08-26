import csv
from typing import Generator

class CSVReader:
    """
    A class to read CSV files and yield their contents as lists of strings.

    Attributes:
        file_path (str): The path to the CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the CSVReader with the given file path.

        Args:
            file_path (str): The path to the CSV file.
        """
        self.file_path = file_path

    def read(self) -> Generator[list[str], None, None]:
        """
        Reads the CSV file and yields its contents as lists of strings.

        Yields:
            list: A list of strings representing a row in the CSV file.
        """
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                yield line

'''
mycsv = CSVReader("C:\\Users\\Luiz Henrique\\Documents\\Python\\cli-data-validator\\samples\\MOCK_DATA.csv")
r = mycsv.read()
for i in r:
    print(i)
'''