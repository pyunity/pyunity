@echo off
set SPHINX_APIDOC_OPTIONS=members,inherited-members,show-inheritance
sphinx-apidoc -e -f -T -o docs\source\api\ pyunity pyunity\config.py pyunity\examples\
if not [%1] == [] (
sphinx-build -b html -a -E -j auto -v docs\source\ docs\en\
)