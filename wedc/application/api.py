import os
import sys

from wedc.domain.conf import configuration
from wedc.infrastructure.database import *


class WEDC():
    def __init__(self):
        self.config = configuration.load_config()

    # def initialize(self):
    #     session = self.initialize_db()

api = WEDC()




    
    


