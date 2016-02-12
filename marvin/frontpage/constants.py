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

STATIC_VULN_TYPES = {
    "UNPROTECTED_EXPORTED_COMPONENT" : "Low",
	"NON_SIGNATURE_PROTECTED_EXPORTED_COMPONENT" : "Low",
    "JAVASCRIPTINTERFACE" : "High",
    "APPLICATION_DEBUGGABLE" : "Medium",
    "APPLICATION_BACKUP" : "Medium" ,
    "PHONEGAP_JS_INJECTION" : "High",
    "PHONEGAP_CVE_3500_URL" : "High",
    "PHONEGAP_CVE_3500_ERRORURL" : "High",
    "PHONEGAP_WHITELIST_BYPASS_REGEX" : "Low",
    "PHONEGAP_CVE_3500_REMOTE" : "Critical",
    "PHONEGAP_DEBUG_LOGGING" : "Medium",
    "PHONEGAP_NO_WHITELIST" : "Medium",
    "PHONEGAP_WHITELIST_BYPASS_WILDCARD" : "Medium",
    "REDIS" : "Critical",
    "SSL_CUSTOM_TRUSTMANAGER" : "High",
    "SSL_CUSTOM_HOSTNAMEVERIFIER" : "High",
    "SSL_ALLOWALL_HOSTNAMEVERIFIER" : "High",
    "SSL_INSECURE_SOCKET_FACTORY" : "High",
    "SSL_WEBVIEW_ERROR" : "High",
    "WEBVIEW_FILE_SCHEME" : "High",
    "CRYPTOGRAPHY" : "Medium",
    "INSECURE_STORAGE_WORLD_READABLE/WRITEABLE" : "High",
    "INTENT_HIJACKING" : "Low",
    "UNPROTECTED_DYNAMICALLY_REGISTERED_RECEIVER" : "Low" ,
    "STICKY_BROADCAST_INTENT" : "Medium",
    "AUTOCOMPLETE_PASSWORD_INPUT" : "High",
    "WEBVIEW_SAVED_PASSWORD" : "High",
    "INSECURE_RUNTIME_EXEC_COMMAND" : "Critical",
    "INSECURE_PATHCLASSLOADER": "Critical",
    "BOLTS" : "High"}

DYNAMIC_VULN_TYPES={"ZIP_PATH_TRAVERSAL" : "Critical",
    "INSECURE_TRANSMISSION" : "High",
    "INSECURE_STORAGE": "Medium"}

SEVERITY_PRIORITIES={"Critical":0,
                     "High":1,
                     "Medium":2,
                     "Low":3}