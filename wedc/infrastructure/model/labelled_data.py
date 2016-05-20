from sqlalchemy import Column, ForeignKey, Integer, String

from wedc.infrastructure.database import dbase, session_scope, load_session
from wedc.domain.core.common import hash_helper

class LabelledData(dbase):
    __tablename__ = 'labelled_data'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(1*1024*1024), nullable=False)
    extraction = Column(String(1*1024*1024), nullable=False)
    label = Column(Integer, nullable=False)
    checksum = Column(String(200), unique=True, nullable=False)

    """ use flag to note data
    0: normal data
    1: groundtruth
    2: need to check manually
    """
    flag = Column(Integer, nullable=False)

    @staticmethod
    def insert(content, label, flag):
        from wedc.domain.entities.post import Post
        post = Post("", "", content)
        extraction = post.body
        checksum = hash_helper.checksum(content)
        with session_scope() as session:
            if not session.query(LabelledData).filter_by(checksum=checksum).all():
                new_data = LabelledData(content=content, 
                                extraction=extraction,
                                label=label,
                                checksum=checksum,
                                flag=flag)
                session.add(new_data)
           

    @staticmethod
    def insert_from_csv(csv_file_path):
        import csv
        from wedc.domain.entities.post import Post

        with open(csv_file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            with session_scope() as session:
                
                for idx, row in enumerate(reader):
                    post_id = idx + 1
                    label = row[0]
                    content = row[1].decode('ascii', 'ignore')
                    post = Post("", "", content)
                    extraction = post.body
                    checksum = hash_helper.checksum(extraction)

                    # filter dups
                    if not session.query(LabelledData).filter_by(checksum=checksum).all():
                        new_data = LabelledData(content=content,
                                        extraction=extraction, 
                                        label=label,
                                        checksum=checksum,
                                        flag=1)
                        session.add(new_data)
                    

    @staticmethod
    def load_data():
        session = load_session()
        return session.query(LabelledData).all()

    @staticmethod
    def clear_data():
        with session_scope() as session:
            num_rows_deleted = session.query(LabelledData).delete()
        return num_rows_deleted

    @staticmethod
    def load_potential_seeds():
        offset = 2 # offset from index to label
        labelled_data = LabelledData.load_data()
        tokens = {}
        for idx, data in enumerate(labelled_data):
            label = data.label
            for token in data.extraction.strip().split(' '):
                tokens.setdefault(str(token), [0, 0, 0])    # 2,3,4
                tokens[token][label-offset] += 1
            
        # print tokens
        ans = {}
        for token, cnt_list in tokens.items():
            max_cnt = max(cnt_list)
            max_cnt_idx = cnt_list.index(max_cnt)
            potential_flag = True
            if max_cnt == 0:
                continue
            for i, cnt in enumerate(cnt_list):
                if cnt == 0:
                    continue
                if i != max_cnt_idx:
                    if max_cnt == cnt or max_cnt < cnt * 3:
                        potential_flag = False
            if potential_flag:
                weight = 1.*max_cnt/sum(cnt_list)
                # print max_cnt, cnt_list, sum(cnt_list)
                label = max_cnt_idx + offset
                ans.setdefault(token, [weight, label])

        # print 'massage:\n', [k for k,v in ans.items() if v[1] == 2], '\n'
        # print 'escort:\n', [k for k,v in ans.items() if v[1] == 3], '\n'
        # print 'job_ads:\n', [k for k,v in ans.items() if v[1] == 4], '\n'

        return ans


