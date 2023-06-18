#!/bin/bash
set -x
if [ $# -eq 0 ]
  then
    echo "./TestBot.sh <playername> <numberOfMatches>"
    exit 1
fi
gamesToPlay=$2
myArray=("RandomPlayer" "OneTurnLookahead" "Minimax" "PrunedBFS" "WBukowski" "JMikolajczyk" "DBaziuk")
echo $(date -u) >> TestOutput/output.txt
for str in ${myArray[@]}; do
  if [ "$str" != "$1" ]; then
    echo "    $str Bot vs $1 Bot" >> TestOutput/output.txt
    echo "    $str Bot vs $1 Bot"
    python3 example/Example_Match_All_bots.py $str $1 $2 > temp.txt
    cat temp.txt | grep "MATCH RESULTS"
    cat temp.txt | grep "MATCH RESULTS" | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$//g' | awk '{if ($1 < $2) SUM += 1; else SUM2 += 1} END { print "      MATCH RESULTS[" SUM2 ", " SUM "]"}' >> TestOutput/output.txt
  fi
done
