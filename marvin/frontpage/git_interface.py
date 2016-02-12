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

# git-interface.py


import pygit2
from gitlab import Gitlab
from apk_storage import get_filepath
from settings import root_git_dir, marvin_git_passwd, gitlab_url, gitlab_token
from frontpage.models import App, VulnerabilityResult, Permission, Sourcefile
from hashlib import md5
import sys
import os
from shutil import rmtree
from zipfile import ZipFile
import logging 



#from django.templates.defaultfilters import slugify
logging.basicConfig(filename="/tmp/marvin.info.log", level=logging.WARN)
#logger = logging.getLogger("git_interface")

def repo_name(package_name):
	md5hash_pn = md5(package_name).hexdigest()
	first_pref = md5hash_pn[0:2]
	second_pref = md5hash_pn[2:4]
	workingdir = root_git_dir+"/"+first_pref+"/"+second_pref+"/" + package_name
	return workingdir

def crear_repo(package_name):
	md5hash_pn = md5(package_name).hexdigest()
	first_pref = md5hash_pn[0:2]
	second_pref = md5hash_pn[2:4]
	workingdir = root_git_dir+"/"+first_pref+"/"+second_pref+"/" + package_name
	if not(os.access(root_git_dir+"/"+first_pref, os.F_OK)):
		os.mkdir(root_git_dir+"/"+first_pref)
		os.mkdir(root_git_dir+"/"+first_pref+"/"+second_pref)
	elif not(os.access(root_git_dir+"/"+first_pref+"/"+second_pref, os.F_OK)):
		os.mkdir(root_git_dir+"/"+first_pref+"/"+second_pref)
	repo = pygit2.init_repository(workingdir)
	dashed_package_name=package_name.replace('.','-').lower()
	myRemote = repo.remotes.create(package_name, gitlab_url+'/marvin/'+dashed_package_name+'.git')
	gl = Gitlab (gitlab_url, gitlab_token)
	gl.auth()
	p = gl.Project({'name': package_name, 'public':True})
	p.save()
	return repo

def borrar_repo(package_name):
	filepath = repo_name(package_name)
	gl = Gitlab (gitlab_url, gitlab_token)
	gl.auth()
	# Project search no anda bien, da error si pongo el package_name entero
	# Si pido todos seria un delirio para la cantidad de proyectos que queremos manejar
	# asi que buscamos por la ultima palabra del nombre (esperando que no sea Android) 
	# e iteramos sobre los resultados hasta encontrar package_name
	split_name = package_name.split('.')

	searchterm = split_name[len(split_name)-1]
	projlist = gl.search_projects(searchterm)
	for project in projlist:
		if project.name == package_name:
			break
	else:
		project = None
	if project == None:
		raise Exception("El proyecto no existe en GitLab")
	else:
		project.delete()
	rmtree(filepath)



def stage_apk(app, overrides):
	myRepo = pygit2.Repository(repo_name(app.package_name))
	master = myRepo.lookup_branch("master")
#	if master == None:
		#myTreeGen = myRepo.TreeBuilder()
#	else:
#		lastcommit = myRepo.get(master.target)
#		lastTree = lastcommit.tree.oid
		#myTreeGen = myRepo.TreeBuilder(lastTree)
	myIndex = myRepo.index
	for sourcefile in app.sourcefile_set.all():
		logging.info( "Storing "+sourcefile.file_name+"\n")
		src = (sourcefile.file_contents).encode('ascii','replace').replace("\\n", "\n")
		contents = myRepo.create_blob(src)
		myIndex.add(pygit2.IndexEntry(sourcefile.file_name+".java", contents, pygit2.GIT_FILEMODE_BLOB))
	logging.info( "Listo el codigo fuente")
	add_other_files(app, myRepo, myIndex, overrides)
		#myTreeGen.insert(sourcefile.file_name, contents, pygit2.GIT_FILEMODE_BLOB)
	#myTree = myTreeGen.write()
	myTree    = myIndex.write_tree()
	version   = app.version
	author    = pygit2.Signature("Alice Author", "alice@authors.tld")
	committer = pygit2.Signature("Alice Author", "alice@authors.tld")
	if master == None:
		myRepo.create_commit('refs/heads/master', author, committer, 
							  version,
							  myTree,
							  [])
	else:
		myRepo.create_commit('refs/heads/master', author, committer, 
							  version,
							  myTree,
							  [master.target])
	myRepo.create_branch(version, myRepo.head.get_object())
	myRemote = myRepo.remotes[0]
	#myRemote.credentials = pygit2.UserPass("marvin",marvin_git_passwd)
	credentials = pygit2.UserPass("marvin",marvin_git_passwd)
	callbacks=pygit2.RemoteCallbacks(credentials=credentials)
	myRemote.push(["refs/heads/master"],callbacks=callbacks)
	myRemote.push(["refs/heads/"+version],callbacks=callbacks)



def add_other_files(app, myRepo, myIndex, overrides):
	logging.info("Agregando otros archivos, overrides: "+ repr(overrides.keys()))
	file_name = get_filepath(app.package_name, app.md5)
	zipfile = ZipFile (file_name, 'r')
	for filename in zipfile.namelist():
		if filename in overrides:
			logging.info ("Storing "+ filename +" from overrides\n")
			myBytes = overrides[filename]
		else:
			myBytes = zipfile.read(filename)
			logging.info ("Storing "+filename+"from zip")
		contents = myRepo.create_blob(myBytes)
		myIndex.add(pygit2.IndexEntry(filename, contents, pygit2.GIT_FILEMODE_BLOB))
	zipfile.close()




def gitlab_upload_app(myApp, overrides):
	#myApp = App.objects.get(package_name=package_name, version=version)
	repo_dir = repo_name(myApp.package_name)
	if os.access(repo_dir, os.F_OK) == False:
		crear_repo(myApp.package_name)
	stage_apk(myApp, overrides)
