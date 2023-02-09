import sys
import uuid
import pandas as pd
import jsonpickle
import json
import os
import logging
from config import ROOT_DIR

from service_handling.dynamo_handling.models.experiment_model import ExperimentModel
from service_handling.dynamo_handling.user_creation.user_video_allocation import set_items

log_file_path = os.path.join(ROOT_DIR, "files/logs/db_upload.log")

logging.basicConfig(filename=log_file_path, level=logging.INFO, filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')


# user_pool = set_items()

# frozen = jsonpickle.encode(user_pool)

# Writing to sample.json
# with open("user_pool.json", "w") as outfile:
#     outfile.write(frozen)


def upload(user_pool):
    alias_set = set()

    for i in range(5):
        logging.info("starting set {}".format(i))

        count = 0
        for user_type in user_pool:
            for user in user_type:
                alias = uuid.uuid4().hex

                randomization_id = count
                count += 1

                if alias in alias_set:
                    logging.info("Overlapping alias found: {}".format(alias))
                    while alias in alias_set:
                        alias = uuid.uuid4().hex

                alias_set.add(alias)

                for obj in user:
                    item = obj["item"]
                    emotions_id_subset = obj["emotions_id_subset"]

                    db_item = ExperimentModel(hash_key=alias,
                                              range_key=item["filename"],
                                              valence=item["emotion_1_valence"],
                                              video_id=item["video_id"],
                                              emotion_id=item["emotion_1_id"],
                                              emotion_options=emotions_id_subset,
                                              set_number=i,
                                              randomization_id=randomization_id)
                    try:
                        response = db_item.save()
                        logging.info(response)
                        logging.info("Saved file with alias: {alias} and filename: {filename}, "
                                     "with valence: {valence} and video_id {video_id},"
                                     "with emotion_id: {emotion_id} and emotion options {emotion_options}"
                                     "to set number {set_number} and randomization_id {randomization_id}"
                                     "".format(alias=alias,
                                               filename=db_item.filename,
                                               valence=db_item.valence,
                                               video_id=db_item.video_id,
                                               emotion_id=db_item.emotion_id,
                                               emotion_options=db_item.emotion_options,
                                               set_number=db_item.set_number,
                                               randomization_id=db_item.randomization_id))

                    except Exception as e:
                        print(e)


def main():
    path = os.path.join(ROOT_DIR, "files/database_files/user_pool.json")

    # read file
    with open(path, 'r') as file:
        data = file.read()

    # parse file
    user_pool = json.loads(data)

    upload(user_pool)


if __name__ == "__main__":
    main()
