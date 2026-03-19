$env:PYTHONPATH = "."
.venv\Scripts\Activate.ps1
$basePrefix = python -c "import sys; print(sys.base_prefix)"
$env:TCL_LIBRARY = "$basePrefix\tcl\tcl8.6"
$env:TK_LIBRARY = "$basePrefix\tcl\tk8.6"
python -m icarus_sentinel.main
