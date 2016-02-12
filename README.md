# MARVIN #

Marvin es un sistema que analiza aplicaciones de Android en busca de vulnerabilidades y permite realizar un seguimiento de las mismas a lo largo de su historial de versiones.

* Versión:0.8

### Instalación  ###

El script `setup.sh` ejecuta las acciones necesarias para instalar Marvin en una máquina Ubuntu 14.04 o superior. Marvin utiliza varios programas externos, a saber MySQL, ElasticSearch y GitLab; la configuración para acceder a los mismos es en `marvin-django/marvin/settings.py` para Elasticsearch y MySql, y en `marvin/django/frontpage/settings.py` para GitLab. ElasticSearch y MySQL los instala el script, pero la instalación de GitLab es aparte. Se recomienda editar estos archivos antes de correr `Instalacion.sh`

`frontpage/settings.py:` 
======================
	 vuln_analysis_dir = ubicación del Apk Vulnerability Finder  (apunta a la ubicación por defecto)  
	 perms_list_file = archivo que contiene la lista de permisos para la interfaz con Weka  (apunta a la ubicación por defecto)  
	 model_file = Modelo bayesiano para Weka  (apunta a la ubicación por defecto)  
	 root_apk_dir = Directorio donde se almacenan los Apk. Debería existir. (esto puede ser un directorio externo a donde corre Marvin, montado por NFS)  
	 root_git_dir = Directorio donde se almacenan los repositorios git locales. Debería existir. (esto puede ser un directorio externo a donde corre Marvin, montado por NFS)  
	 gitlab_url = URL del Gitlab  
	 gitlab_token = Token del usuario marvin para Gitlab  
	 marvin_git_passwd = Contraseña del usuario marvin en Gitlab  
  
`marvin/settings.py` (lo que habría que editar)
-----------------------------------------------
	 SECRET_KEY : No es seguro utilizar la que hay en el repositorio, es mejor crear una aplicación cualquiera con el Django y copiarse ese SECRET_KEY.

	 BUNGIESEARCH = {  
                	'URLS': ['localhost'], # Dirección del servidor de ElasticSearch, sin http://  
                	'INDICES': {'apps2': 'frontpage.myindices'}, # De acá en adelante queda como está  
                	#'ALIASES': {'bsearch': 'marvin.search_aliases'},  
                	'SIGNALS': {'BUFFER_SIZE': 1},  
                	'TIMEOUT': 5  
                	}

	 DATABASES = {
    		'default': {
         		'ENGINE': 'django.db.backends.mysql',
         		'NAME': 'marvin',  #Nombre de la base de datos a usar. Puede quedar como está
         		'USER': 'marvin',  #Nombre del usuario de la base. Puede quedar como está
         		'PASSWORD': '********',  #Contraseña del usuario en la base. Favor de elegirle una. Ver también marvin/init_database.sql
         		'HOST': 'localhost',     #Dirección IP del servidor MySQL, en caso de ya tener uno instalado se puede usar (pero ver marvin/init_database.sql e Instalacion.sh)
         		'PORT': '3306'
    		}
	}


El script `setup.h` instala una cantidad de paquetes, por lo que al invocar a sudo habrá que introducir la contraseña de administrador. También al instalar MySql 
pedirá una contraseña para el usuario 'root', y se deberá ingresar esa contraseña cuando más tarde se creen las bases de datos de la aplicación.

### Iniciando Marvin ###

Marvin se inicia con el comando 

	$ python manage.py runserver 0.0.0.0:[port]

en el directorio `marvin-django/marvin`. Una vez corriendo, queda configurar la cuenta de Google Play que va a ser usada por Marvin: 
entrar con el navegador a la url `localhost:[port]/admin` e ingresar a la sección "Google Play". Ahí se deben ingresar los datos de una cuenta de Google que esté ligada a un teléfono Android: lo más conveniente es crear una cuenta y usar android-checkin para registrarla como ligada a un teléfono. 


Android-checkin: `https://github.com/nviennot/android-checkin`


### Dependencias ###
	  Django 1.7
	  apk-vulnerability-finder
	  django-googleplay-api 
	  androguard
	  elasticsearch
	  bungiesearch 1.1.0 o superior
	  mysql o postgres
	  una cuenta de Gitlab con mucho espacio
	  python-gitlab 
	  pygit2 0.23.1 o superior
	  Weka
	  simplejson
	  arff
	  openjdk 


### Información de contacto ###

  * Juan Heguiabehere, jheguia@fundacionsadosky.org.ar
  * Joaquín Rinaudo, jrinaudo@fundacionsadosky.org.ar
