# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-20 11:18:39
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-20 12:23:44

import sys
import os

sys.path.append(os.path.join(os.path.abspath('..'), 'libs'))


class WEDC():

    PROGRAM_ENV_LOCAL = 'local'
    PROGRAM_ENV_SPARK = 'spark'

    def __init__(self, program_env='local'):
        self.program_env = program_env

    def set_program_env(self, program_env='local'):
        # local' or 'spark'

        st = program_env.lower()
        if program_env.lower() not in [PROGRAM_ENV_LOCAL, PROGRAM_ENV_SPARK] :
            raise Exception(program_env + ' is not a type of program environment, which should be "local" or "spark"')
        self.program_env = program_env

    




