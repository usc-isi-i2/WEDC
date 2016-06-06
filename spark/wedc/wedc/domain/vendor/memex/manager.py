"""

https://happybase.readthedocs.org/en/latest/

"""


import happybase
import yaml
import time
import os
import re

pool = happybase.ConnectionPool(size=3, host='10.1.94.57')

HBASE_DOC_TAG_MAIN = 'doc_id'
HBASE_DOC_TAG_DOC_ID = 'doc_id'
HBASE_DOC_TAG_DOC_URL = 'url'
HBASE_DOC_TAG_DOC_EXTRACTIONS = 'extractions'
HBASE_DOC_TAG_DOC_TITLE = 'title'
HBASE_DOC_TAG_DOC_TEXT = 'text'
HBASE_DOC_TAG_DOC_RESULTS = 'results'


def load_all_data_to_disk(table_name, row_start=None, limit=10, output_file_path=None):
    start_time = time.time()
    if output_file_path:
        fh = open(output_file_path, 'wb')
        with pool.connection() as connection:   # try exception needed
            table = connection.table(table_name)
            count = 0
            for key, data in table.scan(row_start=None, 
                                        row_stop=None, 
                                        row_prefix=None, 
                                        columns=None, 
                                        filter=None,
                                        timestamp=None, 
                                        include_timestamp=False, 
                                        batch_size=100, 
                                        scan_batching=None, 
                                        limit=limit,
                                        sorted_columns=False
                                        ):
                obj = yaml.safe_load(data['ht:ads_doc'])

                if HBASE_DOC_TAG_DOC_EXTRACTIONS in obj:
                    extractions = obj[HBASE_DOC_TAG_DOC_EXTRACTIONS]

                    if HBASE_DOC_TAG_DOC_TEXT in extractions:
                        text= ' '.join(extractions[HBASE_DOC_TAG_DOC_TEXT][HBASE_DOC_TAG_DOC_RESULTS])
                        try:
                            text = text.encode('ascii', 'ignore')
                            text = re.sub(r'[\t\n\r\\]', ' ', text)
                            text = re.sub(r'<[^>]+>', ' ', text)
                            fh.write(text + '\n')
                        except Exception:
                            print text

                        
    time_cost = time.time() - start_time
    
    print time_cost

def load_all_data(table_name, row_start=None, limit=10, output_file_path=None):
    """ Take too much time if dataset is very huge
    """
    
    docs = []

    with pool.connection() as connection:   # try exception needed
        table = connection.table(table_name)
        count = 0
        for key, data in table.scan(row_start=None, 
                                    row_stop=None, 
                                    row_prefix=None, 
                                    columns=None, 
                                    filter=None,
                                    timestamp=None, 
                                    include_timestamp=False, 
                                    batch_size=100, 
                                    scan_batching=None, 
                                    limit=limit,
                                    sorted_columns=False
                                    ):
            obj = yaml.safe_load(data['ht:ads_doc'])

            doc = {}

            if HBASE_DOC_TAG_DOC_ID in obj:
                doc.setdefault(HBASE_DOC_TAG_DOC_ID, obj[HBASE_DOC_TAG_DOC_ID])

            if HBASE_DOC_TAG_DOC_URL in obj:
                doc.setdefault(HBASE_DOC_TAG_DOC_URL, obj[HBASE_DOC_TAG_DOC_URL])

            if HBASE_DOC_TAG_DOC_EXTRACTIONS in obj:
                extractions = obj[HBASE_DOC_TAG_DOC_EXTRACTIONS]

                if HBASE_DOC_TAG_DOC_TITLE in extractions:
                    text= ' '.join(extractions[HBASE_DOC_TAG_DOC_TITLE][HBASE_DOC_TAG_DOC_RESULTS])
                    doc.setdefault(HBASE_DOC_TAG_DOC_TITLE, text)

                if HBASE_DOC_TAG_DOC_TEXT in extractions:
                    text= ' '.join(extractions[HBASE_DOC_TAG_DOC_TEXT][HBASE_DOC_TAG_DOC_RESULTS])
                    doc.setdefault(HBASE_DOC_TAG_DOC_TEXT, text)

                docs.append(doc)
                count += 1

            else:
                continue

            # isi_id = obj['isi_id']
            # doc_id = obj['doc_id']
            # url = obj['url']
            # extractions = obj['extractions']
            # title = ' '.join(extractions['title']['results'])
            # text= ' '.join(extractions['text']['results'])
    
    


    time_cost = time.time() - start_time 
    # print docs
    return time_cost



# print load_all_data('dig_isi_cdr2_ht_ads_2016')




"""
# connection = happybase.Connection('10.1.94.57')
# print connection.tables()

table = connection.table('dig_isi_cdr2_ht_ads_2016')

for key, data in table.scan(row_start=None, row_stop=None, row_prefix=None, columns=None, filter=None,timestamp=None, include_timestamp=False, batch_size=1000, scan_batching=None, limit=None,sorted_columns=False):
    # print key
    # print data['ht:ads_doc']
    obj = yaml.safe_load(data['ht:ads_doc'])
    isi_id = obj['isi_id']
    doc_id = obj['doc_id']
    url = obj['url']
    extractions = obj['extractions']
    title = ' '.join(extractions['title']['results'])
    text= ' '.join(extractions['text']['results'])

    print doc_id,title, url, text
    break




# print table.row('0000EEAFBAB6B2DBE0EC748FE24D096593577640FA085F38B2966812766B7E97')
# print table.row('0000EEAFBAB6B2DBE0EC748FE24D096593577640FA085F38B2966812766B7E97', columns=['ht:ads_doc'])

table_name = 'dig_isi_cdr2_ht_ads_2016'
with pool.connection() as connection:
    table = connection.table(table_name)
    row = table.row('0000EEAFBAB6B2DBE0EC748FE24D096593577640FA085F38B2966812766B7E97', columns=['ht:ads_doc', 'ht:url'])
    print row['ht:url']

"""