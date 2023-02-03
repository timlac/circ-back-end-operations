#!/bin/bash

mkdir -p converted
for f in *.mp4; do ffmpeg -i $f -c:v copy -c:a aac -b:a 192k "converted/${f%.mp4}.mp4"; done