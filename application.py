from flask import Flask, g, render_template, jsonify, url_for, flash, redirect
from flask import request, redirect, make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from database_setup import Base, SISTEMASIMPRESORAS, RRHHDIAESTUDIO, COMERCIAL, OPERACIONES, RRHHVACACIONES, User
import random
import string
import json
import datetime

app = Flask(__name__)

#1	BASE DE DATOS 

#-------------------------------------------------------------------------------------------------
#1.1 Conectar a base de datos y crear base de datos session
#-------------------------------------------------------------------------------------------------
engine = create_engine('postgresql://co:ASD123qwe@localhost/dbformulariosco')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
#-------------------------------------------------------------------------------------------------

#1	INICIO DE PAGINA WEB: FORMULARIOS DM 

#-------------------------------------------------------------------------------------------------
#1.1 Inicio de sesion de usuario
#-------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('1_1_login.html')
	else:
		if request.method == 'POST':
			print ("dentro de POST login")
			user = session.query(User).filter_by(
				username = request.form['username'],
				password = request.form['password']).first()
			if not user:
				error = "Usuario no registrado"
				flash('Usuario no registrado')
				return redirect(url_for('login', error = error ) )
			else:
				print ("dentro de user")
				login_session['username'] = request.form['username']
				return redirect(url_for('RRHH_Home', username=login_session['username']))
				
		
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#1.2 Registro de usuario
#-------------------------------------------------------------------------------------------------
				
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():

	if request.method == 'GET':
		return render_template('registrar.html')
	else:
		if request.method == 'POST':
			nuevoUsuario = User(
					username = request.form['username'],
					password=request.form['password'],
					email = request.form['email']) 
			session.add(nuevoUsuario)
			session.commit()
			login_session['username'] = request.form['username']
			return redirect(url_for('login'))
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#1.3 Cerrar sesion de usuario
#-------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
		del login_session['username']
		return render_template('login.html')

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'username' not in login_session:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function
# -------------------------------------------------------------------------------------------------------	

#2	RECURSOS HUMANOS: FORMULARIOS

#-------------------------------------------------------------------------------------------------
#2.1 Home RRHH
#-------------------------------------------------------------------------------------------------
@app.route('/RRHH_Home', methods=['GET'])
def RRHH_Home():
	posts = session.query(RRHHDIAESTUDIO).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('RRHH_Home.html', posts = posts, username=username)	
	else:
		return render_template('RRHH_Home.html', posts = posts)
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#2.2 RRHH: Dia de Estudio
#-------------------------------------------------------------------------------------------------
@app.route('/RRHHAgregarDiaDeEstudio', methods=['GET', 'POST'])
def RRHHAgregarDiaDeEstudio():
	posts = session.query(RRHHDIAESTUDIO).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('RRHHAgregarDiaDeEstudio.html', posts = posts, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			rrhhdiaestudio = RRHHDIAESTUDIO(
					apellidoynombre = request.form['apellidoynombre'],
					dni = request.form['dni'],
					materia = request.form['materia'],
					fecha = request.form['fecha'],
					autor = username,
					estado = 'Abierto',
					fecha_creacion = datetime.datetime.now())
			session.add(rrhhdiaestudio)
			session.commit()
			return redirect(url_for('RRHH_Home'))
#-------------------------------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------------------------
#2.2.1 RRHH: Dia de Estudio: Eliminar Solicitud
#-------------------------------------------------------------------------------------------------		
@app.route('/rrhhdiaestudio/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarRRHHDIAESTUDIO(id):
	post = session.query(RRHHDIAESTUDIO).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and post.autor == username:
		return render_template('RRHHdiaestudio_Delete_Solicitud.html', post = post)
	else:
		if request.method == 'POST':
			session.delete(post)
			# delete blog set id=2
			session.commit()
			return redirect(url_for('RRHH_ReportesDiaDeEstudio.html'))
		else:
			return redirect(url_for('RRHHdiaestudios_Delete_Solicitud_Error'))
#-------------------------------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------------------------
#2.2.2 RRHH: Dia de Estudio: Error al Eliminar Solicitud 
#-------------------------------------------------------------------------------------------------
			
@app.route('/RRHHdiaestudio_Delete_Solicitud_Error', methods=['GET'])
def RRHHdiaestudios_Delete_Solicitud_Error():
	return render_template('RRHHdiaestudio_Delete_Solicitud_Error.html')
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#2.2.3 RRHH: Dia de Estudio: Reportes 
#-------------------------------------------------------------------------------------------------	
@app.route('/RRHH_ReportesDiaDeEstudio', methods=['GET'])
def RRHH_ReportesDiaDeEstudio():
	posts = session.query(RRHHDIAESTUDIO).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('RRHH_ReportesDiaDeEstudio.html', posts = posts, username=username)	
	else:
		return render_template('RRHH_ReportesDiaDeEstudio.html', posts = posts)

#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#2.3 RRHH: Vacaciones 
#-------------------------------------------------------------------------------------------------	
@app.route('/RRHHSolicitudVacaciones', methods=['GET', 'POST'])
def RRHHSolicitudVacaciones():
	posts = session.query(RRHHVACACIONES).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('RRHHSolicitudVacaciones.html', posts = posts, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			rrhhvacaciones = RRHHVACACIONES(
					apellidoynombre = request.form['apellidoynombre'],
					dni = request.form['dni'],
					fechainicio = request.form['fechainicio'],
					fechafin = request.form['fechafin'],
					autor = username,
					estado = 'Abierto',
					fecha_creacion = datetime.datetime.now())
			session.add(rrhhvacaciones)
			session.commit()
			return redirect(url_for('RRHH_Home'))
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#2.3.1 RRHH: Eliminar Vacaciones 
#-------------------------------------------------------------------------------------------------
@app.route('/rrhhvacaciones/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarRRHHvacaciones(id):
	post = session.query(RRHHVACACIONES).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and post.autor == username:
		return render_template('RRHHSolicitudVacaciones_Delete_Solicitud.html', post = post)
	else:
		if request.method == 'POST':
			session.delete(post)
			session.commit()
			return redirect(url_for('RRHH_Reportes_Vacaciones'))
		else:
			return redirect(url_for('RRHHSolicitudVacaciones_Delete_Solicitud_Error'))
#-------------------------------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------------------------
#2.3.2 RRHH: Vacaciones: Error al Eliminar Solicitud 
#-------------------------------------------------------------------------------------------------
@app.route('/RRHHSolicitudVacaciones_Delete_Solicitud_Error', methods=['GET'])
def RRHHSolicitudVacaciones_Delete_Solicitud_Error():
	return render_template('RRHHSolicitudVacaciones_Delete_Solicitud_Error.html')	
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#2.3.3 RRHH: Vacaciones: Reportes 
#-------------------------------------------------------------------------------------------------	
@app.route('/RRHH_Reportes_Vacaciones', methods=['GET'])
def RRHH_Reportes_Vacaciones():
	posts = session.query(RRHHVACACIONES).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('RRHH_Reportes_Vacaciones.html', posts = posts, username=username)	
	else:
		return render_template('RRHH_Reportes_Vacaciones.html', posts = posts)
# -------------------------------------------------------------------------------------------------------	

#3	COMERCIAL: FORMULARIOS
#-------------------------------------------------------------------------------------------------
#3.1 Home COMERCIAL
#-------------------------------------------------------------------------------------------------
			
@app.route('/Comercial_Home', methods=['GET'])
def Comercial_Home():
	posts = session.query(COMERCIAL).all()
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Comercial_Home.html', posts = posts, username=username)	
	else:
		return render_template('Comercial_Home.html', posts = posts)

#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#3.2 COMERCIAL: Inscripcion Actividades
#-------------------------------------------------------------------------------------------------
		
@app.route('/Comercial_Inscripcion_Actividades', methods=['GET', 'POST'])
def Comercial_Inscripcion_Actividades():
	posts = session.query(COMERCIAL).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('Comercial_Inscripcion_Actividades.html', posts = posts, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			comercial = COMERCIAL(
					apellidoynombre = request.form['apellidoynombre'],
					dni = request.form['dni'],
					correo = request.form['correo'],
					telefono = request.form['telefono'],
					evento = request.form['evento'],
					autor = username,
					estado = 'Abierto',
					fecha_creacion = datetime.datetime.now())
			session.add(comercial)
			session.commit()
			return redirect(url_for('Comercial_Reportes'))
			
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
#3.2 COMERCIAL: Inscripcion Actividades
#-------------------------------------------------------------------------------------------------
			
@app.route('/Comercial_Reportes', methods=['GET'])
def Comercial_Reportes():
	posts = session.query(COMERCIAL).all()
	
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Comercial_Reportes.html', posts = posts, username=username)	
	else:
		return render_template('Comercial_Reportes.html', posts = posts)
		
		
#-------------------------------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------------------------
#3.2.1 COMERCIAL: Inscripcion Actividades: Eliminar Inscripcion
#-------------------------------------------------------------------------------------------------		
@app.route('/comercial/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarCOMERCIAL(id):
	post = session.query(COMERCIAL).filter_by(id = id).one()
	username = login_session['username']
	if request.method == 'GET' and post.autor == username:
		return render_template('Comercial_Delete_Solicitud.html', post = post)
	else:
		if request.method == 'POST':
			session.delete(post)
			session.commit()
			return redirect(url_for('Comercial_Reportes'))
		else:
			return redirect(url_for('Comercial_Delete_Solicitud_Error'))
#-------------------------------------------------------------------------------------------------------	

#-------------------------------------------------------------------------------------------------
#3.2.2 COMERCIAL: Inscripcion Actividades: Error Eliminar Inscripcion
#-------------------------------------------------------------------------------------------------		
			
@app.route('/Comercial_Delete_Solicitud_Error', methods=['GET'])
def Comercial_Delete_Solicitud_Error():
	return render_template('Comercial_Delete_Solicitud_Error.html')	
#-------------------------------------------------------------------------------------------------------	
	




 	


# -------------------------------------------------------------------------------------------------------
			
# OPERACIONES INICIO
			
@app.route('/Operaciones_Home', methods=['GET'])
def Operaciones_Home():
	posts = session.query(OPERACIONES).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Operaciones_Home.html', posts = posts, username=username)	
	else:
		return render_template('Operaciones_Home.html', posts = posts)
		
@app.route('/Operaciones_Solicitud', methods=['GET', 'POST'])
def Operaciones_Solicitud():
	posts = session.query(OPERACIONES).all()
	if request.method == 'GET':
		username = login_session['username']
		return render_template('Operaciones_Solicitud.html', posts = posts, username=username)	
	else:
		if request.method == 'POST':
			username = login_session['username']
			operaciones = OPERACIONES(
					apellidoynombre = request.form['apellidoynombre'],
					sede = request.form['sede'],
					piso = request.form['piso'],
					inconveniente = request.form['inconveniente'],
					estado = 'Abierto',
					autor = username,
					fecha_creacion = datetime.datetime.now())
			session.add(operaciones)
			session.commit()
			return redirect(url_for('Operaciones_Reportes'))
			
@app.route('/Operaciones_Reportes', methods=['GET'])
def Operaciones_Reportes():
	posts = session.query(OPERACIONES).all()
	# select * from blog
	
	if 'username' in login_session:
		username = login_session['username']
		return render_template('Operaciones_Reportes.html', posts = posts, username=username)	
	else:
		return render_template('Operaciones_Reportes.html', posts = posts)
		
@app.route('/operaciones/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminarOPERACIONES(id):
	post = session.query(OPERACIONES).filter_by(id = id).one()
	# select * from blog where id=2
			
	username = login_session['username']
	if request.method == 'GET' and post.autor == username:
		return render_template('Operaciones_Delete_Solicitud.html', post = post)
	else:
		if request.method == 'POST':
			session.delete(post)
			# delete blog set id=2
			session.commit()
			return redirect(url_for('Operaciones_Reportes'))
		else:
			return redirect(url_for('Operaciones_Delete_Solicitud_Error'))
			
@app.route('/Operaciones_Delete_Solicitud_Error', methods=['GET'])
def Operaciones_Delete_Solicitud_Error():
	return render_template('Operaciones_Delete_Solicitud_Error.html')	
		
# OPERACIONES FIN

# --------------------------------------------------------------------------------------


@app.route('/PanelDeControl', methods=['GET'])
def PanelDeControl():
	username = login_session['username']
	if username == 'adm-mrojas':
		return render_template('PanelDeControl.html', username=login_session['username'])	
	else:
		return render_template('1_1_login.html')	

					

if __name__ == '__main__':
	app.secret_key = "secret key"
	app.debug = True
	app.run(host = '0.0.0.0', port = 8080)
