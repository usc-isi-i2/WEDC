# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-20 10:55:39
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-20 14:27:09





"""

spark-submit \
--conf "spark.yarn.executor.memoryOverhead=8192" \
--conf "spark.rdd.compress=true" \
--conf "spark.shuffle.compress=true" \
--driver-memory 6g \
--executor-memory 6g  --executor-cores 4  --num-executors 20 \
spark_workflow.py \
--input_file /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output \
--output_dir /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_lp \
--seed_file /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/spark_dependencies/seeds \
--labelled_data /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/spark_dependencies/labelled_data

spark-submit \
--conf "spark.yarn.executor.memoryOverhead=8192" \
--conf "spark.rdd.compress=true" \
--conf "spark.shuffle.compress=true" \
--driver-memory 6g \
--executor-memory 6g  --executor-cores 4  --num-executors 20 \
spark_workflow.py \
--input_file /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/memex_data \
--output_dir /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/spark_output \
--seed_file /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/spark_dependencies/seeds \
--labelled_data /Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/spark_dependencies/labelled_data

"""

import json
import sys
import os
import argparse
from pyspark import SparkContext, SparkConf, SparkFiles
from digSparkUtil.fileUtil import FileUtil

from wedc.domain.core.data.loader import generate_extraction
from wedc.domain.core.data.seed.seed_vector import generate_vector
from wedc.domain.core.ml.classifier.label_propagation import labelprop

# sys.path.insert(1, os.path.join(os.path.abspath(__file__), 'wedc', 'domain', 'vendor', 'en'))
# sys.path.append(os.path.join(os.path.dirname(__file__), 'wedc', 'domain', 'vendor'))


def load_jsonlines(sc, input, file_format='sequence', data_type='json', separator='\t'):
    fUtil = FileUtil(sc)
    rdd = fUtil.load_file(input, file_format=file_format, data_type=data_type, separator=separator)
    return rdd

def save_jsonlines(sc, rdd, output_dir, file_format='sequence', data_type='json', separator='\t'):
    fUtil = FileUtil(sc)
    fUtil.save_file(rdd, output_dir, file_format=file_format, data_type=data_type, separator=separator)

def load_labelled_data_file(path):
    labelled_data = []
    with open(path, 'rb') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            labelled_data.append([line[0], line[1]])
    return labelled_data

def load_seed_file(path):
    seeds = {}
    with open(path, 'rb') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            seeds.setdefault(line[0], line[1])
    return seeds

def extract_content(raw):
    if not raw:
        return ''
    content = []
    if isinstance(raw, basestring):
        content.append(raw)
    else:
        content = raw
    return ' '.join(content)


def run(sc, input_file, output_dir, seed_file, labelled_data_file):

    seeds = load_seed_file(seed_file)
    broadcast_seeds = sc.broadcast(seeds)

    labelled_data = load_labelled_data_file(labelled_data_file)
    broadcast_labelled_data = sc.broadcast(labelled_data)

    def map_load_data(data):
        key, json_obj = data
        text_list = []
        if 'description' in json_obj:
            desc = extract_content(json_obj['description'])
            text_list.append(desc)
        if 'name' in json_obj:
            name = extract_content(json_obj['name'])
            text_list.append(name)
        return (str(key), ' '.join(text_list))

    def map_clean(data):
        key, text = data
        return (key, generate_extraction(text))

    def map_vectorize(data):
        key, tokens = data
        seeds = broadcast_seeds.value
        return (key, generate_vector(tokens, seeds))

    def map_labelprop(iterator):
        labelled_data = broadcast_labelled_data.value
        
        return labelprop.run(list(iterator), labelled_data)

    # rdd = load_jsonlines(sc, input_file)

    # rdd = rdd.map(map_load_data).map(map_vectorize)

    rdd = sc.textFile(input_file)

    rdd = rdd.mapPartitions(map_labelprop)
    # ans = rdd.collect()
    # 
    rdd.saveAsTextFile(output_dir)


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i','--input_file', required=True)
    arg_parser.add_argument('-o','--output_dir')#, required=True)
    arg_parser.add_argument('-s','--seed_file', required=True)
    arg_parser.add_argument('-l','--labelled_data_file', required=True)

    args = arg_parser.parse_args()

    spark_config = SparkConf().setAppName('WEDC')
    sc = SparkContext(conf=spark_config)

    run(sc, args.input_file, args.output_dir, args.seed_file, args.labelled_data_file)