__echo_inkscape_dir(){
  echo "$INKSCAPE_DIR"
}

make_command "test_usage" "Test: all commands appear in usage output."
test_usage(){
  local expected_commands=(
    symbols_build symbols_install symbols_clean symbols_clean_cache
    templates_install templates_clean
    extension_install extension_clean extension_dev extension_run
    all clean
  )
  local usage_output
  usage_output=$("$RUNME_DIR/RUNME.sh" 2>&1)
  local failed=0
  for cmd in "${expected_commands[@]}"; do
    if ! echo "$usage_output" | grep -q "$cmd"; then
      echo "FAIL: command '$cmd' not found in usage output"
      failed=1
    fi
  done
  if [[ $failed -eq 0 ]]; then
    echo "PASS: all commands present in usage output"
  fi
  return $failed
}

make_command "test_inkscape_dir" "Test: INKSCAPE_DIR resolves correctly."
test_inkscape_dir(){
  local failed=0
  if [[ "$(uname)" == "Darwin" ]]; then
    local expected="$HOME/Library/Application Support/org.inkscape.Inkscape/config/inkscape"
  else
    local expected="$HOME/.config/inkscape"
  fi

  # Test auto-detection by running script with INKSCAPE_DIR unset
  local detected
  detected=$(unset INKSCAPE_DIR; "$RUNME_DIR/RUNME.sh" __echo_inkscape_dir 2>/dev/null)
  if [[ "$detected" != "$expected" ]]; then
    echo "FAIL: auto-detected INKSCAPE_DIR='$detected', expected='$expected'"
    failed=1
  else
    echo "PASS: auto-detected INKSCAPE_DIR is correct"
  fi

  # Test override
  local override="/tmp/test-inkscape-override"
  detected=$(INKSCAPE_DIR="$override" "$RUNME_DIR/RUNME.sh" __echo_inkscape_dir 2>/dev/null)
  if [[ "$detected" != "$override" ]]; then
    echo "FAIL: override INKSCAPE_DIR='$detected', expected='$override'"
    failed=1
  else
    echo "PASS: INKSCAPE_DIR override works"
  fi

  return $failed
}

make_command "test_install" "Test: install tasks put files in correct dirs."
test_install(){
  local tmpdir
  tmpdir=$(mktemp -d)
  local original_inkscape_dir="$INKSCAPE_DIR"
  INKSCAPE_DIR="$tmpdir"
  local failed=0

  # Test templates_install
  templates_install
  if [[ ! -d "$tmpdir/templates/aws-architect" ]]; then
    echo "FAIL: templates not installed to $tmpdir/templates/aws-architect"
    failed=1
  else
    echo "PASS: templates installed correctly"
  fi

  # Test extension_install
  extension_install
  if [[ ! -d "$tmpdir/extensions/aws-auto-diagram" ]]; then
    echo "FAIL: extension not installed to $tmpdir/extensions/aws-auto-diagram"
    failed=1
  else
    echo "PASS: extension installed correctly"
  fi

  # Test symbols_install (only if target/ exists)
  if [[ -d "$RUNME_DIR/symbols/aws-inkscape-symbols/target" ]]; then
    symbols_install
    if [[ ! -d "$tmpdir/symbols/aws-architect" ]]; then
      echo "FAIL: symbols not installed to $tmpdir/symbols/aws-architect"
      failed=1
    else
      echo "PASS: symbols installed correctly"
    fi
  else
    echo "SKIP: symbols_install (target/ not built)"
  fi

  # Cleanup
  rm -rf "$tmpdir"
  INKSCAPE_DIR="$original_inkscape_dir"
  return $failed
}

make_command "test_config_schema" "Test: config schema coverage, validation, preset_varying, defaults."
test_config_schema(){
  python3 "$RUNME_DIR/extensions/aws-auto-diagram/tests/test_config_schema.py"
}

make_command "test_ica_cli" "Test: ica CLI config-override parse/coerce/validate."
test_ica_cli(){
  python3 "$RUNME_DIR/extensions/aws-auto-diagram/tests/test_ica_cli.py"
}

make_command "test_all" "Run all tests."
test_all(){
  local failed=0
  test_usage || failed=1
  test_inkscape_dir || failed=1
  test_install || failed=1
  test_config_schema || failed=1
  test_ica_cli || failed=1
  if [[ $failed -eq 0 ]]; then
    echo -e "\nAll tests passed."
  else
    echo -e "\nSome tests failed."
  fi
  return $failed
}
