import random

from config import emotion_id_to_valence, video_files, video_ids


class EmotionSubsetHandler:
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def get_sample(self):

        # Pick 5 elements from the list randomly
        subset = random.sample(self.data, 5)

        print(subset)






def get_random_subset_emotion(my_list, subset_length):
    ret = []
    subset = random.sample(my_list, subset_length)
    for i in range(13):
        ret.extend(subset)
    ret = ret[:133]
    print(len(ret))
    return ret


def get_video_ids():
    ret = []
    for i in range(5):
        ret.extend(video_ids)
    random.shuffle(ret)
    ret = ret[:133]
    print(len(ret))

    return ret


def get_balanced_subset_sex():
    female_video_ids = [d['video_id'] for d in video_files if d['sex'] == 'female']
    male_video_ids = [d['video_id'] for d in video_files if d['sex'] == 'male']

    random.shuffle(female_video_ids)
    random.shuffle(male_video_ids)

    n = min(len(female_video_ids), len(male_video_ids))

    print(n)

    balanced_video_ids = female_video_ids[:n] + male_video_ids[:n]
    random.shuffle(balanced_video_ids)

    return balanced_video_ids


def get_emotion_ids_by_valence(valence):
    ret = []
    for key, val in emotion_id_to_valence.items():
        if val == valence or val == "neu":
            ret.append(key)
    return ret


def main():

    subset_handler = EmotionSubsetHandler()

    subset_handler.get_sample()

    subset_handler.get_sample()

    subset_handler.get_sample()

    subset_handler.get_sample()

    # pos_ids = get_emotion_ids_by_valence("pos")
    # print(pos_ids)
    # print(len(pos_ids))
    # subset = get_random_subset_emotion(pos_ids, 11)
    # print(subset)
    # print(len(subset))
    #
    # neg_ids = get_emotion_ids_by_valence("neg")
    # print(neg_ids)
    # print(len(neg_ids))
    # subset = get_random_subset_emotion(neg_ids, 11)
    # print(subset)
    # print(len(subset))



if __name__ == "__main__":
    main()
