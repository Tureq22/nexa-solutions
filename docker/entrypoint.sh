#!/bin/sh

set -e

echo "Aguardando o banco de dados..."

python - <<'PY'
import os
import socket
import sys
import time

host = os.environ.get("POSTGRES_HOST", "db")
port = int(os.environ.get("POSTGRES_PORT", "5432"))

for tentativa in range (1, 61):
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Banco disponivel em {host}: {port}.")
            sys.exit(0)
    except OSError:
        print(f"Tentativa {tentativa}/60 - banco indisponivel ainda.")
        time.sleep(1)

print(f"Banco respondeu em {host}:{port}. Abortando.", file=sys.stderr)
sys.exit(1)
PY

echo "Aplicando migrações..."
python manage.py migrate --noinput

exec "$@"