import argparse
import re
from pyspark import SparkContext
from wedc.domain.core.data.seed.seed_vector import generate_vector

# need redesign to a function that accept seeds and contains map()
def map_vectorize(data):
    key, tokens = data
    seeds = broadcast_seeds.value
    return (key, generate_vector(tokens, seeds))




