#!/bin/bash

# test

#PARAMS
PATHP="/path/to/dl-playbook"
MPATH="/path/to/mt-playbook"

##### SSH-AGENT BLOCK #####
##### NEED IF MASTER PASS IS NOT EMPTY #####
echo "exec cat" > /tmp/ap-helper.sh
chmod a+x /tmp/ap-helper.sh
PASS="<some_password>"
KEY_FILE="~/.ssh/id_rsa"
eval "$(ssh-agent)" > /dev/null
export DISPLAY=1
trap "ssh-agent -k > /dev/null" EXIT
echo "$PASS"| SSH_ASKPASS=/tmp/ap-helper.sh ssh-add ~/.ssh/id_rsa
rm -f /tmp/ap-helper.sh

##### OUTPUT SECTION  #####
#exec 2>/dev/null

ansible-playbook -i $PATHP/inventories/$1/hosts "$PATHP"/site.yml --vault-password-file "$MPATH"/masterpass.txt

exit 1

