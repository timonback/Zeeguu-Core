#@IgnoreInspection BashAddShebang
export PYTHONWARNINGS="ignore"

if [ -z $ZEEGUU_CORE_CONFIG ]; then
	export ZEEGUU_CORE_CONFIG='./testing_default.cfg'
fi

python -m unittest discover -v
return_value=$?
export PYTHONWARNINGS="default"
exit $return_value