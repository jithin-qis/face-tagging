"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

#----------------------------------------
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from core import views as cv

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cv.feed, name='home'),
    path('core/',include('core.urls')),
    path('login/',LoginView.as_view(template_name='core/login.html'),name='login'),
    path('welcome/',cv.welcome,name="welcome"),
    path('accounts/profile/',cv.welcome,name="welcome"),
    path('logout/',LogoutView.as_view(template_name='core/logout.html'),name='logout'),
    path('register/',cv.UserFormView.as_view(template_name='core/registration_form.html'),name='register'),
    url(r'^profile/(?P<username>\w+)/$',cv.profile,name='profile'),
    url(r'^followweb/(?P<username>\w+)/$',cv.followweb,name="followweb"),
    url(r'^unfollowweb/(?P<username>\w+)/$',cv.unfollowweb,name="unfollowweb"),
    url(r'^postweb/(?P<username>\w+)/$',cv.postweb,name="postweb"),
    url(r'^commentweb/(?P<username>\w+)/(?P<post_id>\d+)/$', cv.commentweb,name = "commentweb"),
    path('feed/',cv.feed,name="feed"),
    path('blur/', cv.blur, name='blur'),
    path('blurid/<int:id>/', cv.blurid, name='blurid'),
    path('mailindex/', cv.mailindex, name='mailindex'),
path('clickfun/', cv.clickfun, name='clickfun'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

#---------------------------------------

# from django.contrib import admin
# from django.urls import path,include
# from django.contrib.auth import views as auth_views
# from core import views as user_views
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls import url


# urlpatterns = [
#     path('', user_views.feed, name='home'),
#     path('admin/', admin.site.urls),
#     path('core/',include('core.urls')),
#     path('login/',auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
#      path('welcome/',user_views.welcome,name="welcome"),
#      path('logout/',auth_views.LogoutView.as_view(template_name='core/logout.html'),name='logout'),
#      path('register/',user_views.UserFormView.as_view(template_name='core/registration_form.html'),name='register'),
#      url(r'^profile/(?P<username>\w+)/$',user_views.profile,name='profile'),
#      url(r'^followweb/(?P<username>\w+)/$',user_views.followweb,name="followweb"),
#      url(r'^unfollowweb/(?P<username>\w+)/$',user_views.unfollowweb,name="unfollowweb"),
#      url(r'^postweb/(?P<username>\w+)/$',user_views.postweb,name="postweb"),
#      url(r'^commentweb/(?P<username>\w+)/(?P<post_id>\d+)/$', user_views.commentweb,name = "commentweb"),
#      path('feed/',user_views.feed,name="feed"),
     
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
