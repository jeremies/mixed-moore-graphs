#! /bin/bash

rm predetermined-entries/free/*
for n in {6,12,18,20,30,40,42,54,56,72,84,88}; do
    echo $n
    #       "n    almost   closed    repeat" 
    echo -e "$n \n   0  \n   0    \n  0" | python predetermined.py | tail -n +2 > predetermined-entries/free/$n
done
	 
rm predetermined-entries/closed/*
for n in {6,12,18,20,30,40,42,54,56,72,84,88}; do
    echo $n
    #       "n    almost   closed    repeat" 
    echo -e "$n \n   0  \n   1    \n  0" | python predetermined.py | tail -n +2 > predetermined-entries/closed/$n
done

rm predetermined-entries/almost/*
for n in {26,50,68,84,10,18,28,40,54}; do
    for r in {0,1,2,3}; do
	echo $n
	file=$(printf "%s-%s" "$n" "$r")
	#       "n    almost   closed    repeat" 
	echo -e "$n \n   1  \n   0    \n  $r" | python predetermined.py | tail -n +2 > predetermined-entries/almost/$file
    done
done
