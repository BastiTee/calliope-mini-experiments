#!/bin/bash

cd "$( dirname "$( readlink -f "$0" )" )"
echo "-- working dir: $( pwd )"
if [ -d "$1" ]
then
	srcdir=$( sed -r -e "s/[\/]+$//" <<< $1 )
	echo "-- copying from $srcdir"
	cp -uv $srcdir/*.hex .
else
	echo "-- no source copy set"
fi
cnt=$( ls *.hex | wc -l )
echo "-- input files: $cnt"
[ $cnt -le 0 ] && exit 0
minidir=
if [ -d /media/$( whoami )/MINI ]
then
	minidir="/media/$( whoami )/MINI"
elif [ -d /media/MINI ]
then
	minidir="/media/MINI"
fi
minidir=$( sed -r -e "s/[\/]+$//" <<< $minidir )
echo "-- mini-dir: $minidir"
echo "-- install bbc-cmd-hub"
if [ ! -f "bbc-cmd-hub" ]
then
	curl -H 'Cache-Control: no-cache' -o bbc-cmd-hub \
"https://raw.githubusercontent.com/\
BastiTee/bastis-bash-commons/master/bbc-cmd-hub"
	chmod a+x bbc-cmd-hub
fi
rm -v ${minidir}/*.hex 2> /dev/null
function handle_selection () {
	cp -v $1 $minidir
}
export -f handle_selection
export minidir
./bbc-cmd-hub -c "ls *.hex" -s -p "handle_selection"
