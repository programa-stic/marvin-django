from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from frontpage.models import User


@login_required
def user_crud(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user, created = User.objects.get_or_create(username=username, email='')
        if not created:
            return render(request,'frontpage/user_crud.html', {'msg':"El usuario ya existe en la base de datos."})
        if user:
            user.set_password(password)
            user.save()
            return render(request,'frontpage/user_crud.html', {'msg':"Usuario creado exitosamente."})
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid creation details: {0}, {1}".format(username, password)
            return render(request,'frontpage/user_crud.html', {'msg':"No fue posible agregar el usuario."})
    else:
        return render(request,'frontpage/user_crud.html', {})