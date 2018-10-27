import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class SISTEMASIMPRESORAS(Base):
	__tablename__ = 'sistemasimpresoras'

	id = Column(Integer, primary_key=True)
	sede = Column(String(50), nullable=False)
	piso = Column(String(50), nullable=False)
	serie = Column(String(50), nullable=False)
	falla = Column(String(250), nullable=False)
	autor = Column(String(50), nullable=False)
	estado = Column(String(50), nullable=False)
	fecha_creacion = Column(DateTime, nullable=False)
	
class RRHHDIAESTUDIO(Base):
	__tablename__ = 'rrhhdiaestudio'

	id = Column(Integer, primary_key=True)
	apellidoynombre = Column(String(50), nullable=False)
	dni = Column(String(50), nullable=False)
	materia = Column(String(50), nullable=False)
	fecha = Column(String(50), nullable=False)
	autor = Column(String(50), nullable=False)
	estado = Column(String(50), nullable=False)
	fecha_creacion = Column(DateTime, nullable=False)
	
	
class COMERCIAL(Base):
	__tablename__ = 'comercial'

	id = Column(Integer, primary_key=True)
	apellidoynombre = Column(String(50), nullable=False)
	dni = Column(String(50), nullable=False)
	correo = Column(String(50), nullable=False)
	telefono = Column(String(50), nullable=False)
	evento = Column(String(50), nullable=False)
	autor = Column(String(50), nullable=False)
	estado = Column(String(50), nullable=False)
	fecha_creacion = Column(DateTime, nullable=False)
	
class OPERACIONES(Base):
	__tablename__ = 'operaciones'

	id = Column(Integer, primary_key=True)
	apellidoynombre = Column(String(50), nullable=False)
	sede = Column(String(50), nullable=False)
	piso = Column(String(50), nullable=False)
	inconveniente = Column(String(50), nullable=False)
	estado = Column(String(50), nullable=False)
	autor = Column(String(50), nullable=False)
	fecha_creacion = Column(DateTime, nullable=False)
	
class RRHHVACACIONES(Base):
	__tablename__ = 'rrhhvacaciones'

	id = Column(Integer, primary_key=True)
	apellidoynombre = Column(String(50), nullable=False)
	dni = Column(String(50), nullable=False)
	fechainicio = Column(String(50), nullable=False)
	fechafin = Column(String(50), nullable=False)
	autor = Column(String(50), nullable=False)
	estado = Column(String(50), nullable=False)
	fecha_creacion = Column(DateTime, nullable=False)
	



class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	username = Column(String(50), nullable=False)
	password = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	

	

engine = create_engine('postgresql://co:ASD123qwe@localhost/dbformulariosco')
Base.metadata.create_all(engine)
