import csv
from collections.abc import Generator


class CSVReader:
    """
    A class to read CSV files and yield their contents as lists of strings.

    Attributes:
        file_path (str): The path to the CSV file.
    """

    @staticmethod
    def read(file_path: str) -> Generator[dict[str, str], None, None]:
        """
        Reads the CSV file and yields its contents as lists of strings.

        Yields:
            list: A list of strings representing a row in the CSV file.
        """
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line in reader:
                yield line

'''
mycsv = CSVReader()
r = mycsv.read(".\\samples\\MOCK_DATA.csv")
for i in r:
    print(i)
'''
    