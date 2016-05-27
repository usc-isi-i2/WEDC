import sys
import os

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'data')
imd_data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'imd_san-francisco-maria-2.json'))



from pyspark import SparkContext,SparkConf
# from wedc.domain.entities.post import Post
from wedc.domain.core.data.loader import generate_extraction
from wedc.domain.conf.storage import __res_dir__
import word2vec


APP_NAME = "WEDC"

def loadData(line):
    import json
    value = json.loads(line)
    return [value['sid'], generate_extraction(value['content'])]

if __name__ == '__main__':

    sc = SparkContext(appName=APP_NAME)

    distFile = sc.textFile(imd_data_, minPartitions=5)
    parsedData = distFile.map(loadData)
    print parsedData.collect()

    sc.stop()