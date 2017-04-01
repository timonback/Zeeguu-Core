#@IgnoreInspection BashAddShebang
export PYTHONWARNINGS="ignore"
export ZEEGUU_CORE_CONFIG='./testing_default.cfg'
python -m unittest discover -v
export PYTHONWARNINGS="default"
