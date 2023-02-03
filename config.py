import json
import os

experiment_table_name = "video_validation_experiment"
example_table_name = "example_videos"

ROOT_DIR = "/home/tim/work/su-thesis-project/video-validation-back-end"

s3_bucket_name = "validation-experiment-video-files-01"

emotion_abr_to_emotion_id = {
  "reg": 0,
  "conf": 1,
  "det": 2,
  "dou": 3,
  "env": 4,
  "adm": 5,
  "sad": 6,
  "gra": 7,
  "ele": 8,
  "pos_sur": 9,
  "fea": 10,
  "neg_sur": 11,
  "ang": 12,
  "amu": 13,
  "rej": 14,
  "scha": 15,
  "sat": 16,
  "dist": 17,
  "awe": 18,
  "ins": 19,
  "tri": 20,
  "hop": 21,
  "neu": 22,
  "ple": 23,
  "sex": 24,
  "pea": 25,
  "bor": 26,
  "conc": 27,
  "ten": 28,
  "int": 29,
  "nos": 30,
  "sar": 31,
  "cont": 32,
  "hap": 33,
  "anx": 34,
  "disg": 35,
  "exc": 36,
  "disa": 37,
  "rel": 38,
  "emb": 39,
  "gui": 40,
  "pri": 41,
  "mov": 42,
  "sha": 43
}

emotion_id_to_emotion_abr = dict(zip(emotion_abr_to_emotion_id.values(), emotion_abr_to_emotion_id.keys()))

emotion_id_to_valence = {
    0: "neg",
    1: "neg",
    2: "pos",
    3: "neg",
    4: "neg",
    5: "pos",
    6: "neg",
    7: "pos",
    8: "pos",
    9: "pos",
    10: "neg",
    11: "neg",
    12: "neg",
    13: "pos",
    14: "neg",
    15: "neg",
    16: "pos",
    17: "neg",
    18: "pos",
    19: "pos",
    20: "pos",
    21: "pos",
    22: "neu",
    23: "pos",
    24: "pos",
    25: "pos",
    26: "neg",
    27: "pos",
    28: "pos",
    29: "pos",
    30: "neg",
    31: "neg",
    32: "neg",
    33: "pos",
    34: "neg",
    35: "neg",
    36: "pos",
    37: "neg",
    38: "pos",
    39: "neg",
    40: "neg",
    41: "pos",
    42: "pos",
    43: "neg"
}


