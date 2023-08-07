import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import confusion_matrix, classification_report
import json

from config import ROOT_DIR, emotion_id_to_emotion
from helpers import slice_by, mapper

path = os.path.join(ROOT_DIR, "files/database_files/full_export.csv")


df = pd.read_csv(path)

count_of_rows = len(df[df['emotion_id_reply'] == 1000])
print("Number of rows where emotion_id_reply is equal to 1000:", count_of_rows)

count_of_rows = len(df[df['emotion_id_reply'] != 1000])
print("Number of rows where emotion_id_reply is NOT equal to 1000:", count_of_rows)

slices = slice_by(df, "alias")

complete_subjects = []
incomplete_subjects = []

for s in slices:
    all_rows_equal_1000 = (s['emotion_id_reply'] == 1000).all()
    if not all_rows_equal_1000:
        has_emotion_id_1000 = (s['emotion_id_reply'] == 1000).any()
        if has_emotion_id_1000:
            incomplete_subjects.append(s)
        else:
            complete_subjects.append(s)


print("length of complete subjects: " + str(len(complete_subjects)))
print("length of incomplete subjects: " + str(len(incomplete_subjects)))

complete_subjects_concat = pd.concat(complete_subjects, ignore_index=True)

count_of_matching_rows = len(complete_subjects_concat[complete_subjects_concat['emotion_id_reply']
                                                      == complete_subjects_concat['emotion_id']])
print("Number of rows where emotion_id_reply is equal to emotion_id:", count_of_matching_rows)
print("Total number of rows: ", len(complete_subjects_concat))
print("Fraction: ", count_of_matching_rows/len(complete_subjects_concat))


# Assuming you have the true labels in 'y_true' and the predicted labels in 'y_pred'
# Replace 'y_true' and 'y_pred' with the actual true and predicted labels of your classifier

y_true = complete_subjects_concat[["emotion_id"]]
y_pred = complete_subjects_concat[["emotion_id_reply"]]

# # Create the confusion matrix
# conf_matrix = confusion_matrix(y_true, y_pred, normalize="true")
#
# # get emotion_ids
# emotion_ids = np.unique(y_true)
#
# # get emotion abreviations
# emotion_abrs = mapper(emotion_ids, emotion_id_to_emotion)
#
# # create dataframe with lists of emotion ids as row and column names
# df_cm = pd.DataFrame(conf_matrix, list(emotion_abrs), list(emotion_abrs))
#
# # Convert the confusion matrix to a DataFrame for better visualization
# conf_matrix_df = pd.DataFrame(conf_matrix, index=range(44), columns=range(44))
#
# turquoise_rgb = (118 / 255, 183 / 255, 178 / 255)
# blue_rgb = (78 / 255, 121 / 255, 167 / 255)
#
# # More color definitions
# conf_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(255 / 255, 255 / 255, 215 / 255), turquoise_rgb,
#                                                                      blue_rgb])
#
# plt.figure(figsize=(20, 15))
# ax = sns.heatmap(df_cm, annot=True, fmt='.1f', vmin=0, vmax=1, cmap=conf_cmap)
# plt.yticks(va='center')
# plt.xlabel('Predicted Label')
# plt.ylabel('Actual Label')
# plt.show()


# Generate the classification report
report = classification_report(y_true, y_pred,
                               target_names=emotion_id_to_emotion.values(),
                               output_dict=True)

# save_path = os.path.join(ROOT_DIR, "files/analysis/classification_report")
#
# with open(save_path + ".json", 'w') as fp:
#     json.dump(report, fp)

# Convert the JSON data to a DataFrame
# df = pd.DataFrame.from_dict(report, orient='index')
# Display the classification report
# print(report)

# Create a list of dictionaries from the JSON data
rows = []
for class_label, metrics in report.items():
    if class_label in emotion_id_to_emotion.values():
        print(class_label)
        print(metrics)
        row = {
            'Class': class_label,
            'Precision': metrics['precision'],
            'Recall': metrics['recall'],
            'F1-score': metrics['f1-score'],
            'Support': metrics['support']
        }
        rows.append(row)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(rows)

save_path = os.path.join(ROOT_DIR, "files/analysis/classification_report")
df.to_csv(save_path)