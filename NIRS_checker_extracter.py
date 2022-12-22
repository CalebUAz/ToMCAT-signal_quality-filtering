import os
import sys
import pyxdf
import shutil
import argparse
from termcolor import colored

from utils import get_start_stop_time_from_xdf, dataframe_to_csv, create_time_distribution, str2bool

def read_xdf(xdf_file_paths, rootdir_baseline_task, rootdir_minecraft_data, subject_id, extract_pkl, extract_csv, exclude):
    """
    Read the XDF files.
    """
    columns = shutil.get_terminal_size().columns
    for path in xdf_file_paths:
        data, header = pyxdf.load_xdf(path)
        
        if exclude not in path:             
            if 'lion' in path: print(colored('Lion ', 'magenta', attrs=['bold', 'blink']).center(columns))
            elif 'leopard' in path: print(colored('Leopard ', 'magenta', attrs=['bold', 'blink']).center(columns))
            else: print(colored('Tiger ', 'magenta', 'on_blue', attrs=['bold', 'blink']).center(columns))

            for i in range(0,len(data)):
                if data[i]['info']['type'] == ['NIRS']:
                    print(
                    colored('[Status] Reading ', 'green', attrs=['bold']), 
                    colored(data[i]['info']['type'], 'blue'))
                    time_start_streams_nirs, time_end_streams_nirs = get_start_stop_time_from_xdf(data[i]) #get the unix time
                    time_distribution_human_readable_nirs, time_distribution_unix_nirs = create_time_distribution(time_start_streams_nirs, 
                                                                                time_end_streams_nirs, len(data[i]['time_series']))
                    dataframe_to_csv(path, data[i]['time_series'], 'NIRS', time_distribution_human_readable_nirs, 
                    time_distribution_unix_nirs, rootdir_baseline_task, rootdir_minecraft_data, subject_id, extract_pkl, extract_csv)

        else:
            print(
            colored('[Status] Skipping ', 'yellow', attrs=['bold']), 
            colored(exclude, 'red'))         

def look_for_XDF_files(rootdir_xdf, rootdir_baseline_task, rootdir_minecraft_data, subject_id, extract_pkl, extract_csv, exclude):
    """
    Walk through root directory, looking for the xdf files. 
    """
    xdf_file_paths = []
    for root, dirs, files in os.walk(rootdir_xdf):
        for file in files:
            if file.endswith(".xdf"):
                xdf_file_paths.append(os.path.join(root, file))
                print(
                    colored('[Status] xdf file found at ', 'green', attrs=['bold']), 
                    colored(os.path.join(root, file), 'blue'))
    
    read_xdf(sorted(xdf_file_paths), rootdir_baseline_task, rootdir_minecraft_data, subject_id, extract_pkl, extract_csv, exclude) #1. read all the XDF files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Post experiment script for xdf to csv file conversion"
    )
    parser.add_argument(
        "--p1",
        required=True,
        help="Path to the directory with the XDF files")

    parser.add_argument(
        "--p2", 
        required=True, 
        help="Enter the Path to folder with baseline task data")

    parser.add_argument(
        '--exclude',
        required=False,
        default=None,
        help="Enter iMAC name you'd like to exclude")

    parser.add_argument(
        '--filter',
        required=False,
        default=None,
        help="Enter True if you want to filter the siganl")

    arg = parser.parse_args()

    rootdir_xdf = arg.p1
    rootdir_baseline_task = arg.p2
    rootdir_minecraft_data = arg.p3
    subject_id = arg.s
    extract_pkl = arg.pkl
    extract_csv = arg.csv
    exclude  = str(arg.exclude)

    print(colored('[Status] Root Directory:', 'green', attrs=['bold']), colored(rootdir_xdf, 'blue'))
    sys.exit(look_for_XDF_files(rootdir_xdf, rootdir_baseline_task, rootdir_minecraft_data, subject_id, extract_pkl, extract_csv, exclude))