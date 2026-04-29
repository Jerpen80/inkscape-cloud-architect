make_command "templates_install" "Install templates to Inkscape."
templates_install(){
  mkdir -p "$INKSCAPE_DIR/templates/aws-architect"
  rsync -av "$RUNME_DIR/templates/" "$INKSCAPE_DIR/templates/aws-architect/"
}

make_command "templates_clean" "Remove installed templates."
templates_clean(){
  rm -Rfv "$INKSCAPE_DIR/templates/aws-architect"
}
