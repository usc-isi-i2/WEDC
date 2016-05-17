

from wedc.infrastructure.database import dbase


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

