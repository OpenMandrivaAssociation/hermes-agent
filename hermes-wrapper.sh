#!/bin/sh
# Distro wrapper: bundled skills/locales + system python/llama-server.
prefix=/usr
datadir=${prefix}/share/hermes-agent
export HERMES_BUNDLED_SKILLS="${HERMES_BUNDLED_SKILLS:-$datadir/skills}"
export HERMES_OPTIONAL_SKILLS="${HERMES_OPTIONAL_SKILLS:-$datadir/optional-skills}"
export HERMES_BUNDLED_LOCALES="${HERMES_BUNDLED_LOCALES:-$datadir/locales}"
export HERMES_OPTIONAL_MCPS="${HERMES_OPTIONAL_MCPS:-$datadir/optional-mcps}"
export HERMES_BIN="${HERMES_BIN:-$prefix/bin/hermes}"
export HERMES_PYTHON="${HERMES_PYTHON:-$prefix/bin/python}"
if [ -x "$prefix/bin/node" ]; then
	export HERMES_NODE="${HERMES_NODE:-$prefix/bin/node}"
fi
exec "$prefix/bin/@CMD@" "$@"
