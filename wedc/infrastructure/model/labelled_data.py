from sqlalchemy import Column, ForeignKey, Integer, String

from wedc.infrastructure.database import dbase, session_scope, load_session


class LabelledData(dbase):
    __tablename__ = 'labelled_data'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(1*1024*1024), nullable=False)
    label = Column(Integer, nullable=False)
    checksum = Column(String(200), nullable=False)

    """ use flag to note data
    0: normal data
    1: groundtruth
    2: need to check manually
    """
    flag = Column(Integer, nullable=False)

    @staticmethod
    def calc_checksum(content):
        import hashlib
        hashobj = hashlib.sha256()
        hashobj.update(content.strip())
        hash_value = hashobj.hexdigest().lower()
        return hash_value

    @staticmethod
    def insert(content, label, flag):
        checksum = LabelledData.calc_checksum(content)
        with session_scope() as session:
            # filter dups
            if not session.query(LabelledData).filter_by(checksum=checksum).all():
                new_data = LabelledData(content=content, 
                                label=label,
                                checksum=checksum,
                                flag=flag)
                session.add(new_data)

    # def delete()
    @staticmethod
    def load_data():
        session = load_session()
        return session.query(LabelledData).all()

    


