#!/bin/bash -e

BASEDIR=`dirname $0`

if [ ! -d "$BASEDIR/env" ]; then
    virtualenv -q $BASEDIR/env --prompt='(wedc-spark) '
    echo "Virtualenv created."
fi

cd $BASEDIR
source $BASEDIR/env/bin/activate
echo "Virtualenv activated."

if [ ! -f "$BASEDIR/env/updated" -o $BASEDIR/setup.py -nt $BASEDIR/env/updated ]; then
    pip install -e $BASEDIR
    touch $BASEDIR/env/updated
    echo "Requirements installed."
fi

pip install -r $BASEDIR/requirements.txt


# SPARK_YARN_USER_ENV="PYSPARK_PYTHON=/user/lteng/wedc/venv/bin/python"
# VENV="/user/lteng/wedc/venv"
# source $VENV/bin/activate

# SPARK_YARN_USER_ENV=python
# source activate

