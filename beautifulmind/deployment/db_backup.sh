#!/bin/bash
DIR=/opt/beautifulmind/backup/
[ ! $DIR ] && mkdir -p $DIR || :
pg_dump -U postgres beautifulmind | gzip -c > $DIR/db_$(date +"%Y%m%d%H%M%S").gz