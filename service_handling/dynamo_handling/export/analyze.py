import os
import pandas as pd

from config import ROOT_DIR, emotion_id_to_emotion
from metadata.file_metadata import Metadata

path = os.path.join(ROOT_DIR, "files/database_files/data_user.csv")


df = pd.read_csv(path)

filenames = list(df["filename"])
replies = list(df["emotion_id_reply"])

out = []
metas = []
for idx, filename in enumerate(filenames):
    meta = Metadata(filename)

    rep = {"korrekt känsla": emotion_id_to_emotion[str(meta.emotion_1_id)],
           "svar": emotion_id_to_emotion[str(replies[idx])]}
    out.append(rep)
    metas.append(meta)

df2 = pd.DataFrame.from_dict(out)

out_path = os.path.join(ROOT_DIR, "files/database_files/data_user_overview.csv")

df2.to_csv(out_path)