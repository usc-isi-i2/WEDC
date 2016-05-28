import argparse
import re
from pyspark import SparkContext
from wedc.domain.core.data.seed.seed_vector import generate_vector

def map_vectorize(data):
    key, tokens = data
    
    return (key, tokens)
    # return (key, generate_vector(tokens, seeds))




