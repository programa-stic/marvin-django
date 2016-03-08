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


import settings
import os

root_apk_dir = settings.root_apk_dir

def store_apk(rawfile, package_name, md5):
	prefix1 = md5[0:2]
	prefix2 = md5[2:4]
	filepath = root_apk_dir + prefix1 + '/' + prefix2 + '/'
	if os.path.exists(filepath) == False:
		firstdir = root_apk_dir + '/' + prefix1
		if os.path.exists(firstdir) == False:
			os.mkdir(firstdir)
		os.mkdir(firstdir + '/' + prefix2 )
	full_path = filepath + package_name + '.apk'
	fd = open(full_path,'w')
	fd.write(rawfile)
	fd.close()
	return full_path

def get_filepath(package_name, md5):
	prefix1 = md5[0:2]
	prefix2 = md5[2:4]
	dirpath = root_apk_dir + prefix1 + '/' + prefix2 + '/'
	filepath = dirpath + package_name + '.apk'
	if os.path.exists(dirpath) == False:
		raise Exception ("El directorio no existe")
	else:
		if os.path.exists(filepath):
			return filepath
		else: 
			raise Exception ("El archivo no existe, si existiera se llamaria " + filepath)

def retrieve_apk(package_name, md5):
	filepath = get_filepath(package_name, md5)
	fd = open(filepath, 'r')
	rawfile = fd.read()
	fd.close()
	return rawfile
