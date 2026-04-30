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
  local input_svg
  input_svg=$(mktemp --suffix=.svg)

  # Check inkex is available
  if ! python3 -c "import inkex" 2>/dev/null; then
    echo "Error: inkex not available. Run inside 'nix develop' shell."
    return 1
  fi

  # Create minimal blank SVG
  cat > "$input_svg" <<'SVGEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="800" height="600" viewBox="0 0 800 600">
  <defs/>
</svg>
SVGEOF

  # Run extension
  PYTHONPATH="$ext_dir:${PYTHONPATH:-}" python3 "$ext_dir/aws-auto-diagram.py" \
    --theme="$theme" \
    --layout_mode="$layout_mode" \
    --account_name="$account_name" \
    --data_dir="$data_dir" \
    --region="$region" \
    --output="$output" \
    "$input_svg"

  local exit_code=$?
  rm -f "$input_svg"

  if [[ $exit_code -eq 0 ]]; then
    echo "Output: $output"
  else
    echo "Extension failed with exit code $exit_code"
  fi
  return $exit_code
}
