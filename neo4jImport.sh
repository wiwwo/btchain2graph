#!/bin/bash
set 6x


shopt -s expand_aliases
alias echoi='echo `date +%Y-%m-%d\ %H:%M.%S` -INFO-'
alias echoe='echo `date +%Y-%m-%d\ %H:%M.%S` -ERROR-'

echoi STARTing `basename $0`

export DB_SOURCE_DIR=/media/sf_E_DRIVE/btchain2graph/output
export DB_DEST_DIR=/var/lib/neo4j/data/databases/blckchain.db
export IMP_LOG_FILE=/var/lib/neo4j/data/databases/blckchain.db.log
export NEO4J_LOG_FILE=/var/log/neo4j/debug.log


#############################################################################################################
### Import
IMPORT_PARAMS=" --id-type string --skip-bad-relationships=false --skip-duplicate-nodes=true "
executeMe="sudo neo4j-import --into $DB_DEST_DIR $IMPORT_PARAMS "


cd $DB_SOURCE_DIR
for type in 'nodes' 'relationships'; do
  for thisHeaderfile in `ls *$type*.header`;do
    thisDataFileTemplate=`echo ${thisHeaderfile/.header/}`
    executeMe="$executeMe --$type $DB_SOURCE_DIR/$thisHeaderfile"
    for thisDataFile in `ls *$thisDataFileTemplate`; do
      executeMe="$executeMe,$DB_SOURCE_DIR/$thisDataFile"
    done
  done
done

#for myFile in $DB_SOURCE_DIR/*.nodes.csv.gz
#do
#  myHeaderfile=`echo ${myFile/.gz/.header}`
#  myHeaderfile=`dirname $myHeaderfile`/`basename $myHeaderfile  | cut -d. -f2,3,4,5`
#  executeMe="$executeMe --nodes $myHeaderfile,$myFile"
#done
#
#for myFile in $DB_SOURCE_DIR/*.rels.csv.gz
#do
#  myHeaderfile=`echo "${myFile/.gz/.header}"`
#  myHeaderfile=`dirname $myHeaderfile`/`basename $myHeaderfile  | cut -d. -f2,3,4,5`
#  executeMe="$executeMe --relationships $myHeaderfile,$myFile"
#done

nodeFilesCnt=`ls $DB_SOURCE_DIR/*.nodes.csv.gz | wc -l`
relFilesCnt=`ls $DB_SOURCE_DIR/*.relationships.csv.gz | wc -l`

echoi Executing import
echoi " "Source CSV files in $DB_SOURCE_DIR
echoi " "Datafiles in $DB_DEST_DIR
echoi " "Log file in $IMP_LOG_FILE
echoi " "Node files count: $nodeFilesCnt, Relationship files count: $relFilesCnt
sudo rm -rf $DB_DEST_DIR
eval $executeMe > $IMP_LOG_FILE

if [ $? -ne 0 ]; then
   echoe "Error in importing, please check debug.log file and/or bad.log"
   exit 20
fi
if [ -s $DB_DIR/$TEMP_DB_NAME/bad.log ]; then
   echoe "Error in importing, bad.log file exists; exiting"
   exit 20
fi

export timeTaken=`tail -7 $IMP_LOG_FILE | grep "IMPORT DONE" | cut -d "." -f 1 | cut -d " " -f 4,5,6,7,8,9,10`
export nodesLoaded=`tail -5 $IMP_LOG_FILE | grep "nodes" | cut -d " " -f 3`
export relsLoaded=`tail -5 $IMP_LOG_FILE | grep "relationships" |  cut -d " " -f 3`
export propsLoaded=`tail -5 $IMP_LOG_FILE | grep "properties" |  cut -d " " -f 3`
echoi "Import done - loaded $nodesLoaded nodes, $relsLoaded relationships, $propsLoaded properties"

chown -R neo4j:neo4j $DB_DEST_DIR/


#############################################################################################################
### Restarting server
echoi Restarting neo4j server...
(/etc/init.d/neo4j restart || /etc/init.d/neo4j-server restart || service neo4j restart) > /dev/null 2>&1
if [ $? -ne 0 ]; then
   echoe "Error in starting neo4j instance; exiting"
   exit 30
fi

#echoi Waiting for neo4j to be available...
echoi ...
sleep 5

isStarted=0

while [[ isStarted -lt 1 ]]
do
  echoi ...
  sleep 5
  #isStarted=`tail -4 $NEO4J_LOG_FILE | grep "SERVER STARTED ENDED" | wc -l`
  isStarted=`service neo4j status | tail | grep "Remote interface available at" | wc -l`
  let timer=timer+1
  if [[ timer -gt 20 ]]; then
    echoe "Neo4j seems not starting, please check $NEO4J_LOG_FILE; exiting"
    exit 30
  fi
done

echoi Neo4j seems to be started

export myDate=`date`
sudo neo4j-shell -c "create (x:_importInfo   { dbCreateDate: '$myDate', dbCreateDateEpoch: timestamp(), timeTaken: '$timeTaken', nodesLoaded: $nodesLoaded, relationshipsLoaded: $relsLoaded, propertiesLoaded: $propsLoaded, nodesFilesCount: $nodeFilesCnt, relationshipsFileCount: $relFilesCnt, commandExecuter: '$executeMe' }  );" >/dev/null 2>&1

echoi ENDing

