
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, column
from sqlalchemy.orm import relationship
import datetime

BaseModel = declarative_base()

unitedSequence = Sequence('all_id_seq')


#  STRUCTURE: forms -> sections -> blocks -> items
FormGroupModel = Table('forms_groups', BaseModel.metadata,
        Column('id', BigInteger, Sequence('all_id_seq'), primary_key=True),
        Column('form_id', ForeignKey('forms.id'), primary_key=True),
        Column('section_id', ForeignKey('sections.id'), primary_key=True),
        Column('block_id', ForeignKey('blocks.id'), primary_key=True),
)


class FormModel(BaseModel):
    __tablename__ = 'forms'

    id = id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(BigInteger, index=True)

    sections = relationship('SectionModel',back_populates = 'form')

class SectionModel(BaseModel):
    __tablename__ = 'sections'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(String, index=True)

    #sectiontype_id = Column(ForeignKey('sectiontypes.id'))
    #sectiontype = relationship('SectionTypeModel', back_populates='sections')
    
    form_id = Column(BigInteger, index = True)

    form = relationship('FormModel', back_populates='sections')
    blocks = relationship('BlockModel', back_populates = 'section')

class BlockModel(BaseModel):
    __tablename__ = 'blocks'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(String, index=True)

    section_id = Column(BigInteger, index = True)

    section = relationship('SectionModel', back_populates='blocks')
    items = relationship('ItemModel', back_populates = 'block')

class ItemModel(BaseModel):
    __tablename__ = 'items'

    id = Column(BigInteger, Sequence('all_id_seq'), primary_key=True)
    name = Column(String)

    lastchange = Column(DateTime, default=datetime.datetime.now)
    externalId = Column(String, index=True)

    block_id = Column(BigInteger, index = True)
    block = relationship('BlockModel', back_populates='items')