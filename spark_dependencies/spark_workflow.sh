# @Author: ZwEin
# @Date:   2016-06-20 10:55:48
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-29 11:25:02


/usr/lib/spark/bin/spark-submit \
--master yarn-client \
--conf "spark.yarn.executor.memoryOverhead=8192" \
--conf "spark.shuffle.memoryFraction=0.5" \
--executor-memory 10g  --executor-cores 4  --num-executors 20 \
--py-files python_main.zip,python_lib.zip \
spark_workflow.py \
$@