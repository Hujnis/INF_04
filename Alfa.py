
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table
from sqlalchemy.orm import relationship
import datetime

BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')


#  STRUCTURE: forms -> section -> block -> item 
FormGroupModel = Table('forms_groups', BaseModel.metadata,
        Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
        Column('form_id', ForeignKey('form.id'), primary_key=True),
        Column('group_id', ForeignKey('groups.id'), primary_key=True)
)


class FormModel(BaseModel):
    __tablename__ = 'forms'

    id = id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)

    groups = relationship('GroupModel', secondary=FormGroupModel, back_populates='forms')

class SectionModel(BaseModel):
    __tablename__ = 'sections'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)

    externalId = Column(String, index=True)

    sictiontype_id = Column(ForeignKey('sectiontypes.id'))

    sectiontype = relationship('SectionTypeModel', back_populates='sections')

    forms = relationship('FormModel', secondary=FormGroupModel, back_populates='sections')