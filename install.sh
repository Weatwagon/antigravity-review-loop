#!/usr/bin/env bash
#
# Antigravity Review Loop Plugin Installer for macOS and Linux
#

set -euo pipefail

echo "========================================================"
echo "  Google Antigravity Review Loop Plugin Installer       "
echo "========================================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.gemini/config/plugins/review-loop"
CONFIG_JSON="${HOME}/.gemini/config/config.json"

echo "[*] Source: ${SCRIPT_DIR}"
echo "[*] Destination: ${TARGET_DIR}"

# Create target directory
mkdir -p "${TARGET_DIR}"

# Copy files
echo "[*] Installing plugin files..."
cp -R "${SCRIPT_DIR}/plugin.json" "${TARGET_DIR}/"
cp -R "${SCRIPT_DIR}/rules" "${TARGET_DIR}/"
cp -R "${SCRIPT_DIR}/skills" "${TARGET_DIR}/"
echo "    ✓ Copied plugin.json, rules/, and skills/"

# Ensure enabled in config.json if python is available
if [ -f "${CONFIG_JSON}" ] && command -v python3 >/dev/null 2>&1; then
    python3 -c "
import json
try:
    with open('${CONFIG_JSON}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    if 'plugins' not in data:
        data['plugins'] = {}
    if 'review-loop' not in data['plugins']:
        data['plugins']['review-loop'] = {'enabled': True}
        with open('${CONFIG_JSON}', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print('    ✓ Enabled review-loop in config.json')
    else:
        print('    ✓ review-loop already enabled in config.json')
except Exception as e:
    print('    [!] Could not auto-update config.json:', e)
"
fi

echo ""
echo "========================================================"
echo "  Installation Complete!                                "
echo "========================================================"
echo "You can now use /review-loop in Antigravity:"
echo "  start /reviewLoop PM 8-4 DR 90%-3"
echo "  /review-loop"
echo ""
