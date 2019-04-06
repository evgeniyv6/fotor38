#!/bin/bash

#v0.2

# crypt files and folders

d=`date '+%d%m%Y_%H%M%S'`
scr_dir=$(cd `dirname $0` && pwd)

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

#set -x # for debug mode

arch () {
  if ! [ -d ${scr_dir}/archive/ ];then
     echo "archive directory is absent and will be created..."
     mkdir ${scr_dir}/archive
     echo "archive dir is created"
     if [ "$1" = "pwdarch" ]; then
       mv ${scr_dir}/insideall* ${scr_dir}/archive/
     fi
     if [ "$1" = "folderarch" ]; then
       mv ${scr_dir}/pdfarch* ${scr_dir}/archive/
     fi
     echo -e "${GREEN}\n\tarchive done\n"
  else
     if [ "$1" = "pwdarch" ]; then
       mv ${scr_dir}/insideall* ${scr_dir}/archive/
     fi
     if [ "$1" = "folderarch" ]; then
       mv ${scr_dir}/pdfarch* ${scr_dir}/archive/
     fi
     echo -e "${GREEN}\n\tarchive done\n"
  fi
}



funcUsage () {
cat << EOF
#########################################
Note
#########################################
1 arg:	vw - to view file
	cz - to create file
	xz - to extract file
2 arg:  file to view, archive or *.tar.gz to extract
3 arg:  *.tar.gz to archive (write only name without ./ path way)
EOF
}

checkExist () {
case "$1" in
	exist)
	declare -a argAll=("${@}")
	argCut=("${argAll[@]::${#argAll[@]}-1}")
	unset "argCut[0]"
	unset "argCut[1]"
	for item in "${argCut[@]}";do
		if [ -e $(cd `dirname "${item}"` && pwd)/$(basename "${item}") ] || [ -d $(cd `dirname "${item}"` && pwd)/$(basename "${item}") ];then
			echo -e "${GREEN}${item}${NC}"
			echo -e "${GREEN}\n\tfile exists\n${NC}"
		else
			echo -e "${RED}------->\t${item}${NC}"
			echo -e "${RED}------->\tfile or folder not found\n${NC}"
			break
		fi
	done
	;;
	rmrf)
	for item in "${argCut[@]}";do
		rm -rf "${item}"
		echo -e "${RED}\n\tfile(s) was(were) removed\n${NC}"
	done
	;;
	cgz)
	tar cz "${argCut[@]}" | openssl enc -aes-256-cbc -md md5 -e > $scr_dir/"${!#}_$d.tar.gz"
	;;
	*) echo -e "${RED}\n\tnothing to do\n${NC}";exit 1;
esac
}


main_func () {
declare -a argAll=("${@}")
argCut=("${argAll[@]::${#argAll[@]}-1}")
unset "argCut[0]"
if [ "$#" -gt 1109 ];then
	echo -e "${RED} \n\tNot more then 1109 parameters!\n${NC}"
	exit 1 #General errors, miscellaneous errors, such as "divide by zero" and other impermissible operations
else
	case "$1" in
		help) funcUsage; exit 1
		;;
		vw)
		openssl aes-256-cbc -d -md md5 -in "$2" | gzcat | less
		exit 1
		;;
		xz)
		openssl aes-256-cbc -d -md md5 -in "$2" | tar -xz
                echo -e "${GREEN}\n\tDone\n${NC}"
		exit 1
		;;
		cz)
                arch "$3"
		checkExist exist $@
		checkExist cgz $@
		read -p "Remove original file(s) - " ynof
		if [[ $ynof =~ ^[yY]$  ]];then
			checkExist rmrf
		elif [[ $ynof =~ ^[nN]$  ]];then
			echo -e "${RED}\n\t WARNING!! file(s) was(were) not removed\n${NC}"
		else
			echo -e "${RED}\n\tWrong answer. y|Y or n|N required\n${NC}"
		fi
                if [ "$3" = "pwdarch" ];then
                       read -p "Clear draft file? - " ynd
                       if [[ $ynd =~ ^[yY]$  ]];then
                            : > ${scr_dir}/draft.txt 
                            echo -e "${RED}\n\tDraft file was cleared\n${NC}"
                       elif [[ $ynd =~ ^[nN]$  ]];then
                            echo -e "${RED}\n\t WARNING!! U left credentials in draft file\n${NC}"
                       else
                            echo -e "${RED}\n\tWrong answer. y|Y or n|N required\n${NC}"
                       fi
                fi
		exit 1
		;;
		*) echo ""; funcUsage; exit 1;
	esac
fi
}

main_func $@
exit 2
exit 0
