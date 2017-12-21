import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


Base = declarative_base()
 

class Restaurant(Base):
	__tablename__ = 'restaurant'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)

	@property
	def serialize(self):
		# return object data in easily serializeable format
		return {
			'id': self.id,
			'name': self.name
		}

class MenuItem(Base):
	__tablename__ = 'menu_item'
	
	name = Column(String(80), nullable=False)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(15))

	id = Column(Integer, primary_key=True)
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		# return object data in easily serializeable format
		return {
			'course': self.course,
			'description': self.description,
			'id': self.id,
			'name': self.name,
			'price': self.price
		}

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

