#!/bin/bash

mydir=$PWD
err_log=$mydir/error_log.log
exec 2>$err_log
echo "BACKUP..."
for i in $(dspmq|grep -v -e RKM -e MAINENV|sed -e 's/QMNAME(//g' -e 's/).*//g');do
cat << EOF | runmqsc ${i}
dis listener(${i}.LISTENER)
EOF
done > $mydir/backup_without_MAINENV_suffix.txt
for x in $(dspmq|grep MAINENV|grep -v -e RKM -e LOG|sed -e 's/QMNAME(//g' -e 's/).*//g');do for y in $(dspmq|grep MAINENV|grep -v RKM|sed -e 's/QMNAME(//g' -e 's/.MAINENV.*//g');
do
cat << EOF | runmqsc ${x}
dis listener(${y}.LISTENER)
EOF
done; done > $mydir/backup_with_MAINENV_suffix.txt
echo "START DELETE ALL LISTENERS..."
echo "1. START KILL MQ PROCESSES..."
for x in $(ps -ef|grep lsr|grep QM|grep -v -e RKM -e LOG|awk '{print $2}');do kill -9 ${x};done
sleep 15
echo "2. DONE."
echo "3. START DELETE LISTENERS..."
for i in $(dspmq|grep -v -e RCMSK -e PROD|sed -e 's/QMNAME(//g' -e 's/).*//g');do
cat << EOF | runmqsc ${i}
delete listener(${i}.LISTENER)
EOF
done > $mydir/delLog_without_MAINENV_suffix.txt
sleep 10
for x in $(dspmq|grep MAINENV|grep -v -e RKM -e LOG|sed -e 's/QMNAME(//g' -e 's/).*//g');do 
for y in $(dspmq|grep MAINENV|grep -v -e RKM -e LOG|sed -e 's/QMNAME(//g' -e 's/.MAINENV.*//g');do
cat << EOF | runmqsc ${x}
delete listener(${y}.LISTENER)
EOF
done; done > $mydir/delLog_with_MAINENV_suffix.txt
echo "4. DONE."
echo "5. CHECK LOG FILE $mydir/delLog_with_MAINENV_suffix.txt AND $mydir/delLog_without_MAINENV_suffix.txt"
echo "DELETED LISTENERS OF MANAGERS WITHOUT MAINENV SUFFIX"
delVar1=`grep -irc "WebSphere MQ listener object deleted" $mydir/delLog_without_MAINENV_suffix.txt`
echo $delVar1
echo "DELETED LISTENERS OF MANAGERS WITH MAINENV SUFFIX"
delVar2=`grep -irc "WebSphere MQ listener object deleted" $mydir/delLog_with_MAINENV_suffix.txt`
echo $delVar2
exit 1