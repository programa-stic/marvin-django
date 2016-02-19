# README #

Marvin is a system that analyzes Android applications in search of vulnerabilities and allows 
tracking of an app through its version history.

It is composed of 4 subsystems:

* [Marvin-django](https://github.com/programa-stic/marvin-django): The web application frontend for use and adminsitration of Marvin (this repostory). It includes a bayesian classifier that provides a probability estimation of a given Android app being malware. 
* [Marvin-static-Analyzer](https://github.com/programa-stic/Marvin-static-Analyzer): A static code analysis system that uses Androguard and Static Android Analysis Framework (SAAF). 
* [Marvin-dynamic-Analyzer](https://github.com/programa-stic/Marvin-dynamic-Analyzer): A dynamic code analysis system that uses Android x86-emulators and Open Nebula virtualization to find vulnerabilities automatically
* [Marvin-toqueton](https://github.com/programa-stic/Marvin-toqueton): An automated GUI testing tool developed to assist Marvin's dynamic code analysis.

A Marvin user's guide is provided in the [docs](https://github.com/programa-stic/marvin-django/tree/master/marvin/docs) folder of this repository.

### Installing Marvin ###

Once the repository is cloned, the script `setup.sh` executes the actions needed to install Marvin in a PC running Ubuntu Linux 14.04 or higher. 
Marvin uses several external programs, such as MySQL, Elasticsearch and Gitlab, for which configuration is needed before running `setup.sh`.
Elasticsearch and MySQL need to have their data specified in `marvin-frontend/marvin/marvin/settings.py`, and GitLab settings 
go in `marvin-frontend/marvin/frontend/settings.py`. MySQL and Elasticsearch get installed by `setup.sh`, but a running GitLab installation
will have to be provided by the user.

`frontpage/settings.py`:
-----------------------
	vuln_analysis_dir = marvin_static_analyzer installation folder (points to default path)
	perms_list_file = Permissions list for malware heuristics analysis  (default path)
	model_file = Bayesian model for malware heuristics analysis (default path)
	root_apk_dir = Path to where the APK files will be stored. Should exist.
	root_git_dir = Path to where local Git repositories will be stored. Should exist.
	gitlab_url = Self explanatory
	gitlab_token = There should be a "marvin" user in GitLab. This is where you store his token.
	marvin_git_passwd = The password for user "marvin" in GitLab



`marvin/settings.py` (the parts you should edit)
-----------------------------------------------
	SECRET_KEY : It's not safe to use the repositories', you should generate one (perhaps creating an empty app with Django and copying its SK)
	
	BUNGIESEARCH = {
                	'URLS': ['localhost'], # ElasticSearch IP address, (no http:// prefix)
                	'INDICES': {'apps2': 'frontpage.myindices'}, # From here on, no changes
                	#'ALIASES': {'bsearch': 'marvin.search_aliases'},
                	'SIGNALS': {'BUFFER_SIZE': 1},
                	'TIMEOUT': 5
                	}

	DATABASES = {
    		'default': {
         		'ENGINE': 'django.db.backends.mysql',
         		'NAME': 'marvin',  #Name of the database. Can be left as is (otherwise you must change marvin/init_database.sql accordingly)
         		'USER': 'marvin',  #Name of the database user. Can be left as is, otherwise as above
         		'PASSWORD': '********',  # Database user password. Please choose one and update init_database.sql with it
         		'HOST': 'localhost',     # MySQL server IP address. Can be left as is, otherwise see init_database.sql
         		'PORT': '3306'           # MySQL server port. Can be left as is, yadda yadda
    			}
		}





The `setup.sh` script installs a number of packages, for which it invokes sudo and will ask for the user's password. 
Also, since it installs MySQL, it will ask for the creation of a MySQL administrator user, and will later want this 
administrator's password for creating the Marvin database. Finally, it will create an administrator account for Django,
asking for its credentials.

Marvin starts with the command

	$ python manage.py runserver 0.0.0.0:[port]

while on  `marvin-frontend/marvin`. Once running, there is one last task: configuring the Google account that will be used to 
access the Play Store. Browse to `localhost:[port]/admin` (you should give it the credentials it last asked for)
and enter "Google Play". There you need to enter the details of a Google account that should be "checked in" in the Play Store:
there is an app that does the checkin at 
Android-checkin: `https://github.com/nviennot/android-checkin`


### Dependencies ###
  	 Django 1.7
  	 apk-vulnerability-finder
 	 django-googleplay-api 
  	 androguard
  	 elasticsearch
  	 bungiesearch 1.1.0 or later
  	 mysql or postgres
  	 a GitLab account with lots of space
  	 python-gitlab 
  	 pygit2 0.23.1 or later
  	 Weka
  	 simplejson
  	 arff
  	 openjdk 


### Credits ###
  * Juan Heguiabehere ([@jheguia](https://www.twitter.com/jheguia))

### Who do I talk to? ###
 * Send an email to stic at fundacionsadosky.org.ar

