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

from django.db import models
from bungiesearch.managers import BungiesearchManager
# Create your models here.

class App(models.Model):
	QUEUED_STATUS = 'QUEUED'
	DOWNLOADING = 'Started'
	DOWNLOADED  = 'Complete'
	N_A			= 'N/A'
	START_STAT  = 'Started'
	END_STAT    = 'Complete'
	START_VF    = 'Started'
	END_VF      = 'Complete'
	
	
	# app_id = models.AutoField(db_index=True, blank=True)
	status = models.CharField(default = QUEUED_STATUS, max_length=20)
	DLstatus = models.CharField(default = QUEUED_STATUS, max_length=20)
	DCstatus = models.CharField(default = N_A, max_length=20)
	SAstatus = models.CharField(default = N_A, max_length=20)
	DAstatus = models.CharField(default = N_A, max_length=20)
	package_name = models.CharField(db_index=True, max_length=100)
	app_name = models.CharField(blank = True, db_index=True, max_length=100)
	version = models.CharField(blank = True, max_length=30)
	md5 = models.CharField(db_index=True, max_length=100)
	sha1 = models.CharField(db_index=True, max_length=100)
	uploaded = models.DateField(auto_now_add = True, blank=True)
	targetSDK = models.CharField(blank = True, max_length=10)
	minSDK = models.CharField(blank = True, max_length=10)
	bayesResult = models.NullBooleanField(blank=True)
	bayesConfidence = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=3)
	sourcesUploaded = models.BooleanField(default=False, blank=True)

	objects = BungiesearchManager()

	def __unicode__(self):
		return self.package_name + ' ' + self.version
	
	class Meta:
		app_label = 'frontpage'

class Sourcefile(models.Model):
	file_name = models.CharField(max_length=200)
	file_contents = models.TextField()
	app = models.ForeignKey(App)

	objects = BungiesearchManager()

	def __unicode__(self):
		return self.file_name
	
	class Meta:
		app_label = 'frontpage'

class App_metadata(models.Model):
	app_name = models.CharField(blank = True, db_index=True, max_length=100)
	version_string = models.CharField(blank = True, max_length=30)
	author = models.CharField(blank = True, max_length=80)
	date_upload = models.CharField(blank = True, max_length=20)
	description = models.TextField()
	app = models.ForeignKey(App)
	objects = BungiesearchManager()

	def __unicode__(self):
		return self.app_name
	
	class Meta:
		app_label = 'frontpage'


class Permission(models.Model):
	name = models.CharField(max_length=100)
	perm_description = models.TextField()
	perm_danger = models.TextField()
	app = models.ManyToManyField(App)

	objects = BungiesearchManager()

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'


class Activity(models.Model):
	name = models.CharField(max_length=150)
	app = models.ForeignKey(App)
	objects = BungiesearchManager()

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'

class Receiver(models.Model):
	name = models.CharField(max_length=150)
	app = models.ForeignKey(App)
	objects = BungiesearchManager()

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'

class Provider(models.Model):
	name = models.CharField(max_length=150)
	app = models.ForeignKey(App)
	objects = BungiesearchManager()

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'

class Service(models.Model):
	name = models.CharField(max_length=150)
	app = models.ForeignKey(App)

	objects = BungiesearchManager()

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'

class VulnerabilityResult(models.Model):
	name        = models.CharField(max_length=150)
	description = models.TextField()
	confidence  = models.CharField(max_length=10, null=True)
	severity    = models.CharField(max_length=20, null=True)
	dynamicTest = models.BooleanField(default=False)
	scheduledForDT = models.BooleanField(default=False)
	dynamic_test_params = models.TextField(null=True)
	vuln_class  = models.CharField(max_length=300, null=True)
	vuln_method = models.CharField(max_length=300, null=True)
	app         = models.ForeignKey(App, db_index = True)

	objects = BungiesearchManager()

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'

class DynamicTestResults(models.Model):
	name = models.CharField(max_length=150)
	status = models.CharField(max_length=150)
	count = models.IntegerField()
	description = models.TextField()
	vuln = models.ForeignKey(VulnerabilityResult)
	last_check = models.DateField(blank=True, auto_now=True)
	objects = BungiesearchManager()
	#app = models.ForeignKey(App)

	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'frontpage'



# class NoUpdatedField(models.Model):
# 	package_name = models.CharField(max_length=150, db_index=True)

# 	objects = BungiesearchManager()

# 	class Meta:
# 		app_label = 'frontpage'


# class ManagedButEmpty(models.Model):
# 	package_name = models.CharField(max_length=150, db_index=True)

# 	objects = BungiesearchManager()

# 	class Meta:
# 		app_label = 'frontpage'

# class Unmanaged(models.Model):
# 	package_name = models.CharField(max_length=150, db_index=True)

# 	objects = BungiesearchManager()

# 	class Meta:
# 		app_label = 'frontpage'


