#!/bin/bash

access_database=${1}


output_dir=${2}
mkdir -p "${output_dir}"


if [ -z ${access_database} ]; then
    exit 1
fi


echo "-- Export database: ${access_database}"

# export schema
echo "-- Export schema"
mdb-schema  ${access_database}  postgres > "${output_dir}/_schema.sql"

tables=$(mdb-tables -1 ${access_database})
for table in $tables
do
    echo "-- Export table: ${table}"
    mdb-export -d "\t" ${access_database} ${table} > "${output_dir}/${table}.csv"
done
echo "-- End export tables"