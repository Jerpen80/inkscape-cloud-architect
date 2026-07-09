#!/usr/bin/env bash
#(C)2019-2026 Pim Snel - https://github.com/mipmip/RUNME.sh
CMDS=(); DESC=(); NARGS=$#; ARG1=$1;ALL_ARGS=("$@");make_command(){ CMDS+=($1);DESC+=("$2");};usage(){ printf "\nUsage: %s [command]\n\nCommands:\n" $0;line="              ";for ((i=0;i<=$((${#CMDS[*]}-1));i++));do printf "  %s %s ${DESC[$i]}\n" ${CMDS[$i]} "${line:${#CMDS[$i]}}";done;echo;};RUNME_DIR="$(cd "$(dirname "$0")" && pwd)";if [ -d "$RUNME_DIR/RUNME.d" ]; then for _f in "$RUNME_DIR/RUNME.d"/*.sh; do [ -f "$_f" ] && source "$_f"; done;fi;runme(){ if test $NARGS -ge 1; then "${ALL_ARGS[@]}"||usage;else usage;fi;}

ASSETS_ZIP=Icon-package_04302026.4705b90f5aa45b019271a2699e9ce9b97b941ee1.zip

if [[ -z "${INKSCAPE_DIR}" ]]; then
  if [[ "$(uname)" == "Darwin" ]]; then
    INKSCAPE_DIR="$HOME/Library/Application Support/org.inkscape.Inkscape/config/inkscape"
  else
    INKSCAPE_DIR="$HOME/.config/inkscape"
  fi
fi

runme
