#!/bin/bash
#Ling572 HW3Q5
#Nat Byington
#Mami Sasaki
commandNB='./build_NB2.sh'
path='../../dropbox/09-10/572/hw3/examples/'
trainf='train.vectors.txt'
testf='test.vectors.txt'
modelf='model.'
sysf='sys.'
accf='acc_file.'
delta=0
cond_prob="0.1 0.5 1.0 2.0"
outdir='q5/'

#create directlry if it doesn't exist already
if [ ! -d "$outdir" ];then
 mkdir -p $outdir 
fi

#binarize input file
./binarize.py $path$trainf $outdir$trainf 
./binarize.py $path$testf $outdir$testf 

#run tests
for cp in $cond_prob 
do
$commandNB $outdir$trainf $outdir$testf $delta $cp $outdir$modelf$cp $outdir$sysf$cp >$outdir$accf$cp
done
