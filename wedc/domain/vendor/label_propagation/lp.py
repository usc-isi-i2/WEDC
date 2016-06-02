import os
from pyspark import SparkContext
from py4j.java_gateway import java_import

def run_by_py4j(do_lp, data, iter=100, eps=0.00001):
    # sc = SparkContext(appName="LabelProp")
    # java_import(sc._jvm, "org.ooxo.*")
    # lp = sc._jvm.LProp()
    # raw_output = lp.do_lp(lines, eps, iter)
    raw_output = do_lp(lines, eps, iter)
    return refine_result(raw_output)

def run_by_jar(input, output=None, iter=100, eps=0.00001):
    import ast
    import subprocess
    from subprocess import check_output
    from decimal import Decimal
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

