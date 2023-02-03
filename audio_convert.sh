#!/bin/bash

mkdir -p converted
for f in *.mov; do ffmpeg -i $f -s 1280x720 -c:v h264 -c:a aac -b:a 192k "converted/${f%.mov}.mp4"; done
