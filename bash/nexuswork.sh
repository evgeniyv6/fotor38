#!/bin/bash
 
# vars section
SCRIPTDIR="$(cd "$(dirname ${0})" && pwd)"
LOGFILE=${SCRIPTDIR}/nexusuploadlog.txt
CONNTIMEOUT=10
CURL=`which curl`
if [[ ! -z "${3}" ]]; then FILENAME="$(basename $3)";FILEEXTENSION="${FILENAME##*.}";fi
 
# NEXUS PARAMS
FIRSTNEXUSURL='https://<1_nexus_address>'
SECONDNEXUSURL='https://<2_nexus_address>'
REPOSITORY="Nexus"
CLASSIFIER="myclassifier"
GROUPID="mygroupid"
ARTIFACTID="myartifactid"
PACKAGING=${FILEEXTENSION}
EXTENSION=${FILEEXTENSION}
 
# colors vars
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
 
funcUsage() {
        cat << EOF >&2
**********************************************************************
Needed parameter is absent.
You should specify three parameters:
{mode}, {version}, {archive}
{mode} format:
   --help - to get information
   --upload - to upload archive
   --download - to download archive
EXIT...
EOF
}
 
getDate() {
        echo -n $(date +'[%d/%m/%y %H:%M:%S]')
}
 
logFunction() {
        LOGMSG=${@}
        echo "$(getDate): ${LOGMSG}" >> ${LOGFILE}
}
 
availableCheck() {
        CALLNEXUS=$(${CURL} -k -S -I --connect-timeout ${CONNTIMEOUT} ${FIRSTNEXUSURL} 2>&1)
        if [[ ${?} != 0 && ${?} = 60 ]]; then
                logFunction ${CALLNEXUS}
                exit 1
        fi
}
 
if [[ $# < 1 ]]; then echo "";funcUsage;exit 1; fi
 
checkArtifactId() {
${CURL} -k -s "${FIRSTNEXUSURL}/repositories/${REPOSITORY}/content/${GROUPID}/${ARTIFACTID}/maven-metadata.xml"|grep "<version>.*</version>"| sort| uniq | grep -v initial_version |sed -e "s#\(.*\)\(<version>\)\(.*\)\(</version>\)\(.*\)#\3#g" | grep -i "${1}"
if [[ ${?} == 0 ]]; then
echo -e "${RED}Such an artifact already exists${NC}"
exit 1
fi
}
 
nexusUpload() {
checkArtifactId $1
        tryUpload=$(${CURL} -v -k -F r=${REPOSITORY} -F hasPom=false -F c=${CLASSIFIER} -F g=${GROUPID} -F a=${ARTIFACTID} -F v=${1} -F p=${FILEEXTENSION} -F e=${FILEEXTENSION} -F file=@${FILENAME} -u ${NEXUSUSER}:${NEXUSPASSWORD} ${FIRSTNEXUSURL}/artifact/maven/content)
if [[ ${?} != 0 ]]; then
                echo -e "${RED}Upload failed${NC}"
logFunction ${tryUpload}
                exit 1
else
echo -e "${GREEN}Upload DONE.${NC}"
        fi
}
 
nexusDownload() {
[[ $(${CURL} -k -s -o /dev/null -w "%{http_code}" "${FIRSTNEXUSURL}/") == "200" ]] && NEXUSADDRESS=${FIRSTNEXUSURL} || NEXUSADDRESS=${SECONDNEXUSURL}
reverseslash=$(echo ${2} | sed 's/\\/\//g')
echo "${reverseslash}"
tryDownload=$(${CURL} -v -o ${reverseslash} -u ${NEXUSUSER}:${NEXUSPASSWORD} -k -L "${NEXUSADDRESS}/artifact/maven/redirect?r=${REPOSITORY}&g=${GROUPID}&a=${ARTIFACTID}&v=${1}&p=${FILEEXTENSION}&c=${CLASSIFIER}")
if [[ ${?} != 0 ]]; then
                echo -e "${RED}Download failed${NC}"
                logFunction ${tryDownload}
                exit 1
else
echo -e "${GREEN}Download COMPLETED.${NC}"
        fi
 
}
 
main() {
case "$1" in
--help) funcUsage; exit 0
;;
--upload)
read -p "NEXUS USER: " NEXUSUSER
read -s -p "NEXUS PASSWORD: " NEXUSPASSWORD
echo ""
nexusUpload $2 $3; exit 0
;;
--download)
read -p "NEXUS USER: " NEXUSUSER
read -s -p "NEXUS PASSWORD: " NEXUSPASSWORD
echo ""
nexusDownload $2 "$3"; exit 0
;;
*) echo ""; funcUsage; exit 0;
esac
}
 
 
main $@
exit 2
exit 0