from back_end.dynamo_handling.get_bucket_contents import get_bucket_contents
from back_end.metadata.file_metadata import Metadata
from back_end.dynamo_handling.models.experiment_model import ExperimentModel
from back_end.helpers import get_filename


def add_user(alias, valence, intensities, modes):
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

        if metadata.emotion_1_id not in added_emotions:
            print("adding item")

            item = ExperimentModel(hash_key=alias,
                                   range_key=metadata.filename,
                                   valence=metadata.emotion_1_valence,
                                   video_id=metadata.video_id,
                                   emotion_id=metadata.emotion_1_id)
            item.save()
            added_emotions.add(metadata.emotion_1_id)

            counter += 1

        if len(added_emotions) == 43:
            added_emotions = set()


add_user("Tim",
         "pos",
         {2, 4},
         {"p"})
