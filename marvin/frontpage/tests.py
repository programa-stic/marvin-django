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

from django.test import TestCase

# Create your tests here.
from bungiesearch import Bungiesearch
from bungiesearch.management.commands import search_index
from bungiesearch.utils import update_index
from time import sleep

from frontpage.models import App, Sourcefile, Permission, Activity, Provider, Service
from frontpage.myindices import AppIndex, SourcefileIndex, PermissionIndex, ActivityIndex, ServiceIndex, ProviderIndex


class ModelIndexTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		#Let's start by creating the index and mapping.
		#If we create an object before the index, the index
		#will be created automatically, and we want to test the command.
		#search_index.Command().run_from_argv(['pruebas', 'empty_arg', '--create'])

		myApp = App(package_name = "package com.myCompany.myApp",
		app_name = "My Wonderful App",
		version = "1.0",
		md5 = "md5sum",
		sha1 = "sha1sum" )
		myApp.save()
		myApp2 = App(package_name = "package com.myOtherCompany.myApp",
		app_name = "That thing",
		version = "1.0",
		md5 = "deme cinco",
		sha1 = "shashasha" )
		myApp2.save()
		source1 = Sourcefile(file_name="source1.java", file_contents ="sourcefile contents, viste", app=myApp)
		source2 = Sourcefile(file_name="source2.java", file_contents ="sourcefile contents 2, viste", app=myApp)
		source1.save()
		source2.save()
		perm1 = Permission (name="android.permission.0WN_PHONE", perm_description="This permission lets you pretend you're Google", perm_danger="VERY DANGEROUS")
		perm1.save()
		perm1.app.add(myApp)
		perm1.app.add(myApp2)
		perm2 = Permission(name="android.permission.CAMERA", perm_description="Allows an app to take pictures", perm_danger="It depends on where you point it")
		perm2.save()
		perm2.app.add(myApp)
		sleep(2)
	
	def test_all(self):
		self.assertEqual(len(App.objects.all()), 2)
		# print len(App.objects.all())
		pepe = App.objects.all()
		print "Lista de objetos de la base. Cantidad:" + str(len(pepe))
		for obj in pepe:
			print "Objeto:" +repr(obj)
			print "Package_name: " + obj.package_name
			print "app_name: " + obj.app_name
			print "version:" + obj.version
			print "sha1: " + obj.sha1
			print "md5: " + obj.md5

	def test_search(self):
		res = App.objects.search.query('match', package_name='com.myCompany.myApp')
		print repr(res[0])
		self.assertEqual(App.objects.search.query('match', _all='com.myCompany.myApp')[0], 
			App.objects.get(md5='md5sum'), 
			'Buscar "myCompany" no trajo solo la primera app.')

	def test_iteration(self):
		lazy_search = App.objects.search.query('match', package_name='package')
		db_items = list(App.objects.all())
		print "Len lazy_search: " + str (len(lazy_search))
		print "Len db_items: "  + str(len(db_items))
		print "       Items: "
		for item in lazy_search:
			print repr(item)
		print "       End items"
		self.assertTrue(all([result in db_items for result in lazy_search]), "Buscar 'package' en el package_name no devuelve todas las apps")
		self.assertEqual(len(lazy_search[:1]), 1, 'Get item with start=None and stop=1 did not return one item.')
		self.assertEqual(len(lazy_search[:2]), 2, 'Get item with start=None and stop=2 did not return two items.')

	def test_fk_sourcefiles(self):
		app = App.objects.get(md5="md5sum")
		sources = app.sourcefile_set.all()
		self.assertEqual(len(sources),2)

	def test_m2m_permissions(self):
		app = App.objects.get(package_name = "package com.myCompany.myApp")
		permissions = app.permission_set.all()
		self.assertEqual(len(permissions),2)
		perm = Permission.objects.get(name="android.permission.0WN_PHONE")
		apps = App.objects.filter(permission=perm)
		self.assertEqual(len(apps),2)

	@classmethod
	def tearDownClass(cls):
		search_index.Command().run_from_argv(['pruebas', 'empty_arg', '--delete', '--guilty-as-charged'])

