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


    @staticmethod
    def insert_from_txt(txt_file_path):
        with open(txt_file_path, 'rb') as txtfile:
            lines = txtfile.readlines()

            with session_scope() as session:
                for line in lines:
                    line = line.strip().lower()
                    line = line.split('\t')
                    new_data = SeedDict(seed=str(line[0]), weight=float(line[1]))
                    session.add(new_data)

    @staticmethod
    def load_data():
        session = load_session()
        return session.query(SeedDict).all()

    @staticmethod
    def clear_data():
        with session_scope() as session:
            num_rows_deleted = session.query(SeedDict).delete()
        return num_rows_deleted
    




  