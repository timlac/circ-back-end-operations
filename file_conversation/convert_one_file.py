import os
import subprocess
import logging

from config import ROOT_DIR

log_file_path = os.path.join(ROOT_DIR, "files/logs/ffmpeg_file.log")


logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s %(message)s')

input_file = os.path.join(ROOT_DIR, "files/test_files/A218_adm_p_1.mp4")
output_file = os.path.join(ROOT_DIR, "files/out/A218_adm_p_1.mp4")

command = ['ffmpeg', '-i', input_file, '-s', '1280x720', '-c:v', 'h264', '-c:a', 'aac', '-b:a', '192k', output_file]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

logging.info(result.stdout.decode('utf-8'))
logging.error(result.stderr.decode('utf-8'))
