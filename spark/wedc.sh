# export PYENCHANT_LIBRARY_PATH="/user/lteng/wedc/lib/libenchant.so.1.6.0" 
# PYSPARK_PYTHON=/user/lteng/wedc/venv/bin/python 

# export TENCHANTPATH=libenchant.so.1.6.0

# echo PYENCHANT_LIBRARY_PATH
# echo TENCHANTPATH

export PYTHON_EGG_CACHE="/tmp"

PYTHON_EGG_CACHE="/tmp"
export PYSPARK_PYTHON=python

# export PYSPARK_DRIVER_PYTHON=python

# export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:mylib
# export LD_LIBRARY_PATH=mylib
# MY_LIBRARY_PATH=./mylib
# export MY_LIBRARY_PATH
# hadoop fs -mkdir -p $MY_LIBRARY_PATH


# """
/usr/lib/spark/bin/spark-submit \
--master yarn-client \
--conf "spark.yarn.executor.memoryOverhead=8192" \
--conf "spark.shuffle.memoryFraction=0.5" \
--executor-memory 10g  --executor-cores 2  --num-executors 5 \
--py-files wedc-lib.zip,scipy-0.18.0.dev0_5a779fd-py2.7-linux-x86_64.egg,scikit_learn-0.18.dev0-py2.7-linux-x86_64.egg,Cython-0.24-py2.7-linux-x86_64.egg,nltk-3.2.1-py2.7.egg,nose2-0.6.2-py2.7.egg,pyenchant-1.6.7-py2.7.egg,digSparkUtil-1.0.23-py2.7.egg,inflection-0.3.1-py2.7.egg,numpy-1.11.0-py2.7-linux-x86_64.egg \
spark_entrance.py \
$@
# """

# --conf "spark.executorEnv.PYTHON_EGG_CACHE=${PYTHON_EGG_CACHE}" \
# --conf "spark.executorEnv.PYSPARK_PYTHON=${PYSPARK_PYTHON}" \
# --files mylib \
# --conf "spark.executorEnv.LD_LIBRARY_PATH=${MY_LIBRARY_PATH}:${LD_LIBRARY_PATH}" \
# --conf "spark.driver.extraLibraryPath=${MY_LIBRARY_PATH}" \
# --conf "spark.executor.extraLibraryPath=${MY_LIBRARY_PATH}" \


# --conf "spark.driver.extraJavaOptions python.import.site=false  " \
# --conf "spark.executor.extraJavaOptions python.import.site=false " \
# --py-files wedc-lib.zip,numpy,scipy-0.18.0.dev0_5a779fd-py2.7-linux-x86_64.egg,scikit_learn-0.18.dev0-py2.7-linux-x86_64.egg,Cython-0.24-py2.7-linux-x86_64.egg,nltk-3.2.1-py2.7.egg,nose2-0.6.2-py2.7.egg,pyenchant-1.6.7-py2.7.egg,digSparkUtil-1.0.23-py2.7.egg,inflection-0.3.1-py2.7.egg \
#  \

# export PYENCHANT_LIBRARY_PATH=libenchant.so.1.6.0
# --conf spark.executorEnv.PYENCHANT_LIBRARY_PATH=$PYENCHANT_LIBRARY_PATH \
# --conf spark.executorEnv.PYENCHANT_LIBRARY_PATH=libenchant.so.1.6.0 \

# --archives python-lib.zip \
# --py-files wedc-lib.zip,numpy,scipy-0.18.0.dev0_5a779fd-py2.7-linux-x86_64.egg,scikit_learn-0.18.dev0-py2.7-linux-x86_64.egg,Cython-0.24-py2.7-linux-x86_64.egg,nltk-3.2.1-py2.7.egg,nose2-0.6.2-py2.7.egg,pyenchant-1.6.7-py2.7.egg,digSparkUtil-1.0.23-py2.7.egg,inflection-0.3.1-py2.7.egg \
# --conf spark.executorEnv.PYTHON_EGG_CACHE="/tmp" \

# --conf PYENCHANT_LIBRARY_PATH=/user/lteng/wedc/lib/libenchant.so.1.6.0 \
# --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/user/lteng/wedc/venv/bin/python \

 # --master yarn-client \
 # --executor-memory 10g  --executor-cores 2  --num-executors 5 \
 # --py-files python-lib.zip \
# --jars spark-examples-1.6.1-hadoop2.6.0.jar


# --jars elasticsearch-hadoop-2.2.0-m1.jar,spark-examples_2.10-2.0.0-SNAPSHOT.jar,random-0.0.1-SNAPSHOT-shaded.jar,karma-spark-0.0.1-SNAPSHOT-shaded.jar  \
# /user/worker/hbase-dump-2015-10-01-2015-12-01-aman/webpage

#####
# spark-submit spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n' -s /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/seeds -l /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelled_data -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output --lp_jar /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar
#####

