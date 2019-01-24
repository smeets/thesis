#!/bin/bash
echo "replotting..."
win=$(xdotool getactivewindow)
node scripts/fe.js > fe.csv
python3 scripts/model-plot.py fe.csv graph.png
xdotool search "Mozilla Firefox" windowactivate --sync key --clearmodifiers F5
xdotool windowactivate "$win"
