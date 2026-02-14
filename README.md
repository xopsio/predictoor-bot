Install (dev):
  py -3.12 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install -U pip
  pip install -c constraints.txt -e .
