Name:		hermes-agent
Version:	2026.9.11
Release:	1
Summary:	Self-improving AI agent from Nous Research
License:	MIT
Group:		Development/Other
URL:		https://github.com/NousResearch/hermes-agent
Source0:	https://github.com/NousResearch/hermes-agent/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
Source1:	hermes-wrapper.sh
Patch0:		0001-omv-system-python-llama-server.patch
BuildArch:	noarch
# Upstream pins exact PyPI versions in METADATA. The automatic
# pythonX.Ydist() generator would require those exact versions
# (and unpackaged firecrawl-anydoc). We list unversioned cooker
# modules below instead.
%global __requires_exclude ^python[0-9.]*dist\\(
BuildRequires:	python
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(wheel)
Requires:	python
Requires:	python%{pyver}dist(openai)
Requires:	python%{pyver}dist(certifi)
Requires:	python%{pyver}dist(python-dotenv)
Requires:	python%{pyver}dist(fire)
Requires:	python%{pyver}dist(httpx)
Requires:	python%{pyver}dist(rich)
Requires:	python%{pyver}dist(tenacity)
Requires:	python%{pyver}dist(pyyaml)
Requires:	python%{pyver}dist(ruamel.yaml)
Requires:	python%{pyver}dist(requests)
Requires:	python%{pyver}dist(jinja2)
Requires:	python%{pyver}dist(pydantic)
Requires:	python%{pyver}dist(prompt-toolkit)
Requires:	python%{pyver}dist(croniter)
Requires:	python%{pyver}dist(snowballstemmer)
Requires:	python%{pyver}dist(packaging)
Requires:	python%{pyver}dist(markdown)
Requires:	python%{pyver}dist(pyjwt)
Requires:	python%{pyver}dist(urllib3)
Requires:	python%{pyver}dist(cryptography)
Requires:	python%{pyver}dist(psutil)
Requires:	python%{pyver}dist(websockets)
Requires:	python%{pyver}dist(pathspec)
Requires:	python%{pyver}dist(fastapi)
Requires:	python%{pyver}dist(uvicorn)
Requires:	python%{pyver}dist(python-multipart)
Requires:	python%{pyver}dist(ptyprocess)
Requires:	python%{pyver}dist(pillow)
Recommends:	ollama
Recommends:	llama-cpp-server
Recommends:	ripgrep
Recommends:	git-core
Recommends:	ffmpeg
Recommends:	nodejs

%description
Hermes Agent is a self-improving AI agent built by Nous Research.
It adds skills, memory, cron, and messaging gateways on top of any
OpenAI-compatible endpoint.

This package uses the system llama-cpp (llama-server) and works with
Ollama at http://127.0.0.1:11434/v1. Run `hermes setup` or
`hermes model` after install. Do not use the upstream curl|bash
installer — it downloads its own Python and llama.cpp builds.

%prep
%autosetup -p1 -n %{name}-%{version}

# Drop trees we do not ship (desktop Electron, website, tests).
rm -rf apps website tests tests-js evals contributors docker nix \
	mcp-research-data datagen-config-examples MagicMock .github

%build
# Installed in %install (pip --root). Nothing to compile.

%install
# HERMES_NIX_BUILD lifts the upstream wheel/sdist guard (uv/Nix only).
export HERMES_NIX_BUILD=1
python -m pip install \
	--no-deps --no-build-isolation --no-compile \
	--root %{buildroot} --prefix %{_prefix} \
	.

install -d %{buildroot}%{_datadir}/%{name}
cp -a skills optional-skills locales optional-mcps \
	%{buildroot}%{_datadir}/%{name}/

# Prefer /usr/bin/python; wrap to point at bundled assets.
for cmd in hermes hermes-agent hermes-acp; do
	if [ -f %{buildroot}%{_bindir}/$cmd ]; then
		sed -i '1s|^#!/usr/bin/env python3|#!/usr/bin/python|' \
			%{buildroot}%{_bindir}/$cmd
		sed -i '1s|^#!/usr/bin/python3|#!/usr/bin/python|' \
			%{buildroot}%{_bindir}/$cmd
	fi
done

install -D -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/hermes-omv-wrap
# Keep the real CLIs as hermes.real etc.; public names go through the wrap.
for cmd in hermes hermes-agent hermes-acp; do
	if [ -f %{buildroot}%{_bindir}/$cmd ]; then
		mv %{buildroot}%{_bindir}/$cmd %{buildroot}%{_bindir}/$cmd.real
		sed "s|@CMD@|$cmd.real|" %{SOURCE1} \
			> %{buildroot}%{_bindir}/$cmd
		chmod 0755 %{buildroot}%{_bindir}/$cmd
	fi
done
rm -f %{buildroot}%{_bindir}/hermes-omv-wrap

%files
%license LICENSE
%doc README.md SOUL.md AGENTS.md
%{_bindir}/hermes
%{_bindir}/hermes.real
%{_bindir}/hermes-agent
%{_bindir}/hermes-agent.real
%{_bindir}/hermes-acp
%{_bindir}/hermes-acp.real
%{_datadir}/%{name}/
%{py_sitedir}/agent
%{py_sitedir}/tools
%{py_sitedir}/hermes_cli
%{py_sitedir}/gateway
%{py_sitedir}/tui_gateway
%{py_sitedir}/cron
%{py_sitedir}/acp_adapter
%{py_sitedir}/plugins
%{py_sitedir}/providers
%{py_sitedir}/*.py
%{py_sitedir}/hermes_agent-*.*-info
