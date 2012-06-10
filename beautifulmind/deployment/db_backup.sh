#!/bin/bash
DIR=/opt/beautifulmind/backup/
FILENAME=db_$(date +"%Y%m%d%H%M%S").gz
mkdir -p $DIR && pg_dump -U postgres beautifulmind | gzip -c > $DIR$FILENAME