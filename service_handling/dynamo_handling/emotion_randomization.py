import random

from config import emotion_id_to_valence


def get_random_subset(my_list, subset_length):
    return random.sample(my_list, subset_length)


def get_emotion_ids_by_valence(valence):
    ret = []
    for key, val in emotion_id_to_valence.items():
        if val == valence or val == "neu":
            ret.append(key)
    return ret


def main():
    pos_ids = get_emotion_ids_by_valence("pos")
    print(pos_ids)
    print(len(pos_ids))
    subset = get_random_subset(pos_ids, 11)
    print(subset)
    print(len(subset))

    neg_ids = get_emotion_ids_by_valence("neg")
    print(neg_ids)
    print(len(neg_ids))
    subset = get_random_subset(neg_ids, 11)
    print(subset)
    print(len(subset))



if __name__ == "__main__":
    main()
