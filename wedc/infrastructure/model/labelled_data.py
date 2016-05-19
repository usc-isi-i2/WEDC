from sqlalchemy import Column, ForeignKey, Integer, String

from wedc.infrastructure.database import dbase, session_scope, load_session
from wedc.domain.core.common import hash_helper

class LabelledData(dbase):
    __tablename__ = 'labelled_data'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(1*1024*1024), nullable=False)
    # extraction = Column(String(1*1024*1024), nullable=False)
    label = Column(Integer, nullable=False)
    checksum = Column(String(200), nullable=False)

    """ use flag to note data
    0: normal data
    1: groundtruth
    2: need to check manually
    """
    flag = Column(Integer, nullable=False)

    @staticmethod
    def insert(content, label, flag):
        checksum = hash_helper.checksum(content)
        with session_scope() as session:
            # filter dups
            if not session.query(LabelledData).filter_by(checksum=checksum).all():
                new_data = LabelledData(content=content, 
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
    


