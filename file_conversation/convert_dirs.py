import glob
import os
import subprocess
import logging
from pathlib import Path

from config import ROOT_DIR

log_file_path = os.path.join(ROOT_DIR, "files/logs/ffmpeg_dir.log")

logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def change_extension(file, new_extension):
    filename_no_extension = Path(file).stem
    return filename_no_extension + new_extension


input_path = os.path.join(ROOT_DIR, 'files/test_files/**/*.mov')
output_path = os.path.join(ROOT_DIR, "files/out")
files = glob.glob(input_path, recursive=True)

for filepath in files:
    if os.path.isfile(filepath):
        filename = Path(filepath).name
        new_filename = change_extension(filename, ".mp4")

        output_filepath = os.path.join(output_path, new_filename)
        if os.path.isfile(output_filepath):
            logging.info("file {} already exists, skipping...".format(output_filepath))
        else:
            # process the file
            logging.info("processing file: {}".format(filepath))

            command = ['ffmpeg',
                       '-i', filepath,
                       '-s', '854x480',
                       '-c:v', 'h264',
                       '-c:a', 'aac',
                       '-b:a', '192k',
                       output_filepath]

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info(result.stdout.decode('utf-8'))
            logging.error(result.stderr.decode('utf-8'))

logging.info("done")
