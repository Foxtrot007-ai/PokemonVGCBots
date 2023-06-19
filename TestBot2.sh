#!/bin/bash
#set -x
if [ $# -ne 3 ]
  then
    echo "./TestBot.sh <playername> <numberOfMatches> <testingPack>"
    exit 1
fi

gamesToPlay=$2
all=("RandomPlayer" "OneTurnLookahead" "TypeSelector" "Minimax" "PrunedBFS" "WBukowski" "JMikolajczyk" "DBaziuk")
bots=("RandomPlayer" "OneTurnLookahead" "TypeSelector" "Minimax" "PrunedBFS")
players=("WBukowski" "JMikolajczyk" "DBaziuk")
sims=("Minimax" "PrunedBFS")

declare -n selected=$3
for str in ${selected[@]}; do
  if [ "$str" != "$1" ]; then
    echo -n "$str Bot vs $1 Bot - "
    python3 Match_All_bots.py $str $1 $2 | grep "MATCH RESULTS" | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$//g' | awk '{if ($1 < $2) SUM += 1; else SUM2 += 1} END { print "[" SUM2 ", " SUM "]"}'
  fi
done
