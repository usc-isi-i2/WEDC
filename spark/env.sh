#!/bin/bash

# BASEDIR=`dirname $0`

# export PYENCHANT_LIBRARY_PATH="/user/lteng/wedc/lib/libenchant.so.1.6.0" 

# export TENCHANTPATH="$BASEDIR/lib/libenchant.so.1.6.0"

# echo $PYENCHANT_LIBRARY_PATH
# echo $TENCHANTPATH

# ldd --version

echo 'hello LD_LIBRARY_PATH'
echo $LD_LIBRARY_PATH

echo 'hello kernel'
uname -a

echo 'hello distribution release'
cat /etc/*-release

echo 'hello lsb_release'
lsb_release -a

echo 'kernel version and gcc version'
cat /proc/version

echo 'hello python'

pp=$(readlink -f $(which python) | xargs -I % sh -c 'echo -n "%: "; % -V')
pp -V
# BASEDIR=`dirname $0`

# if [ ! -d "$BASEDIR/env" ]; then
#     virtualenv -q $BASEDIR/env --prompt='(wedc-spark) '
#     echo "Virtualenv created."
# fi

# cd $BASEDIR
# source $BASEDIR/env/bin/activate
# echo "Virtualenv activated."

# if [ ! -f "$BASEDIR/env/updated" -o $BASEDIR/setup.py -nt $BASEDIR/env/updated ]; then
#     pip install -e $BASEDIR
#     touch $BASEDIR/env/updated
#     echo "Requirements installed."
# fi

# pip install -r $BASEDIR/requirements.txt


# SPARK_YARN_USER_ENV="PYSPARK_PYTHON=/user/lteng/wedc/venv/bin/python"
# VENV="/user/lteng/wedc/venv"
# source $VENV/bin/activate

# SPARK_YARN_USER_ENV=python
# source activate

