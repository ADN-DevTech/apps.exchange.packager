#!/bin/bash

#mkdir -p "$HOME/Autodesk/ApplicationPlugins/{{AppName}}"
#cp -r ./* $HOME/Autodesk/ApplicationPlugins/{{AppName}}
#rm $HOME/Autodesk/ApplicationPlugins/{{AppName}}/install.sh

if [ "$(id -u)" != "0" ]; then
	export INSTALLDIR=$HOME/Autodesk/ApplicationPlugins
else
	export INSTALLDIR=/usr/autodesk/ApplicationPlugins
fi

function untar_payload () {
	match=$(grep --text --line-number '^PAYLOAD:$' $0 | cut -d ':' -f 1)
	payload_start=$((match + 1))
	tail -n +$payload_start $0 | (cd $INSTALLDIR; tar -xzvf -)
}

read -p "Install Files? (y/Y) " ans
if [[ $ans == 'y' || $ans == 'Y' ]]; then
	mkdir -p $INSTALLDIR
	untar_payload
fi
exit 0


