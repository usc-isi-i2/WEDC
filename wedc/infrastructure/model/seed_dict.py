from sqlalchemy import Column, ForeignKey, Integer, String, Float

from wedc.infrastructure.database import dbase, session_scope, load_session
from wedc.domain.core.common import hash_helper

class SeedDict(dbase):
    __tablename__ = 'seed_dict'
    
    id = Column(Integer, primary_key=True)
    seed = Column(String(100), nullable=False)
    weight = Column(Float, nullable=False)

    @staticmethod
    def insert(content, label, flag):
        with session_scope() as session:
            new_data = SeedDict(seed=seed, weight=weight)
            session.add(new_data)

    """
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
    """

    @staticmethod
    def load_data():
        session = load_session()
        return session.query(SeedDict).all()

    @staticmethod
    def clear_data():
        with session_scope() as session:
            num_rows_deleted = session.query(SeedDict).delete()
        return num_rows_deleted
    


