# Copyright (c) 2015, Fundacion Dr. Manuel Sadosky
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import settings
sys.path.insert(0, settings.vuln_analysis_dir)
sys.path.insert(0, settings.vuln_analysis_dir+'/androguard')
from androguard.core.bytecodes import apk
from androguard.misc import AnalyzeAPK
from models import *
from django.utils.encoding import smart_text
import simplejson
#import md5
#import sha
from hashlib import sha1, md5
import classifier_interface_file
import os
from apk_storage import *
from git_interface import gitlab_upload_app
import MarvinStaticAnalyzer
import threading
import logging
import constants

import traceback
from functools import wraps
from multiprocessing import Process, Queue

def processify(func):
    '''Decorator to run a function as a process.
    Be sure that every argument and the return value
    is *pickable*.
    The created process is joined, so the code does not
    run in parallel.
    '''

    def process_func(q, *args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception:
            ex_type, ex_value, tb = sys.exc_info()
            error = ex_type, ex_value, ''.join(traceback.format_tb(tb))
            ret = None
        else:
            error = None

        q.put((ret, error))

    # register original function with different name
    # in sys.modules so it is pickable
    process_func.__name__ = func.__name__ + 'processify_func'
    setattr(sys.modules[__name__], process_func.__name__, process_func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        q = Queue()
        p = Process(target=process_func, args=[q] + list(args), kwargs=kwargs)
        p.start()
        p.join()
        ret, error = q.get()

        if error:
            ex_type, ex_value, tb_str = error
            message = '%s (in subprocess)\n%s' % (ex_value.message, tb_str)
            raise ex_type(message)

        return ret
    return wrapper


@processify
def test_function():
    return os.getpid()


@processify
def test_exception():
    raise RuntimeError('xyz')


def test():
    print os.getpid()
    print test_function()
    test_exception()

if __name__ == '__main__':
    test()




# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': '/tmp/packageinfo.debug.log',
#         },
#     },
#     'loggers': {
#         'packageinfo': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }
#logger = logging.getLogger("packageinfo")
logging.basicConfig(filename="/tmp/packageinfo.info.log", level=logging.INFO)


perms_list_file = settings.perms_list_file 
model_file = settings.model_file          

def data_for_storage(rawfile):
	md5hash = md5(rawfile).hexdigest()
	try:
		myApk = apk.APK(rawfile, raw=True)
		package_name = myApk.package_name
		return (package_name, md5hash)
	except Exception as poof:
		return (repr(poof), None)

def process_package(myfile, app_md):
	t = threading.Thread (target=process_package_worker, args=(myfile, app_md))
	#threads = list()
	#threads.append(t)
	t.start()
	return "Nothing to see yet, move along"

def find_packages(myApp):
	myFileContents = map (lambda element :element.file_contents, myApp.sourcefile_set.all())
	myPackageLines = map (lambda file:
							filter (lambda text: 
								text.startswith("package"), 
								file.split(";")), 
							myFileContents)
	myPackageLines = filter (lambda list: len(list)>0, myPackageLines)
	myPackages = set(map (lambda text: text[0].split(" ")[1], myPackageLines))
	return myPackages

@processify
def process_package_worker(myfile, app_md):
	logging.info ("Entrando a process_package")
	rawfile = myfile.read()
	try:
		logging.info ("Extrayendo APK")
		(myPackage, d, dx) = AnalyzeAPK(rawfile, raw=True, decompiler="dad")
		logging.info ("APK extraido")
	except Exception as poof:
		logging.error ("Exception reading APK: " + repr (poof))
		return "Excepcion leyendo APK: " + repr (poof)
	sources   = {}
	# try:	
	# 	map (lambda cd: sources.update({cd.get_name():cd.get_source()}), d.get_classes())
	# 	print "APK decompilado"
	# except Exception as poof:
	# 	print "Exception decompiling APK: " + repr (poof)

	if myPackage.is_valid_APK():
		#misc_info = compile_misc_info(myPackage)
		package_name = myPackage.get_package()
		version 	 = myPackage.get_androidversion_name()
		qs = App.objects.filter(package_name = package_name, version = version)
		logging.info ("Busco el objeto en la base: encuentro :"+ package_name +" "+ version +" "+ str(len(qs)))
		if len(qs)>0:
			logging.error ("El objeto ya existe en la base")
			return "El objeto ya existe en la base"
		else:
			if app_md != None:
                                app_name= app_md.docV2.title
                        else:
                                app_name = get_app_name(myPackage, d)
			app = App(package_name = myPackage.get_package(),
					  version = myPackage.get_androidversion_name(),
					  app_name = app_name,
					  md5 = md5(rawfile).hexdigest(),
					  sha1 = sha1(rawfile).hexdigest(),
					  bayesConfidence = 0.000)
			app.save()
			store_apk(rawfile, app.package_name, app.md5)
			del rawfile
			if app_md != None:
				metadata = App_metadata(app_name= app_md.docV2.title,
									version_string = app_md.docV2.details.appDetails.versionString,
									author = app_md.docV2.creator,
									date_upload = app_md.docV2.details.appDetails.uploadDate,
									description = app_md.docV2.descriptionHtml,
									app = app)
				metadata.save()
			#store_apk(rawfile, app.package_name, app.md5)
			#print "Decompilando clases"
			android_manifest  = myPackage.get_android_manifest_xml().toxml()
			overrides = {"AndroidManifest.xml": android_manifest}
			#t = threading.Thread (target=save_sources_worker, args=(d, app, overrides))
			save_sources_worker(d, app, overrides)
			#threads = list()
			#threads.append(t)
			#t.start()
			permissions = myPackage.get_details_permissions()
			add_permissions(permissions, app) 

			activities = myPackage.get_activities()
			for act_name in activities:
				django_act = Activity (name = act_name, 
									  app = app)
				django_act.save()

			services = myPackage.get_services()
			for serv_name in services:
				django_srv = Service (name = serv_name, 
									  app = app)
				django_srv.save()

			providers = myPackage.get_providers()
			for prov_name in providers:
				django_prov = Provider (name = prov_name, 
									  app = app)
				django_prov.save()

			receivers = myPackage.get_receivers()
			for recv_name in receivers:
				django_recv = Receiver (name = recv_name, 
									  app = app)
				django_recv.save()

			# Me estaba subiendo los fuentes al repo antes de terminar de cargarlos
			# en la DB. Lo pase al thread que los carga en la DB.
			#gitlab_upload_app(app.package_name, app.version)
			logging.info ("Entrando a analisis bayesiano")
			bayes_analysis(app)
			logging.info ("Fin analisis bayesiano")
			logging.info( "Entrando a chequeo de vulnerabilidades")
			#t = threading.Thread (target=vuln_analysis, args=(app, myPackage, d, dx))
			vuln_analysis(app, myPackage, d, dx)
			#threads = list()
			#threads.append(t)
			#t.start()
			return app
	else:
		logging.error ("Error: APK invalido")
		return "Error: APK invalido"

def save_sources_worker(d, app, overrides):
	logging.info ("Decompilando clases")
	for javaclass in d.get_classes():
		try:
		#	print "Decompilando clase " + javaclass.get_name()
			source = repr(javaclass.get_source())
		except Exception as poof:
			logging.info ("Java class "+ javaclass.get_name() + "could not be decompiled: \n" + repr(poof))
			source = "Class could not be decompiled"
		#sources.update({javaclass.get_name():source})
		name = javaclass.get_name()[1:len(javaclass.get_name())-1]
		sourcefile = Sourcefile (file_name = name, 
									 file_contents= source[1:len(source)-1],
									 app = app)
		try:
			sourcefile.save()
		except Exception as poof:
			logging.error ("Error grabando archivo fuente: "+repr(poof))
	#gitlab_upload_app(app.package_name, app.version)
	gitlab_upload_app(app, overrides)
	app.sourcesUploaded = True
	app.save()
	packages = find_packages(app)
	for package in packages:
		existing = len(Java_package.objects.filter(package_name=package))
		if existing == 0:
			newPackage = Java_package(package_name = package)
			newPackage.save()
			newPackage.app.add(app)
			newPackage.save()
		else:
			myPackage = Java_package.objects.get(package_name=package)
			myPackage.app.add(app)
	logging.info ("Clases decompiladas")

def bayes_analysis(app):
	perms = map (lambda permission:permission.name, app.permission_set.all())
	classifier_report = classifier_interface_file.evaluate_apk(perms, perms_list_file, model_file)
	app.bayesResult = classifier_report[0]
	app.bayesConfidence = classifier_report[1]
	app.status = "BAYES_CHECKED"
	app.save()

def vuln_analysis_retry(app):
		t = threading.Thread (target=vuln_analysis_retry_worker, args=(app,))
		#threads = list()
		#threads.append(t)
		print "Empezando el thread"
		t.start()
		#t.join()
		return "Gracias vuelva prontos"

@processify
def vuln_analysis_retry_worker(app):
	print "entrando a retry_worker"
	try:
		#print "Consiguiendo filename, package_name:" + app.package_name
		filename = get_filepath(app.package_name, app.md5)
		#print "filename:"+filename
		(myPackage, d, dx) = AnalyzeAPK(filename)
		#print "Datos recuperados"
		vuln_analysis(app, myPackage, d, dx)
	except Exception as poof:
		#print "Error en retry: " + repr(poof)
		logging.error ("Exception en analisis de vulnerabilidades: " + repr (poof))


@processify
def decompile(app):
	filename = get_filepath(app.package_name, app.md5)
	(myPackage, d, dx) = AnalyzeAPK(filename)
	android_manifest  = myPackage.get_android_manifest_xml().toxml()
	overrides = {"AndroidManifest.xml": android_manifest}
	save_sources_worker(d, app, overrides)

def vuln_analysis(app, apk, d, dx):
    print "Entrando a vuln_analysis"
    prefix1 = app.md5[0:2]
    prefix2 = app.md5[2:4]
    dir_path = settings.root_apk_dir + '/' + prefix1 + '/' + prefix2 + '/'
    file_path = dir_path + app.package_name + '.apk'
    my_path = os.getcwd()
    os.chdir(settings.vuln_analysis_dir)
    vuln_report = {}
    app.status = "Checking Vulns"
    app.save()
    try:
        vuln_report = MarvinStaticAnalyzer.analyze_vulnerabilities(file_path, apk, d, dx)
    except Exception as poof:
        logging.error ("Error analyzing vulns: " + repr(poof))
        vuln_report = {"Error in analysis": [{'description':repr(poof)}]}
    os.chdir(my_path)
    #print vuln_report
    update_fields_vr(app, vuln_report)
    app.status = "Vulns checked"
    app.save()
    logging.info("Fin chequeo de vulnerabilidades")
    #return vuln_report

def update_fields_vr(app, vuln_report):
	for field in vuln_report.keys():
		for instance in vuln_report[field]:
			report = VulnerabilityResult(name = field,
									 	 description = instance['description'],
									 	 confidence = instance['confidence'],
									 	 dynamicTest = instance['dynamic_test'],
									 	 dynamic_test_params = instance['dynamic_test_params'],
									 	 app = app)
			#if report.name in constants.STATIC_VULN_TYPES:
			#	report.severity = constants.SEVERITY_PRIORITIES[constants.STATIC_VULN_TYPES[report.name]]
			#if report.name in constants.DYNAMIC_VULN_TYPES:
			#	report.severity = constants.SEVERITY_PRIORITIES[constants.DYNAMIC_VULN_TYPES[report.name]]
			report.severity = instance['severity']
			if 'reference_class' in instance:
				report.vuln_class = instance['reference_class']
			if 'reference_method' in instance:
				report.vuln_method = instance['reference_method']
			if report.confidence is None:
				report.confidence = 1
			if report.dynamicTest is None:
				report.dynamicTest = False
			report.save()
			if instance['dynamic_test'] :
				dynamicTestResult = DynamicTestResults(name = '' ,status = 'UNKNOWN' ,count = 0 ,description = '' ,vuln = report) 
				dynamicTestResult.save()


def add_permissions(permissions, app):
	for perm_name in permissions.keys():
		#print perm_name
		res = Permission.objects.search.query('match', name = perm_name)
		if len(res)==0:
			django_perm = Permission (name = perm_name, 
									  perm_description = permissions[perm_name][1],
									  perm_danger = permissions[perm_name][0])
			django_perm.save()
		else:
			django_perm = res[0]
		django_perm.app.add(app)

def get_app_name(a, d):
        try:
                app_name = a.xml['AndroidManifest.xml'].getElementsByTagName('application').pop().attributes['android:label'].nodeValue
        except Exception as poof:
                app_name = 'Error:' + repr(poof)
        if app_name[0] == '@':
                package_name = a.package
                class_name = "L"+package_name.replace('.','/')+"/R$string;"
                my_R_strings = d.get_class(class_name)
                if my_R_strings == None:
                        return package_name
                else:
                        res = a.get_android_resources()
                        for element in my_R_strings.get_fields():
                                elem_offset = format (element.init_value.get_value(),"03X")
                                if elem_offset == app_name[1:]:
                                        resource_name = element.get_name()
                                        app_name = res.get_string(package_name, resource_name)[1]
        return app_name

def reset_error(vuln):
	myVuln = VulnerabilityResult.objects.get(pk=vuln)
	myDr   = myVuln.dynamictestresults_set.first()
	if myDr.status == "ERROR":
		myDr.status = "UNKNOWN"
		myDr.description = ""
		myDr.save()

# 		classifier_report = classifier_interface_file.evaluate_apk(permissions, perms_list_file, model_file)
# 		marvin_es.store_cr(package_name, classifier_report)

##################### Functions for queue processing #############

@processify
def basic_analysis(rawfile, app):
	logging.info ("Entrando a basic_analysis")
	try:
		logging.info ("Extrayendo APK")
		(myPackage, d, dx) = AnalyzeAPK(rawfile, raw=True, decompiler="dad")
		logging.info ("APK extraido")
	except Exception as poof:
		logging.error ("Exception reading APK: " + repr (poof))
		return "Excepcion leyendo APK: " + repr (poof)
	sources   = {}
	# try:	
	# 	map (lambda cd: sources.update({cd.get_name():cd.get_source()}), d.get_classes())
	# 	print "APK decompilado"
	# except Exception as poof:
	# 	print "Exception decompiling APK: " + repr (poof)

	if myPackage.is_valid_APK():
		android_manifest  = myPackage.get_android_manifest_xml().toxml()
		overrides = {"AndroidManifest.xml": android_manifest}
		save_sources_worker(d, app, overrides)
		permissions = myPackage.get_details_permissions()
		add_permissions(permissions, app) 

		activities = myPackage.get_activities()
		for act_name in activities:
			django_act = Activity (name = act_name, 
								  app = app)
			django_act.save()

		services = myPackage.get_services()
		for serv_name in services:
			django_srv = Service (name = serv_name, 
								  app = app)
			django_srv.save()

		providers = myPackage.get_providers()
		for prov_name in providers:
			django_prov = Provider (name = prov_name, 
								  app = app)
			django_prov.save()

		receivers = myPackage.get_receivers()
		for recv_name in receivers:
			django_recv = Receiver (name = recv_name, 
								  app = app)
			django_recv.save()

		logging.info ("Entrando a analisis bayesiano")
		bayes_analysis(app)
		logging.info ("Fin analisis bayesiano")
