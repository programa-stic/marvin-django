# Si el nombre de la clase termina en .java, ya sabemos que el codigo esta en Gitlab.
# Si no, buscamos la clase decompilada: si esta persistida, ya sabemos que existe en gitlab.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from frontpage.models import App, Sourcefile
import frontpage.settings

def show_activity(request, pk, activity_name):
	myApp = App.objects.get(pk=pk)
	if activity_name.endswith('.java'):
		activity_name = activity_name[0:len(activity_name)-5]
		classpath = activity_name.replace('.','/')
		gitname = myApp.package_name.replace('.','-').lower()
		url = frontpage.settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myApp.version+'/'+classpath+'.java'	
		return HttpResponseRedirect(url)	
	else:
		try:
			classpath = activity_name.replace('.','/')
			#mySF = myApp.sourcefile_set.get(file_name=classpath)
			print ("Empiezo a buscar archivos\n")
			filesFound = Sourcefile.objects.filter(file_name=classpath)
			print ("Fin busqueda de archivos\n")
			if len(filesFound) > 0:
				gitname = myApp.package_name.replace('.','-').lower()
				url = frontpage.settings.gitlab_url+'/marvin/'+gitname+'/tree/'+myApp.version+'/'+classpath+'.java'	
				return HttpResponseRedirect(url)
			else:
				context = {"errmsg": "La clase "+ activity_name+" no se halla en el repositorio, puede suceder que haya .DEX suplementarios. "+ str(errmsg)}
				return render(request, 'frontpage/error.html', context)
		except Exception as errmsg:
			context = {"errmsg": "La clase "+ activity_name+" no se halla en el repositorio, puede suceder que haya .DEX suplementarios. "+ str(errmsg)}
			return render(request, 'frontpage/error.html', context)
