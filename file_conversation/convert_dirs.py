import glob
import os
import subprocess
import logging
from pathlib import Path

from metadata.error_file_exception import ErrorFileException
from metadata.file_metadata import Metadata
from config import ROOT_DIR, video_ids

log_file_path = os.path.join(ROOT_DIR, "files/logs/ffmpeg_dir.log")

logging.basicConfig(filename=log_file_path, level=logging.INFO, filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')


def change_extension(file, new_extension):
    filename_no_extension = Path(file).stem
    return filename_no_extension + new_extension


def process_file(filepath, output_path):
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
                   '-s', '1280x720',
                   '-c:v', 'h264',
                   '-c:a', 'aac',
                   '-b:a', '192k',
                   output_filepath]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(result.stdout.decode('utf-8'))
        logging.error(result.stderr.decode('utf-8'))


def main():
    # input_path = os.path.join(ROOT_DIR, 'files/test_files/**/*.mov')
    input_path = "/media/tim/Seagate Backup Plus Drive/for_validation_study/**/*.mov"

    output_path = os.path.join(ROOT_DIR, "files/out")
    files = glob.glob(input_path, recursive=True)

    intensity_levels = [2, 3]

    for filepath in files:
        if os.path.isfile(filepath):
            try:
                metadata = Metadata(Path(filepath).stem)

                if int(metadata.intensity_level) in intensity_levels or metadata.emotion_1_id == 22:

                    if metadata.video_id in video_ids:
                        # logging.info("processing file: {}".format(filepath))
                        process_file(filepath, output_path)
                    else:
                        logging.info("video id {} is not in validation video files list, skipping..."
                                     .format(metadata.video_id))

                else:
                    logging.info("file {} does not have any of intensity levels {}, skipping..."
                                 .format(filepath,
                                         str(intensity_levels)))
            except ErrorFileException as e:
                logging.info(e)
                continue

    logging.info("done")


if __name__ == "__main__":
    main()
