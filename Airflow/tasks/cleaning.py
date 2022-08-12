#!/usr/bin/env python3

import argparse
import os
import pathlib
import shutil

def preprocess():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', type=str, help='folder to save all of downloaded csv')
    parser.add_argument('output_folder', type=str, help='folder to save all of data csv')
    return parser.parse_args()

def main():
    args = preprocess()
    os.makedirs(args.output_folder, exist_ok=True)
    path = pathlib.Path(args.input_folder)
    for path_obj in path.glob('**/API_*.csv'):
        filename = path_obj.name
        path = str(path_obj)
        print(filename)
        shutil.move(path, os.path.join(args.output_folder,filename))
        meta_files = path.replace(filename, "*"+ filename)
        os.system("rm " + meta_files)

if __name__ == "__main__":
    main()