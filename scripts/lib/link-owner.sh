#!/bin/bash
# Sourced by install.sh and uninstall.sh: the one test for "this link is ours".
#
# link_owned_by <link> <owner_dir_physical> <depth>
# True when the link's target sits <depth> levels below the owner dir
# (commands/<category>/<file> = 2, skills/<skill> = 1). The ancestor is resolved
# with cd/pwd -P, so links made through a symlinked repo path match, and it
# survives a renamed category, so dangling links into the repo still match.
# realpath is avoided: older macOS lacks it.
link_owned_by() {
    local link="$1" owner="$2" depth="$3" up i
    up=$(readlink "$link") || return 1
    case "$up" in /*) ;; *) up="$(dirname "$link")/$up" ;; esac
    for ((i = 0; i < depth; i++)); do
        up=$(dirname "$up")
    done
    up=$(cd "$up" 2>/dev/null && pwd -P) || return 1
    [ "$up" = "$owner" ]
}
