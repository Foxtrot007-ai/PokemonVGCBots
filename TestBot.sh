#!/bin/bash
set -x
if [ $# -eq 0 ]
  then
    echo "./TestBot.sh <playername>"
    exit 1
fi
myArray=("RandomPlayer" "OneTurnLookahead" "Minimax" "PrunedBFS" "WBukowski" "JMikolajczyk" "DBaziuk")
echo $(date -u) >> TestOutput/output.txt
for str in ${myArray[@]}; do
    echo "    $str Bot vs $1 Bot" >> TestOutput/output.txt
    python3 example/Example_Match_All_bots.py $str $1 | grep "MATCH RESULTS" | awk '{print "       " $0}' >> TestOutput/output.txt
done
