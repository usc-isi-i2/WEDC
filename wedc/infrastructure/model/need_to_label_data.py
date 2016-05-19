from sqlalchemy import Column, ForeignKey, Integer, String

from wedc.infrastructure.database import dbase, session_scope, load_session
from wedc.domain.core.common import hash_helper


class NeedToLabelData(dbase):
    __tablename__ = 'need_to_label_data'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(1*1024*1024), nullable=False)
    user_id = Column(Integer, nullable=False)
    # checksum = Column(String(200), nullable=False)    # compared before insert

    @staticmethod
    def insert(content, label, flag):
        # need to update
        checksum = hash_helper.checksum(content)
        with session_scope() as session:
            # filter dups
            if not session.query(NeedToLabelData).filter_by(checksum=checksum).all():
                new_data = NeedToLabelData(content=content, user_id=user_id)
                session.add(new_data)

    # def delete()
    @staticmethod
    def load_data():
        session = load_session()
        return session.query(NeedToLabelData).all()

    


