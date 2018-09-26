#!/bin/bash
set -eo pipefail
shopt -s nullglob

file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
		exit 1
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}
file_env 'DB_HOST'
file_env 'DB_USER'
file_env 'DB_PASSWORD'
file_env 'DB_NAME'
file_env 'BACKUP_PATH'

echo "$DB_HOST"
echo "$DB_USER"
echo "$DB_PASSWORD"
echo "$DB_NAME"
echo "$BACKUP_PATH"


export DB_HOST
export DB_USER
export DB_PASSWORD
export DB_NAME
export BACKUP_PATH

/usr/bin/python /usr/local/bin/entrypoint.py
