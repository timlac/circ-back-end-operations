from config import ROOT_DIR, valences
from service_handling.dynamo_handling.user_creation.plots import plot_emotion_distribution, plot_file_distribution, \
    plot_video_id_distribution
from service_handling.dynamo_handling.user_creation.user_video_allocation import get_objects_as_metadata

from collections import defaultdict
import json
import jsonpickle
import pprint
import os


def validate_emotion_subsets(user_pool):
    for idx, user_type in enumerate(user_pool):

        for user in user_type:

            emotions_id_subset0 = user[0]["emotions_id_subset"]

            for obj in user:

                if obj["emotions_id_subset"] != emotions_id_subset0:
                    print("emotions id subsets don't match")

                if len(obj["emotions_id_subset"]) != 11:
                    print("length is wrong")


def find_missing(user_pool):


    for idx, user_type in enumerate(user_pool):
        print("Seeking missing files for {} emotions".format(valences[idx]))

        samples = defaultdict(int)
        for user in user_type:
            for obj in user:
                filename = obj["item"]["filename"]
                samples[filename] += 1

        objects_metadata = get_objects_as_metadata(valences[idx])

        not_found = set()
        for obj in objects_metadata:
            if obj.filename not in samples:
                not_found.add(obj.filename)

        for filename in not_found:
            print(filename + " not found in samples")


def draw_plots(user_pool):
    for idx, user_type in enumerate(user_pool):
        print("plotting analysis for users with {} emotions".format(valences[idx]))
        plot_emotion_distribution(user_type)
        plot_video_id_distribution(user_type)
        plot_file_distribution(user_type)


def main():
    path = os.path.join(ROOT_DIR, "files/database_files/user_pool.json")

    # read file
    with open(path, 'r') as file:
        data = file.read()

    # parse file
    user_pool = json.loads(data)

    draw_plots(user_pool)

    find_missing(user_pool)

    # validate_emotion_subsets(user_pool)


if __name__ == "__main__":
    main()
