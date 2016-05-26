from pyspark import SparkContext,SparkConf

from wedc.domain.conf.storage import __res_dir__
import word2vec


APP_NAME = "WEDC"

if __name__ == '__main__':

    sc = SparkContext(appName=APP_NAME)

    textFile = sc.textFile("README.md")
    print textFile.count()
    print 'storage dir: ', __res_dir__
    sc.stop()