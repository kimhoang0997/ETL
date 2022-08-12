#!/usr/bin/env python3

import argparse
import pathlib
import os
from zipfile import ZipFile

def preprocess():
    parser = argparse.ArgumentParser()
    parser.add_argument('zip_folder', type=str, help='folder to save downloaded zip file')
    parser.add_argument('unzip_folder', type=str, help='folder to save all of downloaded csv')
    return parser.parse_args()

def main():
    args = preprocess()
    path = pathlib.Path(args.zip_folder)
    zipfiles = []
    for name in path.glob('**/*.zip'):
      zipfiles.append(name)

    for zipfile in zipfiles: 
      try:
        with ZipFile(zipfile, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            print(zipfile)
            zipObj.extractall(args.unzip_folder)
        os.remove(zipfile)
      except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()