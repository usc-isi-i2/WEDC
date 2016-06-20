# @Author: ZwEin
# @Date:   2016-06-20 10:55:48
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-20 11:23:12


/usr/lib/spark/bin/spark-submit \
--master yarn-client \
--conf "spark.yarn.executor.memoryOverhead=8192" \
--conf "spark.shuffle.memoryFraction=0.5" \
--executor-memory 10g  --executor-cores 2  --num-executors 5 \
--py-files wedc-lib.zip,scipy-0.18.0.dev0_5a779fd-py2.7-linux-x86_64.egg,scikit_learn-0.18.dev0-py2.7-linux-x86_64.egg,Cython-0.24-py2.7-linux-x86_64.egg,nltk-3.2.1-py2.7.egg,nose2-0.6.2-py2.7.egg,pyenchant-1.6.7-py2.7.egg,digSparkUtil-1.0.23-py2.7.egg,inflection-0.3.1-py2.7.egg,numpy-1.11.0-py2.7-linux-x86_64.egg \
spark_entrance.py \
$@