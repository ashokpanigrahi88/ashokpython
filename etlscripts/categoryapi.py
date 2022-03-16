import oratechetl.db as db
from sqlalchemy import (Column, Integer, Sequence, DateTime,
                        Date, BigInteger, Numeric, ForeignKey,
                        UniqueConstraint)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import oratechetl.commonutil as commonutility
import logging

_table_name = 'inv_item_categories'
_primary_key = 'category_id'
Base = declarative_base()
class  TableClass(object):
    __tablename__ = _table_name


setattr(TableClass,_primary_key,Column(Integer,Sequence(_table_name+'_s'), primary_key=True))

_Table = db.get_Table(_table_name)
mapper(TableClass,_Table)

data = {}
data_list =[{}]
def assignvalues(p_cls, p_data:{} = data):
    try:
        for key, value in db.AUDIT_COLUMNS.items():
            if hasattr(p_cls,key):
                setattr(p_cls,key,value)
    except Exception as ex:
        logging.error(ex)
    try:
        for key, value in p_data.items():
            if hasattr(p_cls,key):
                setattr(p_cls,key,value)
    except Exception as ex:
        logging.error(ex)




from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class Audtcolumns:
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    last_update_date = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, default=-1)
    last_updated_by = Column(Integer, default=-1)
    delete_flag = Column(String(1), default='N')
    update_source = Column(String(30), default='API')
    bu_id = Column(Integer, default=1)
    record_status = Column(String(1), default='I')
    third_party_source = Column(String(30))
    third_party_source_ref = Column(String(30))

class Category(Base, Audtcolumns):
    __tablename__ = 'inv_item_categories'
    __table_args__ = {'extend_existing': True}
    category_id = Column(Integer,Sequence(_table_name+'_s'), primary_key=True)
    category_code = Column(String)
    category_name = Column(String, unique=True)
    description = Column(String)
    #c_arcustitemexlcategories = relationship("ArCustItemExlcategories")
    #c_hruserassignments = relationship("HrUserAssignments")
    #c_invitemmasters = relationship("InvItemMasters")
    #c_invitemmulticategories = relationship("InvItemMultiCategories")
    c_invitemsubcategories = relationship("InvItemSubCategories")
    #c_invsimilarcategories = relationship("InvSimilarCategories")
    #c_prpricelistlines = relationship("PrPricelistLines")
    #c_wwwnodelinks = relationship("WwwNodeLinks")

class InvItemSubCategories(Base, Audtcolumns):
    __tablename__ = 'inv_item_sub_categories'
    __table_args__ = {'extend_existing': True}
    iic_category_id = Column(Integer, ForeignKey('inv_item_categories.category_id'),nullable=False)
    sub_category_id = Column(Integer,primary_key=True)
    sub_category_code = Column(String)
    sub_category_name = Column(String)
    description = Column(String)