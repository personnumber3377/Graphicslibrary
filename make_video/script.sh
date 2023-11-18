#!/bin/sh
ffmpeg -framerate 3 -pattern_type glob -i '/home/cyberhacker/Asioita/Ohjelmointi/Python/Graphics/frames/*.png' -c:v libx264 out.mp4
