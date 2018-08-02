import os
import sys

django_dir           = "/home/juanh/marvin-django/marvin/"
common_modules_dir   = django_dir+"frontpage/"
settings_dir	     = django_dir+"marvin/"

sys.path.append(django_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marvin.settings")
import django
django.setup()
from django.conf import settings
from django.db import connections

import frontpage.settings
#import settings
packages_dir         = frontpage.settings.root_apk_dir
queue_host	     = "172.30.0.7"

marvin_exchange_dl   = "marvin_xchg_dl"
marvin_exchange_andr = "marvin_xchg_androlyze"
marvin_exchange_pr   = "marvin_xchg_pr"

download_queue       = "marvin_download_queue"
androlyze_queue	     = "marvin_androlyze_queue"
process_queue_bayes  = "marvin_bayes_queue"
process_queue_vuln   = "marvin_vuln_queue"
process_queue_monkey = "marvin_monkey_queue"

routing_key_dl	     = "marvin_download"
routing_key_andro    = "marvin_androlyze"
routing_key_new_file = "marvin_new_file"
routing_key_bayes    = "marvin_bayes"
routing_key_vuln     = "marvin_vuln"
routing_key_monkey   = "marvin_monkey"
