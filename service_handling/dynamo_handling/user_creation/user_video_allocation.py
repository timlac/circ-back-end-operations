import math
import random
from collections import defaultdict
from copy import copy

import matplotlib.pyplot as plt
import uuid
import jsonpickle

from helpers import get_filename
from service_handling.dynamo_handling.emotion_randomization import get_emotion_ids_by_valence
from service_handling.dynamo_handling.get_bucket_contents import list_all_objects_in_bucket
from metadata.file_metadata import Metadata
from config import video_ids
from service_handling.dynamo_handling.user_creation.plots import plot_emotion_distribution, \
    plot_video_id_distribution
from service_handling.dynamo_handling.user_creation.plots import plot_file_distribution


def get_random_subset_emotion(my_list):
    my_list = copy(my_list)
    subset_length = 11
    return random.sample(my_list, subset_length)


def get_custom_replication(my_list, total_length):
    ret = []

    my_list = copy(my_list)

    replications = math.ceil(total_length / len(my_list))

    for i in range(replications):
        random.shuffle(my_list)
        ret.extend(my_list)

    return ret[:total_length]


def get_objects_as_metadata(valence):
    ret = []

    meta_list = []
    s3_objects = list_all_objects_in_bucket()
    for obj in s3_objects:
        filename = get_filename(obj["Key"])
        meta = Metadata(filename)
        if meta.emotion_1_valence == valence or meta.emotion_1_valence == "neu":
            meta_list.append(meta)

    for i in range(8):
        random.shuffle(meta_list)
        ret.extend(meta_list)

    return ret


def set_items():
    user_pool = []

    for valence in ["pos", "neg"]:

        # e.g. positive or negative type
        user_type = []

        objects_metadata = get_objects_as_metadata(valence)
        emotions = get_emotion_ids_by_valence(valence)

        # 125 instances of each user_type
        for idx in range(125):
            print(idx)

            user = []

            random.shuffle(objects_metadata)

            emotions_subset = get_random_subset_emotion(emotions)
            emotion_pool = get_custom_replication(emotions_subset, total_length=132)
            video_pool = get_custom_replication(video_ids, total_length=132)

            rejects = 0

            # add items to the user while emotion pool is not exhausted
            while emotion_pool:
                if rejects > len(objects_metadata):
                    video_pool = get_custom_replication(video_ids, total_length=len(video_pool))

                item = random.choice(objects_metadata)
                if item.emotion_1_id in emotion_pool and item.video_id in video_pool:

                    user.append({"item": copy(item),
                                  "emotions_id_subset": copy(emotions_subset)})
                    objects_metadata.remove(item)
                    emotion_pool.remove(item.emotion_1_id)
                    video_pool.remove(item.video_id)

                else:
                    rejects += 1

            user_type.append(user)

        user_pool.append(user_type)

    return user_pool


def main():
    user_pool = set_items()

    frozen = jsonpickle.encode(user_pool)

    # Writing to sample.json
    with open("user_pool.json", "w") as outfile:
        outfile.write(frozen)


if __name__ == "__main__":
    main()
