# Run the following file using `python example.py`

from sqlalchemy import Column, Integer, ForeignKey, join, create_engine
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import mapper, relationship


# The following example is taken from the docs regarding a non primary relationship mapper
# http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#relationship-to-non-primary-mapper
Base = declarative_base()

class A(Base):
    __tablename__ = 'a'

    id = Column(Integer, primary_key=True)
    b_id = Column(ForeignKey('b.id'))
    a_json = Column(JSON)

class B(Base):
    __tablename__ = 'b'

    id = Column(Integer, primary_key=True)
    b_json = Column(JSON)

class C(Base):
    __tablename__ = 'c'

    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey('a.id'))
    c_json = Column(JSON)

class D(Base):
    __tablename__ = 'd'

    id = Column(Integer, primary_key=True)
    c_id = Column(ForeignKey('c.id'))
    b_id = Column(ForeignKey('b.id'))
    d_json = Column(JSON)

# 1. set up the join() as a variable, so we can refer
# to it in the mapping multiple times.
j = join(B, D, D.b_id == B.id).join(C, C.id == D.c_id)

# 2. Create a new mapper() to B, with non_primary=True.
# Columns in the join with the same name must be
# disambiguated within the mapping, using named properties.
B_viacd = mapper(B, j, non_primary=True, properties={
    "b_id": [j.c.b_id, j.c.d_b_id],
    "d_id": j.c.d_id
    })

A.b = relationship(B_viacd, primaryjoin=A.b_id == B_viacd.c.b_id)

# Create DB
engine = create_engine('postgresql://localhost/test_db')
Base.metadata.create_all(engine)

# If we associate `Mutable` with `JSON` then `A` can not be instantiated succesfully
Mutable.associate_with(JSON)
item1 = A()

