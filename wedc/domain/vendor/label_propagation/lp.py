import os
import ast
# import subprocess

from pyspark import SparkContext
from pyspark import SparkConf
from pyspark import SparkFiles
from py4j.java_gateway import java_import
from py4j.java_gateway import JavaGateway
from subprocess import check_output
from decimal import Decimal

def run_by_py4j(data, iter=100, eps=0.00001):
    lp_runnable_jar_ = SparkFiles.get('labelprop.jar')
    eps = '%.e' % Decimal(eps)  # change decimal into e format
    argsArray = ['java', '-classpath', lp_runnable_jar_, 'org.ooxo.LProp', '-a', 'GFHF', '-m', str(iter), '-e', eps, data]
    raw_output = check_output(argsArray)


    # spark_config = SparkConf().setMaster('local').setAppName('test').set("labelprop.jar", SparkFiles.get('labelprop.jar')) 
    # sc = SparkContext(conf=spark_config)
    # java_import(sc._jvm, "org.ooxo.*")
    # lp = sc._jvm.LProp()

    # gateway = JavaGateway()
    # java_import(gateway.jvm, "org.ooxo.*")
    # lp = gateway.jvm.LProp()
    # raw_output = lp.do_lp(lines, eps, iter)
    return refine_result(raw_output)

def run_by_jar(input, output=None, iter=100, eps=0.00001):
    from wedc.domain.conf.storage import __res_dir__

    lp_runnable_jar_ = os.path.expanduser(os.path.join(__res_dir__, 'labelprop.jar'))

    # run label propagation
    eps = '%.e' % Decimal(eps)  # change decimal into e format
    argsArray = ['java', '-classpath', lp_runnable_jar_, 'org.ooxo.LProp', '-a', 'GFHF', '-m', str(iter), '-e', eps, input]
    raw_output = check_output(argsArray)

    # output into file
    if output:
        output_file = open(output, 'wb')
        output_file.writelines(raw_output)
        output_file.close()

    return refine_result(raw_output)

def refine_result(raw_output):
    ans = []
    for line in raw_output.split('\n'):
        if not line:    # actually in the end of file
            continue

        # line definition
        # line[0]: post id
        # line[1]: predict label
        # line[2:]: categories with weight
        line = ast.literal_eval(line)

        # filter invalid predictionobject
        if sum([float(_[1]) for _ in line[2:]]):
            ans.append(line)

    return ans

