#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

function gen_stub()
{
  local stub_path=$1/__init__.py
  echo "Creating $stub_path..."
  cat > "$stub_path" <<'STUB'
#!/usr/bin/env python3
"""Package stub."""
STUB
}

export -f gen_stub

cd -- "$DIR"
find src/* test/* -type d -exec bash -c 'gen_stub "$0"' {} \;
