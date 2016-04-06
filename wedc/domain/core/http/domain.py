
import os

from wedc.domain.conf.storage import __res_dir__

__res_dir__

def get_domain_ext_list():
    path = os.path.join(__res_dir__, 'domain_ext_list')
    with open(path, 'r') as f:
        lines = f.readlines()
    return ''.join(lines).lower().split('\n')
    