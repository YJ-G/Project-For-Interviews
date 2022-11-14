import unittest
import pandas as pd
import os
from Combiner import Combiner
import logging

class TestCsvCombiner(unittest.TestCase):

    def test_normal_input(self):
        """inputs are normal input files that have right formats"""

        files = ["fixtures/accessories.csv", 'fixtures/clothing.csv', 'fixtures/household_cleaners.csv']
        c = Combiner()
        c.combine(files)
        df = pd.read_csv('combined_file.csv')
        self.assertTrue(len(df) == len(pd.read_csv("fixtures/accessories.csv")) +
                        len(pd.read_csv("fixtures/clothing.csv")) +
                        len(pd.read_csv("fixtures/household_cleaners.csv")))
        self.assertTrue(df.columns[2] == "filename")

    def test_file_not_exist(self):
        """testing when inputs include files that don't exist """

        files = ["fixtures/filedoesntexsit.csv", "fixtures/accessories.csv"]
        c = Combiner()
        c.combine(files)
        df = pd.read_csv('combined_file.csv')
        self.assertTrue(len(df) == len(pd.read_csv("fixtures/accessories.csv")))

    def test_file_not_csv(self):
        """testing when inputs include files that aren't .csv """

        files = ["fixtures/notcsv.txt", "fixtures/accessories.csv"]
        c = Combiner()
        c.combine(files)
        df = pd.read_csv('combined_file.csv')
        self.assertTrue(len(df) + 1 == len(pd.read_csv("fixtures/accessories.csv")))

    def test_empty_file(self):
        """testing when inputs include empty .csv files"""

        files = ["fixtures/empty.csv", "fixtures/accessories.csv"]
        c = Combiner()
        c.combine(files)
        df = pd.read_csv('combined_file.csv')
        self.assertTrue(len(df) == len(pd.read_csv("fixtures/accessories.csv")))

    def test_different_file(self):
        """testing when inputs include different .csv files"""

        files = ["fixtures/accessories.csv", "fixtures/differentfile.csv"]
        c = Combiner()
        c.combine(files)
        df = pd.read_csv('combined_file.csv',  sep='delimiter')
        self.assertTrue(len(df) == len(pd.read_csv("fixtures/accessories.csv")) +
                        len(pd.read_csv("fixtures/differentfile.csv")))

    def test_no_input(self):
        """testing when input is empty"""

        files = []
        c = Combiner()
        c.combine(files)
        self.assertTrue(not os.path.exists('combined_file.csv'))

    if __name__ == '__main':
        unittest.main(exit=False)
