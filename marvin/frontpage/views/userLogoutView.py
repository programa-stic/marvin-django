from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.http import HttpResponseRedirect

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/frontpage/')