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

#!/usr/bin/python
# encoding: utf-8

# EvaluarAPK: Este programa toma un archivo, extrae la informaci0n de permisos, los almacena en formato ARFF,
# llama al programa WEKA para que evalue si el APK es malware o no, y reporta True si es malware o False si no.
# Necesita:
#   Nombre del APK
#   Lista de permisos a incluir en el archivo ARFF
#   
# androguard.py debe estar accesible para que funcione, claro

#Cambiar directorios no funciona cambiando el directorio, salvo que '.' este en el PYTHONPATH. 
# Para eso, mejor poner el path a androguard mismo dentro del PYTHONPATH, 
# que es lo que finalmente se hace
# agpath = '/home/jheguia/Proyectos/android-tools/androguard-1.9'

import arff
import simplejson
import subprocess
import os
import tempfile

#curpath = os.getcwd()
#os.chdir(agpath)
from androguard.core.bytecodes import apk
#os.chdir(curpath)

# def get_permissions(filename):
# 	package = apk.APK(filename)
# 	return package.get_permissions()

def perm_bitmap(perm_list, app_perms):
	return map ( lambda p: p in app_perms, perm_list)

def evaluate_apk(permissions, perm_file, model_file):
	fd = open(perm_file,'r')
	perm_list = simplejson.load(fd)
	fd.close()
#	permissions = get_permissions(filename)

	bitmap = perm_bitmap(perm_list, permissions)+[True]

	temp=tempfile.mkstemp(suffix='.arff')
	arff.dump(temp[1],[bitmap], names=perm_list+['Class'])

	output = subprocess.check_output(['java','weka.classifiers.bayes.NaiveBayesUpdateable','-p','0','-T',temp[1],'-l',model_file])	
	#os.remove(temp[1])
	virus =  output.split()[13]=='1:True'
	assurance = output.split()[14]
	if assurance == '+':
		assurance = output.split()[15]
	return (virus, str(assurance))


def update_model(new_instances, old_model, new_model):
	subprocess.call(['java','weka.classifiers.bayes.NaiveBayesUpdateable', '-l', old_model, '-d',new_model, '-T', new_instances])
	if os.path.exists(new_model):
		return True


