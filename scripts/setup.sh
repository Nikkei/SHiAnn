#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NEOLOGD_DIR="${PROJECT_ROOT}/external/mecab-ipadic-neologd"

NEOLOGD_REPO="https://github.com/neologd/mecab-ipadic-neologd.git"
NEOLOGD_COMMIT="abc61e33d8be3d0ead202e6b1df064c72d5ccf11"
NEOLOGD_INSTALL_DIR="${HOME}/local/lib/mecab/dic/mecab-ipadic-neologd"

cd "${PROJECT_ROOT}"

# Check dependencies
for command in uv git mecab mecab-config; do
    command -v "${command}" >/dev/null 2>&1 || {
        echo "ERROR: ${command} is not installed."
        exit 1
    }
done

# Python environment
echo "==> Syncing Python environment"
uv sync --no-dev

# MeCab configuration
MECAB_SYSCONF_DIR="$(mecab-config --sysconfdir)"
MECABRC_PATH="${MECAB_SYSCONF_DIR}/mecabrc"

if [[ ! -f "${MECABRC_PATH}" ]]; then
    echo "ERROR: mecabrc was not found:"
    echo "    ${MECABRC_PATH}"
    exit 1
fi

echo "==> MeCab configuration: ${MECABRC_PATH}"

# mecab-ipadic-NEologd
mkdir -p "$(dirname "${NEOLOGD_DIR}")"

if [[ ! -d "${NEOLOGD_DIR}/.git" ]]; then
    echo "==> Cloning mecab-ipadic-NEologd"
    git clone "${NEOLOGD_REPO}" "${NEOLOGD_DIR}"
fi

echo "==> Checking out NEologd commit ${NEOLOGD_COMMIT}"
git -C "${NEOLOGD_DIR}" fetch
git -C "${NEOLOGD_DIR}" checkout "${NEOLOGD_COMMIT}"

CURRENT_COMMIT="$(git -C "${NEOLOGD_DIR}" rev-parse HEAD)"

if [[ "${CURRENT_COMMIT}" != "${NEOLOGD_COMMIT}" ]]; then
    echo "ERROR: Failed to checkout the expected NEologd commit."
    exit 1
fi

# Install NEologd
echo "==> Installing NEologd"
"${NEOLOGD_DIR}/bin/install-mecab-ipadic-neologd" \
    -n \
    -y \
    -p "${NEOLOGD_INSTALL_DIR}"

if [[ ! -d "${NEOLOGD_INSTALL_DIR}" ]]; then
    echo "ERROR: NEologd installation failed."
    exit 1
fi

# Environment
cat > "${PROJECT_ROOT}/.env" <<EOF
MECABRC=${MECABRC_PATH}
NEOLOGD_PATH=${NEOLOGD_INSTALL_DIR}
EOF

# Verify
echo "==> Verifying MeCab + NEologd"

uv run --no-dev python - <<'PY'
import os

import MeCab
from dotenv import load_dotenv

load_dotenv(".env")

mecabrc = os.environ["MECABRC"]
neologd = os.environ["NEOLOGD_PATH"]

print("MECABRC_PATH:", mecabrc)
print("NEOLOGD_PATH:", neologd)

tagger = MeCab.Tagger(
    f"-r {mecabrc} -d {neologd}"
)

print()
print(tagger.parse("自然言語処理の研究しています。"))
PY

echo "==> Environment setup completed successfully."
