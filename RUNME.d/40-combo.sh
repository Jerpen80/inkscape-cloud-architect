make_command "all" "Build and install everything (correct order)."
all(){
  symbols_build && symbols_install && templates_install && extension_install
}

make_command "clean" "Remove all installed assets."
clean(){
  symbols_clean
  templates_clean
  extension_clean
}
