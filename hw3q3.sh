#!/bin/bash
#Ling572 HW3Q3
#Nat Byington
#Mami Sasaki
commandNB='./build_NB1.sh'
trainf='../../dropbox/09-10/572/hw3/examples/train.vectors.txt'
testf='../../dropbox/09-10/572/hw3/examples/test.vectors.txt'
modelf='model.'
sysf='sys.'
accf='acc_file.'
delta=0
cond_prob="0.1 0.5 1.0 2.0"
outdir='q3/'

#create directlry if it doesn't exist already
if [ ! -d "$outdir" ];then
 mkdir -p $outdir 
fi

#q3
for cp in $cond_prob 
do
$commandNB $trainf $testf $delta $cp $outdir$modelf$cp $outdir$sysf$cp >$outdir$accf$cp
done

