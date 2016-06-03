/usr/lib/spark/bin/spark-submit \
--master yarn-client \
--py-files python-lib.zip \
spark_entrance.py \
$@


 # --master yarn-client \
 # --executor-memory 10g  --executor-cores 2  --num-executors 5 \
 # --py-files python-lib.zip \
# --jars spark-examples-1.6.1-hadoop2.6.0.jar
# --conf "spark.driver.extraJavaOptions python.import.site=false  " \
# --conf "spark.executor.extraJavaOptions python.import.site=false " \
# --conf "spark.yarn.executor.memoryOverhead=8192" \
# --conf "spark.shuffle.memoryFraction=0.5" \

# --jars elasticsearch-hadoop-2.2.0-m1.jar,spark-examples_2.10-2.0.0-SNAPSHOT.jar,random-0.0.1-SNAPSHOT-shaded.jar,karma-spark-0.0.1-SNAPSHOT-shaded.jar  \
# /user/worker/hbase-dump-2015-10-01-2015-12-01-aman/webpage

#####
# spark-submit spark_entrance.py -i /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/webpage_jsonline.jsonl --input_file_format text --input_data_type jsonlines --input_separator '\n' -s /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/seeds -l /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelled_data -o /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output --lp_jar /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar
#####

