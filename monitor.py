Sure, here is a complete code example of the implementation, step by step:

Step 1: Create a new Django project.

Code snippet
django-admin startproject monitoring
Step 2: Create a new app called services.

Code snippet
python manage.py startapp services
Step 3: Add the services app to the INSTALLED_APPS setting in settings.py.

Python
INSTALLED_APPS = [
    ...
    'services',
]
Step 4: Create a models.py file in the services app.

Python
from django.db import models

class Service(models.Model):
    url = models.CharField(max_length=255)
    status = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
Step 5: Create a views.py file in the services app.

Python
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

from .models import Service

def index(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'services/index.html', context)

def monitor(request, service_url):
    try:
        response = requests.get(service_url)
        if response.status_code == 200:
            status = 'up'
        else:
            status = 'down'
    except Exception as e:
        status = 'down'

    service = Service.objects.get(url=service_url)
    service.status = status
    service.save()

    if status == 'down':
        send_mail('Service Down', 'The service at {} is down.'.format(service_url), 'noreply@example.com', ['admin@example.com'])

    return HttpResponse('OK')
Step 6: Create a urls.py file in the services app.

Python
from django.urls import path

from .views import index, monitor

urlpatterns = [
    path('', index, name='index'),
    path('monitor/<slug:service_url>/', monitor, name='monitor'),
]
Step 7: Update the urls.py file in the main project.

Python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/', include('services.urls', namespace='services')),
]
Step 8: Create a templates/services/index.html file.

HTML
<!DOCTYPE html>
<html>
<head>
<title>Service Monitoring</title>
</head>
<body>
<h1>Service Monitoring</h1>
<ul>
{% for service in services %}
    <li>
        <a href="{% url 'services:monitor' service.url %}">{{ service.url }}</a>
        <span>{{ service.status }}</span>
    </li>
{% endfor %}
</ul>
</body>
</html>
Step 9: Run the development server.

Code snippet
python manage.py runserver
Step 10: Open the browser and navigate to http://localhost:8000/services/.

You should see a list of all the services that are being monitored. If any of the services are down, you will see a notification in the email inbox that you specified in the code.

I hope this helps!

Sources
1. https://github.com/Exia01/Python
2. https://stackoverflow.com/questions/24216729/django-form-saving-issue-attributeerror-tuple-object-has-no-attribute-get
3. https://github.com/kianbehzad/Zprava-server
4. https://github.com/gonza56d/rat_on
