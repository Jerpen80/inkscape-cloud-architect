make_command "symbols_build" "Build SVG symbols from AWS asset zip."
symbols_build(){
  cd "$RUNME_DIR/symbols/aws-inkscape-symbols" && ./build.sh "$ASSETS_ZIP"
}

make_command "symbols_install" "Install symbols to Inkscape."
symbols_install(){
  mkdir -p "$INKSCAPE_DIR/symbols/aws-architect"
  rsync -av "$RUNME_DIR/symbols/aws-inkscape-symbols/target/" "$INKSCAPE_DIR/symbols/aws-architect/"
}

make_command "symbols_clean" "Remove installed symbols."
symbols_clean(){
  rm -Rfv "$INKSCAPE_DIR/symbols/aws-architect"
}

make_command "symbols_clean_cache" "Remove awslabs repo cache."
symbols_clean_cache(){
  rm -Rfv "$RUNME_DIR/symbols/aws-inkscape-symbols/awslabs-repo"
}
