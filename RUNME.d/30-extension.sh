make_command "extension_install" "Install extension to Inkscape."
extension_install(){
  mkdir -p "$INKSCAPE_DIR/extensions"
  cp -av "$RUNME_DIR/extensions/aws-auto-diagram" "$INKSCAPE_DIR/extensions/"
}

make_command "extension_clean" "Remove installed extension."
extension_clean(){
  rm -Rfv "$INKSCAPE_DIR/extensions/aws-auto-diagram"
}

make_command "extension_dev" "Auto-install extension while developing."
extension_dev(){
  echo "Auto installing extension. Press CTRL-C to quit."
  cd "$RUNME_DIR/extensions/aws-auto-diagram" && find | entr cp -av "$RUNME_DIR/extensions/aws-auto-diagram" "$INKSCAPE_DIR/extensions/"
}
