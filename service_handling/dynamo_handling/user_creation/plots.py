from config import emotion_id_to_emotion_abr


from collections import defaultdict

from matplotlib import pyplot as plt


def plot_distribution(my_list):
    samples = defaultdict(int)

    for i in my_list:
        samples[i] += 1

    print(len(samples))

    plt.bar(samples.keys(), samples.values(), color='g')
    plt.xticks(rotation=90)

    plt.show()


def plot_emotion_distribution(user_type):
    samples = defaultdict(int)

    for user in user_type:
        for obj in user:
            emotion_id = obj["item"]["emotion_1_id"]
            emotion_abr = emotion_id_to_emotion_abr[emotion_id]
            samples[emotion_abr] += 1

    plt.bar(samples.keys(), samples.values(), color='g')
    plt.title("Samples for each emotion")
    plt.xticks(rotation=90)

    plt.show()


def plot_video_id_distribution(user_type):
    samples = defaultdict(int)

    for user in user_type:
        for obj in user:
            video_id = obj["item"]["video_id"]

            samples[video_id] += 1

    print("total number of samples in video is distribution: ", end="")
    print(sum(samples.values()))

    plt.bar(samples.keys(), samples.values(), color='g')
    plt.xticks(rotation=90)
    plt.title("Samples for each video id")
    plt.show()


def plot_file_distribution(user_type):

    samples = defaultdict(int)
    for user in user_type:
        for obj in user:
            filename = obj["item"]["filename"]
            samples[filename] += 1

    print("total number of samples in analyze users: ", end="")
    print(sum(samples.values()))

    plt.bar(range(len(samples)), samples.values(), color='g')
    plt.title("Samples of each video")
    plt.show()

