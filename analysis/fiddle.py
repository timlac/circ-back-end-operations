from config import video_files

print("female naro")
for i in video_files:
    if i["sex"] == "female" and i["prosody"] == "naro":
        print(i["video_id"])

print()
print("female meli")
for i in video_files:
    if i["sex"] == "female" and i["prosody"] == "meli":
        print(i["video_id"])


print()
print("male naro")
for i in video_files:
    if i["sex"] == "male" and i["prosody"] == "naro":
        print(i["video_id"])


print()
print("male meli")
for i in video_files:
    if i["sex"] == "male" and i["prosody"] == "meli":
        print(i["video_id"])


# for i in video_files:
#     print("'" + i["video_id"] + "',")