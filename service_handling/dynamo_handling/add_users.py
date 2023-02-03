import pynamodb

from service_handling.dynamo_handling.get_bucket_contents import get_bucket_contents
from service_handling.metadata.file_metadata import Metadata
from service_handling.dynamo_handling.models.experiment_model import ExperimentModel
from service_handling.helpers import get_filename
from service_handling.dynamo_handling.emotion_randomization import get_emotion_ids_by_valence, get_random_subset


def add_user(alias, valence, intensities, modes):
    emotion_ids_val = get_emotion_ids_by_valence(valence)
    emotion_ids_subset = get_random_subset(emotion_ids_val, 11)

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

            item = ExperimentModel(hash_key=alias,
                                   range_key=metadata.filename,
                                   valence=metadata.emotion_1_valence,
                                   video_id=metadata.video_id,
                                   emotion_id=metadata.emotion_1_id,
                                   emotion_options=emotion_ids_subset)
            try:
                response = item.save()
                print(response)
                added_emotions.add(metadata.emotion_1_id)
                counter += 1
            except Exception as e:
                print(e)

        if len(added_emotions) == len(emotion_ids_subset):
            added_emotions = set()


def add_users(users):
    valences = ["pos", "neg"]
    for alias in users:
        for valence in valences:
            add_user(alias + valence,
                     valence,
                     {1, 2, 3, 4},
                     {"p", "v"}
                     )


users = ["Alexandra_"]

# users = ["test"]
add_users(users)

