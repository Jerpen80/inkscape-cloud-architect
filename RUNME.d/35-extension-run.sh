make_command "extension_run" "Run extension headless (args: data_dir region [account_name] [output.svg] [theme] [layout_mode])."
extension_run(){
  if [[ $# -lt 2 ]]; then
    echo "Usage: ./RUNME.sh extension_run <data_dir> <region> [account_name] [output.svg] [theme] [layout_mode]"
    echo "Example: ./RUNME.sh extension_run account-data/222222222222 eu-west-1"
    echo "Example: ./RUNME.sh extension_run account-data/222222222222 eu-west-1 'My Account'"
    echo "Example: ./RUNME.sh extension_run account-data/222222222222 eu-west-1 'My Account' output.svg dark dense"
    return 1
  fi

  local data_dir="$1"
  local region="$2"
  local account_name="${3:-}"
  local output="${4:-output.svg}"
  local theme="${5:-light}"
  local layout_mode="${6:-spaced}"
  local ext_dir="$RUNME_DIR/extensions/aws-auto-diagram"

  # Check inkex is available
  if ! python3 -c "import inkex" 2>/dev/null; then
    echo "Error: inkex not available. Run inside 'nix develop' shell."
    return 1
  fi

  # Call the render engine directly (pure Python import, no subprocess, no
  # blank-SVG dance). The engine returns SVG; we write it to $output.
  ICA_DATA_DIR="$data_dir" ICA_REGION="$region" ICA_ACCOUNT_NAME="$account_name" \
  ICA_THEME="$theme" ICA_LAYOUT_MODE="$layout_mode" ICA_OUTPUT="$output" \
  PYTHONPATH="$ext_dir:${PYTHONPATH:-}" python3 - <<'PYEOF'
import os
from ica_utils.engine import render

svg = render(
    data_dir=os.environ["ICA_DATA_DIR"],
    region=os.environ["ICA_REGION"],
    account_name=os.environ.get("ICA_ACCOUNT_NAME", ""),
    theme=os.environ.get("ICA_THEME", "light"),
    layout_mode=os.environ.get("ICA_LAYOUT_MODE", "spaced"),
)
with open(os.environ["ICA_OUTPUT"], "w") as f:
    f.write(svg)
PYEOF

  local exit_code=$?
  if [[ $exit_code -eq 0 ]]; then
    echo "Output: $output"
  else
    echo "Extension failed with exit code $exit_code"
  fi
  return $exit_code
}
