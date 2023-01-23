from config import emotion_abr_to_emotion_id, emotion_id_to_valence
from helpers import get_digits_only, name2list, get_filename
from metadata.error_file_exception import ErrorFileException


class Metadata(object):

    DEFAULT_INTENSITY_LEVEL = 1
    DEFAULT_VERSION = 1
    DEFAULT_SITUATION = 1

    # can be vocalization (v) or prosody (p)
    DEFAULT_MODE = "v"

    DEFAULT_PROPORTIONS = 0
    DEFAULT_EMOTION = None
    DEFAULT_MIX = 0
    # set it to some number not in the list
    DEFAULT_EMOTION_ID = 100
    DEFAULT_VALENCE = None

    def __init__(self,
                 filename):

        self.filename = filename
        self.name_list = name2list(filename)

        # e.g. A220
        self.video_id = self.name_list[0]

        self.mix = self.DEFAULT_MIX
        self.emotion_1 = self.DEFAULT_EMOTION
        self.emotion_1_id = self.DEFAULT_EMOTION_ID

        self.emotion_2 = self.DEFAULT_EMOTION
        self.emotion_2_id = self.DEFAULT_EMOTION_ID

        self.proportions = self.DEFAULT_PROPORTIONS
        self.mode = self.DEFAULT_MODE
        self.intensity_level = self.DEFAULT_INTENSITY_LEVEL
        self.version = self.DEFAULT_VERSION
        self.situation = self.DEFAULT_SITUATION
        self.emotion_1_valence = self.DEFAULT_VALENCE
        self.emotion_2_valence = self.DEFAULT_VALENCE

        self.set_all_metadata(self.name_list)

    def set_mixed_emotions(self, name_list):
        """
        e.g. A220_mix_ang_disg_5050.csv
        """
        self.mix = 1
        self.emotion_1 = name_list[2]
        self.emotion_2 = name_list[3]
        self.proportions = name_list[4]

    def set_neutral_emotion(self, name_list):
        """
        e.g. A220_neu_sit1_v.csv
        """
        self.emotion_1 = name_list[1]
        # remove all non-numeric characters from situation string, keep only the digit
        self.situation = get_digits_only(name_list[2])
        self.mode = name_list[3]

    def set_long_name(self, name_list):
        """
        e.g. A220_neg_sur_p_1.csv
        """
        # concat the long name of the emotion
        self.emotion_1 = "_".join((name_list[1], name_list[2]))
        self.mode = name_list[3]
        self.intensity_level = name_list[4]

    def set_default_emotion(self, name_list):
        """
        e.g. A220_adm_p_1.csv
        """
        self.emotion_1 = name_list[1]
        self.mode = name_list[2]
        self.intensity_level = name_list[3]

    def set_versioned_emotion(self, name_list):
        """
        e.g. A327_ang_v_1_ver1.csv
        """
        self.emotion_1 = name_list[1]
        self.mode = name_list[2]
        self.intensity_level = name_list[3]
        self.version = get_digits_only(name_list[4])

    def set_emotion_ids(self):
        self.emotion_1_id = emotion_abr_to_emotion_id[self.emotion_1]

        if self.mix == 1:
            self.emotion_2_id = emotion_abr_to_emotion_id[self.emotion_2]

    def set_valence(self):
        self.emotion_1_valence = emotion_id_to_valence[self.emotion_1_id]
        if self.mix == 1:
            self.emotion_2_valence = emotion_id_to_valence[self.emotion_2_id]

    def set_all_metadata(self, name_list):
        if name_list[1] == special_cases["mixed_emotions"]:
            self.set_mixed_emotions(name_list)
        elif name_list[1] == special_cases["neutral_emotion"]:
            self.set_neutral_emotion(name_list)
        elif len(name_list) > 4:
            if name_list[4] == special_cases["error"]:
                raise ErrorFileException
            elif name_list[4].startswith("ver"):
                self.set_versioned_emotion(name_list)
            else:
                self.set_long_name(name_list)
        else:
            self.set_default_emotion(name_list)

        self.set_emotion_ids()
        self.set_valence()


special_cases = {
    "mixed_emotions": "mix",
    "neutral_emotion": "neu",
    "error": "e"
}