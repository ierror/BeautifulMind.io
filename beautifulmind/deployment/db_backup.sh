#!/bin/bash
DIR=/opt/beautifulmind/backup/
FILENAME=db_$(date +"%Y%m%d%H%M%S").gz
FILENAMETMP=$FILENAME-tmp;
mkdir -p $DIR && cd $DIR && pg_dump -U postgres beautifulmind | gzip -c > $FILENAMETMP 
mv $FILENAMETMP $FILENAME