# MARVIN #

Marvin es un sistema que analiza aplicaciones de Android en busca de vulnerabilidades y permite realizar un seguimiento de las mismas a lo largo de su historial de versiones.

Está compuesto de 4 subsistemas:

* [Marvin-django](https://github.com/programa-stic/marvin-django): Una aplicación web que sirve de entrada para el uso y administración del sistema (este repositorio). Incluye un clasificador bayesiano que estima la probabilidad de que una app para Android sea malware.
* [Marvin-static-Analyzer](https://github.com/programa-stic/Marvin-static-Analyzer): Un sistema de análisis estático de código que usa Androguard y Static Android Analysis Framework (SAAF) para detectar vulnerabilidades.
* [Marvin-dynamic-Analyzer](https://github.com/programa-stic/Marvin-dynamic-Analyzer): Un sistema de análisis dinámico de código que usa emuladores de Android para x86 y el entorno de virtualización de OpenNebula para detectar vulnerabilidades automáticamente.
* [Marvin-toqueton](https://github.com/programa-stic/Marvin-toqueton): Una herramienta para pruebas automatizadas de GUIs desarrollada para asistir en la búsqueda de vulnerabildiades al sistema de análisis dinámico de código de Marvin. 

Hay una guía para el usuario de Marvin en la carpetas [docs](https://github.com/programa-stic/marvin-django/tree/master/marvin/docs) de este repositorio.


### Instalación  ###

El script `setup.sh` ejecuta las acciones necesarias para instalar Marvin en una máquina Ubuntu 14.04 o superior. Marvin utiliza varios programas externos, a saber MySQL, ElasticSearch y GitLab; la configuración para acceder a los mismos es en `marvin-django/marvin/settings.py` para Elasticsearch y MySql, y en `marvin/django/frontpage/settings.py` para GitLab. ElasticSearch y MySQL los instala el script, pero la instalación de GitLab es aparte. Se recomienda editar estos archivos antes de correr `Instalacion.sh`

`frontpage/settings.py:` 
----------------------
	 vuln_analysis_dir = ubicación del Apk Vulnerability Finder  (apunta a la ubicación por defecto)  
	 perms_list_file = archivo que contiene la lista de permisos para la interfaz con Weka  (apunta a la ubicación por defecto)  
	 model_file = Modelo bayesiano para Weka  (apunta a la ubicación por defecto)  
	 root_apk_dir = Directorio donde se almacenan los Apk. Debería existir. (esto puede ser un directorio externo a donde corre Marvin, montado por NFS)  
	 root_git_dir = Directorio donde se almacenan los repositorios git locales. Debería existir. (esto puede ser un directorio externo a donde corre Marvin, montado por NFS)  
	 gitlab_url = URL del Gitlab  
	 gitlab_token = Token del usuario marvin para Gitlab  
	 marvin_git_passwd = Contraseña del usuario marvin en Gitlab

	 gp_server = googleplay.GooglePlayAPI(	<language>,
	 										<timezone>,
	 										<device_id>)
	 	languaje 	= Lenguaje de la cuenta de google ('it_IT', 'es_AR', etc)
	 	timezone 	= Zona horaria del dispositivo
	 	device_id 	= Nombre del dispositivo que se conecta. Todos los disponibles se pueden ver en /marvin/gpApi/device.properties
  
  
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


El script `setup.h` instala una cantidad de paquetes, por lo que al invocar a sudo habrá que introducir la contraseña de administrador. También al instalar MySql pedirá una contraseña para el usuario 'root', y se deberá ingresar esa contraseña cuando más tarde se creen las bases de datos de la aplicación.

### Iniciando Marvin ###

Marvin se inicia con el comando 

	$ python manage.py runserver 0.0.0.0:[port]

en el directorio `marvin-django/marvin`.

### Agentes ###
El proyecto cuenta con 3 agentes que son los encargados de interactuar la cola de mensajes que genera Marvin. El codigo de los mismos se pude encontrar dentro del dirctorio "/agent".
Para que marvin funcione correctamente, es necesario inicializar los agentes, lo cual se puede hacer desde el script "start-agents", o corriendo cada uno individualmente con el comando python "marvin_nombre_del_agente_agent.py"
La opcion "Resetar Agentes" dentro del menu, permite vaciar la cola de mensajes en caso de que sea necesario. Que Llos agentes no esten activos no causa ningun inconveniente  


### Dependencias ###
	  Django 1.7
	  pip
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

### Créditos ###
  * Juan Heguiabehere ([@jheguia](https://www.twitter.com/jheguia))

### Contacto ###
* Mandar un correo a stic en el dominio fundacionsadosky.org.ar
