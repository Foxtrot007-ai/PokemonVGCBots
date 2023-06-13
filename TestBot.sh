#!/bin/bash
set -x
myArray=("RandomPlayer" "OneTurnLookahead" "Minimax" "PrunedBFS")
echo $(date -u) >> TestOutput/output.txt
for str in ${myArray[@]}; do
    echo "    $str Bot vs MyPolicy Bot" >> TestOutput/output.txt
    python3 example/Example_Match_All_bots.py $str | grep "MATCH RESULTS" | awk '{print "       " $0}' >> TestOutput/output.txt
done
