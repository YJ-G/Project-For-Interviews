import os
import pandas as pd
import logging
import argparse

file_path = 'combined_file.csv'


class Combiner:
    """A class that merge multiple .csv file into one single file and add filename column"""

    def __init__(self):
        self.header = True

    def add_new_column(self, df, basename):
        """ add <filename> column

        :param
        - df: the dataframe to be processed
        - basename: the basename for the input dataframe
        """

        filename = [basename for x in range(0, len(df))]
        df['filename'] = filename
        logging.info(f"column added for file {basename}")

    def verify_files(self, input_csvs):
        """ verify input formats and return all existed non-empty '.csv' file

        :param
        - input_csvs: the files to be verified

        :return
        - (list) all existed non-empty '.csv' file
        """
        logging.info("==================================================> verification begins")
        if len(input_csvs) < 1:
            logging.warning("The input is empty.")
        files = []
        for csv in input_csvs:
            logging.info(f"verification for {csv} begins")
            if not os.path.exists(csv):
                logging.warning(f"File not found: {csv}")
            elif '.csv' not in csv:
                logging.warning("not .csv file")
            elif os.path.getsize(csv) == 0:
                logging.warning(f"File is empty: {csv} ")
            else:
                files.append(csv)
            logging.info(f"verification for {csv} ends")
        logging.info("==================================================> verification ends")
        return files

    def output(self, csv, chunk_size, verbose):
        """ read files in chunks and output to .csv file/stdout in chunks to be able to combine large files.

        :param
        - csv: the files to be output
        - chunk_size: the size of chunks in which reading from files/outputting
        """
        logging.info(f"output begins for {csv} ends in chunk size of {chunk_size}")
        for df in pd.read_csv(csv, chunksize=chunk_size):
            base = os.path.basename(csv)
            self.add_new_column(df, base)
            df.columns = [col.lower() for col in df.columns]
            df.to_csv(file_path, index=False, header=self.header, chunksize=chunk_size, mode='a')
            stdout_combined_csv = df.to_csv(index=False, header=self.header, chunksize=chunk_size, mode='a')
            if verbose:
                print(stdout_combined_csv, end="")
            self.header = False
        logging.info(f"output ends for {csv} ends in chunk size of {chunk_size}")

    def combine(self, input_csvs, verbose=True):
        """ verify inputs, combine files and output to stdout and .csv file

        :param
        - input_csvs: the files to be combined
        """
        files = self.verify_files(input_csvs)
        if os.path.exists(file_path):
            os.remove(file_path)
        chunk_size = 10 ** 7
        logging.info("==================================================> files merging begins")
        for file in files:
            self.output(file, chunk_size, verbose)
        self.header = True
        logging.info("==================================================> files merging ends")


def main():
    parser = argparse.ArgumentParser(description="A CSV combiner")
    parser.add_argument("-f", "--files", nargs="+", type=str, metavar="", required=True,
                        help="CSV files to be combined, can't be empty")
    parser.add_argument("-v", "--verbose", action="store_true", help="set logging level to INFO")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    combiner = Combiner()
    combiner.combine(args.files)


if __name__ == '__main__':
    main()
