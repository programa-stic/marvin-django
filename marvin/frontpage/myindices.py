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

from frontpage.models import App
from frontpage.models import Sourcefile
from frontpage.models import Permission
from frontpage.models import Service
from frontpage.models import Activity
from frontpage.models import Provider
from bungiesearch.fields import StringField
from bungiesearch.indices import ModelIndex


class AppIndex(ModelIndex):
    #effectived_date = DateField(eval_as='obj.created if obj.created and obj.published > obj.created else obj.published')
    meta_data = StringField(eval_as='" ".join([fld for fld in [obj.package_name, obj.app_name, obj.md5, obj.sha1] if fld])')

    class Meta:
        model = App
        #exclude = []
        #hotfixes = {}
    default = True

class SourcefileIndex(ModelIndex):
    #effectived_date = DateField(eval_as='obj.created if obj.created and obj.published > obj.created else obj.published')
    meta_data = StringField(eval_as='" ".join([fld for fld in [obj.file_name, obj.file_contents] if fld])')

    class Meta:
        model = Sourcefile
        exclude = ('file_contents')
        #hotfixes = {}
    default = True

class PermissionIndex(ModelIndex):
    #effectived_date = DateField(eval_as='obj.created if obj.created and obj.published > obj.created else obj.published')
    #meta_data = StringField(eval_as='" ".join([fld for fld in [obj.link, str(obj.tweet_count), obj.raw] if fld])')

    class Meta:
        model = Permission
        #exclude = ('raw', 'missing_data', 'negative_feedback', 'positive_feedback', 'popularity_index', 'source_hash')
        #hotfixes = {}
    default = True

class ActivityIndex(ModelIndex):
    #effectived_date = DateField(eval_as='obj.created if obj.created and obj.published > obj.created else obj.published')
    #meta_data = StringField(eval_as='" ".join([fld for fld in [package_name, app_name, md5, sha1] if fld])')

    class Meta:
        model = Activity
        #exclude = ('raw', 'missing_data', 'negative_feedback', 'positive_feedback', 'popularity_index', 'source_hash')
        #hotfixes = {}
    default = True

class ServiceIndex(ModelIndex):
    #effectived_date = DateField(eval_as='obj.created if obj.created and obj.published > obj.created else obj.published')
    #meta_data = StringField(eval_as='" ".join([fld for fld in [obj.link, str(obj.tweet_count), obj.raw] if fld])')

    class Meta:
        model = Service
        #exclude = ('raw', 'missing_data', 'negative_feedback', 'positive_feedback', 'popularity_index', 'source_hash')
        #hotfixes = {}
    default = True

class ProviderIndex(ModelIndex):
    #effectived_date = DateField(eval_as='obj.created if obj.created and obj.published > obj.created else obj.published')
    #meta_data = StringField(eval_as='" ".join([fld for fld in [obj.link, str(obj.tweet_count), obj.raw] if fld])')

    class Meta:
        model = Provider
        #exclude = ('raw', 'missing_data', 'negative_feedback', 'positive_feedback', 'popularity_index', 'source_hash')
        #hotfixes = {}
    default = True


