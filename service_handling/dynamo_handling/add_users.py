import collections

from service_handling.dynamo_handling.get_bucket_contents import get_bucket_contents, list_all_objects_in_bucket
from metadata.file_metadata import Metadata
from service_handling.dynamo_handling.models.experiment_model import ExperimentModel
from helpers import get_filename
from service_handling.dynamo_handling.emotion_randomization import get_emotion_ids_by_valence, \
    get_random_subset_emotion, get_video_ids

from config import emotion_id_to_emotion_abr

from collections import defaultdict
import matplotlib.pyplot as plt

# TODO: Equal distribution of emotions, of gender, vocal mode, and näro and meli


def iter_emotions(valence):

    sampled_emotions = defaultdict(int)

    emotion_ids_val = get_emotion_ids_by_valence(valence)

    for k in range(100):

        for i in emotion_ids_val:
            emotion_ids_subset = get_random_subset_emotion(emotion_ids_val, 11)

            for j in emotion_ids_subset:

                emotion_abr = emotion_id_to_emotion_abr[j]

                sampled_emotions[emotion_abr] += 1

    print(sampled_emotions)
    print(len(sampled_emotions))

    plt.bar(sampled_emotions.keys(), sampled_emotions.values(), color='g')
    plt.xticks(rotation=90)

    plt.show()


def algorithm(valence):
    emotion_ids_val = get_emotion_ids_by_valence(valence)
    emotion_ids_subset = get_random_subset_emotion(emotion_ids_val, 11)

    video_ids = get_video_ids()

    added_emotions = defaultdict(int)
    added_video_ids = defaultdict(int)
    counter = 0

    for obj in list_all_objects_in_bucket():

        counter += 1

        filename = get_filename(obj["Key"])

        metadata = Metadata(filename)

        if metadata.video_id in video_ids and metadata.emotion_1_id in emotion_ids_subset:
            added_emotions[metadata.emotion_1_id] += 1
            added_video_ids[metadata.video_id] += 1
            emotion_ids_subset.remove(metadata.emotion_1_id)
            video_ids.remove(metadata.video_id)

    print(counter)
    print(added_video_ids)

    print(len(added_video_ids))
    sorted_dict = sorted(added_video_ids.items(), key=lambda x: x[0])

    labels, values = zip(*sorted_dict)

    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.show()

    plt.bar(added_emotions.keys(), added_emotions.values(), color='g')
    plt.xticks(rotation=90)
    plt.show()

    print(added_emotions)

    print(len(added_emotions))

algorithm("pos")









def add_user(alias, valence, intensities, modes):
    emotion_ids_val = get_emotion_ids_by_valence(valence)
    emotion_ids_subset = get_random_subset_emotion(emotion_ids_val, 11)

    print("Adding user: " + alias)

    counter = 0
    added_emotions = set()

    for key in get_bucket_contents():
        if counter > 99:
            break

        filename = get_filename(key)

        metadata = Metadata(filename)

        if int(metadata.intensity_level) not in intensities:
            continue

        if metadata.mode not in modes:
            continue

        if metadata.emotion_1_id not in emotion_ids_subset:
            continue

        if metadata.emotion_1_id not in added_emotions:

            # item = ExperimentModel(hash_key=alias,
            #                        range_key=metadata.filename,
            #                        valence=metadata.emotion_1_valence,
            #                        video_id=metadata.video_id,
            #                        emotion_id=metadata.emotion_1_id,
            #                        emotion_options=emotion_ids_subset)
            try:
                # response = item.save()
                # print(response)
                added_emotions.add(metadata.emotion_1_id)
                counter += 1
            except Exception as e:
                print(e)

        if len(added_emotions) == len(emotion_ids_subset):
            added_emotions = set()







# def add_users(users):
#     valences = ["pos", "neg"]
#     for alias in users:
#         for valence in valences:
#             add_user(alias + valence,
#                      valence,
#                      {1, 2, 3, 4},
#                      {"p", "v"}
#                      )
#
#
# users = ["Alexandra_"]
#
# # users = ["test"]
# add_users(users)

