from sqlalchemy import Column, ForeignKey, Integer, String

from wedc.infrastructure.database import dbase, session_scope, load_session


class LabelledData(dbase):
    __tablename__ = 'labelled_data'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(1*1024*1024), nullable=False)
    label = Column(Integer, nullable=False)
    checksum = Column(String(50), nullable=False)

    """ use flag to note data
    0: normal data
    1: groundtruth
    2: need to check manually
    """
    flag = Column(Integer, nullable=False)

    @staticmethod
    def calc_checksum(content):
        return 'test'

    @staticmethod
    def insert(content, label, flag):
        with session_scope() as session:
            new_data = LabelledData(content=content, 
                            label=label,
                            checksum=LabelledData.calc_checksum(content),
                            flag=flag)
            session.add(new_data)

    # def delete()
    @staticmethod
    def load_data():
        session = load_session()
        return session.query(LabelledData).all()

    


