from back_end.dynamo_handling.get_bucket_contents import get_bucket_contents
from back_end.metadata.file_metadata import Metadata
from back_end.helpers import get_filename
from back_end.dynamo_handling.models.example_model import ExampleModel


def add_example_videos(emotion_ids):
    counter = 0

    for key in get_bucket_contents():
        print(key)

        if counter >= 3:
            break

        filename = get_filename(key)
        metadata = Metadata(filename)

        if int(metadata.intensity_level) != 3:
            continue

        if metadata.emotion_1_id in emotion_ids:
            print("valence")
            print(metadata.emotion_1_valence)
            item = ExampleModel(hash_key=counter,
                                range_key=metadata.emotion_1_valence,
                                filename=metadata.filename,
                                video_id=metadata.video_id,
                                emotion_id=metadata.emotion_1_id
                                )
            item.save()
            counter += 1


positive_emotions = {
    # happiness/joy
    33,
    # concentration
    27,
    # positive surprise
    9
}

negative_emotions = {
    # disgust
    35,
    # anger
    12,
    # sadness
    6
}

add_example_videos(positive_emotions)
add_example_videos(negative_emotions)
