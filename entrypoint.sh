#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ -z "${KOBO_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export KOBO_USER="${base_postgres_image_default_user}"
fi

python << END
import sys
import time

import psycopg

suggest_unrecoverable_after = 30
start = time.time()

while True:
    try:
        psycopg.connect(
            dbname="${KPI_DB}",
            user="${KOBO_USER}",
            password="${KOBO_PASSWORD}",
            host="${KOBO_HOST}",
            port="${KOBO_PORT}",
        )
        break
    except psycopg.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available...\n")

        if time.time() - start > suggest_unrecoverable_after:
            sys.stderr.write("  This is taking longer than expected. The following exception may be indicative of an unrecoverable error: '{}'\n".format(error))

    time.sleep(1)
END

>&2 echo 'PostgreSQL is available'

exec "$@"
