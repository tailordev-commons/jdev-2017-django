---
transition: fade
logo: 'https://tailordev.fr/favicon-16x16.png'
---

# Django 101, Hands-on!

#### [JDEV T4.A06](http://devlog.cnrs.fr/jdev2017/t4.a06)
Marseille (France) - 2017/07/05

---

## `$ whoami`

* :fa-twitter: [`@julienmaupetit`](https://twitter.com/julienmaupetit/)
* PhD in structural bioinformatics (Paris Diderot)
* Research engineer (RPBS platform, Paris Diderot)
* Co-founder of [TailorDev](https://tailordev.fr) (Clermont-Ferrand)

> What about you?

---

## Disclaimer

> Do you `git`, `bash`, `python`?

---

## Outline

1. A brief theoretical introduction to Django
2. Bootstrap your project
3. Create yout first Django application

--- 

## Install party!

For the practical part, you will need:

* a UNIX shell (`bash`, `zsh`, …)
* `git`
* `python >= 3.4`
* `ping www.google.fr`

> Ready?

---

## Goal

> Develop `climate`, a Django application that displays average temperature records by country since the 18th century.

* Load data from the [Climate Change: Earth Surface Temperature Data](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data) Kaggle dataset (csv),
* Store data in a database,
* View tabular data per country,
* Plot data per country (optional).

--- 

# A short introduction to Django

----

## MTV framework

**M**odel - **T**emplate - **V**iew

----

## Django's ORM

ORM = **O**bject **R**elated **M**apper

```python
# A model is a python class
class Record(models.Model):
    """Temperature record"""

    date = models.DateField()

    temperature = models.DecimalField(
        "Average temperature",
        help_text="In Celcius",
        decimal_places=3,
        max_digits=6,
        null=True,
        blank=True,
    )

    uncertainty = models.DecimalField(
        "Average temperature uncertainty",
        help_text="The 95% confidence interval around the average",
        decimal_places=3,
        max_digits=6,
        null=True,
        blank=True,
    )

    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ('country', 'date')
        unique_together = ('date', 'country')

    def __str__(self):
        return '{} - {}'.format(self.country, self.date
```

Checkout Django's documentation for an exaustive list of `Field` types.

----

## Making queries

```python
import datetime

from .models import Record

# Get all records
records = Record.objects.all()

# Get records from 2017
current_year_records = Record.objects.filter(date__year=2017)
```

----

## Create views

Django as generic views for CRUD operations and more :tada:

```python
from django.views.generic.list import DetailView

from .models import Record


class RecordDetailView(DetailView):

    model = Record
````

----

## Django Templates

HTML + template language

```html
<!-- my_app/record_detail.html -->
<html>
  <head>
    <title>Record detail</title>
  </head>
  <body>
    <h1>Record {{ record.id }}</h1>
    
    Sampling date: {{ record.date | date }}
    ...
  </body>
</html>
```

----

## URL dispatcher

Routing is mapping URLs and views

```python
from django.conf.urls import url

from .views import RecordDetailView

urlpatterns = [
    url(r'^record/(?P<pk>\d+)/$', RecordDetailView.as_view(), name='record_detail'),
]
```

---

# Bootstraping

----

## Virtualenv

Create a `virtualenv` for your first django project:

```bash
$ cd my/projects/directory
$ mkdir django-101
$ cd django-101
$ python3 -m venv venv
```

Activate the newly created `virtualenv`:

```bash
$ source venv/bin/activate
# Now your prompt should be modified:
(venv) $ 
```

----

## Django

Install the latest Django release with `pip`:

```bash
(venv) $ pip install Django
```

And create your Django project:

```bash
(venv) $ django-admin startproject climate . 
# Have you seen the `.` at the end of this latest command?
```

----

## Django project tree

A typical Django project tree looks like the following:

```
.
├── climate
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── venv
    └── ...
```

----

## `manage.py`

Django management command is central to the Django ecosystem.

```bash
# See available commands
(venv) $ python manage.py
# Run the development server
(venv) $ python manage.py runserver
# Quit the server with CTRL+C
```

> You should see a warning message about migrations, no worries, we will fix that later.

You can browse to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to check that everything works :tada:

----

## Versioning

Now it's time to start versioning our project with `git`:

```bash
(venv) $ git init .
# Download a .gitignore template for Python projects from github
(venv) $ curl -qs 'https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore' > .gitignore
# Add project requirements
(venv) $ pip freeze | grep Django > requirements.txt
# Make your first commit
(venv) $ git add .gitignore climate/ manage.py requirements.txt
(venv) $ git commit -m 'Start climate project'
```

**Remark**: your `venv` directory should be ignored (see `.gitignore` file rules)

---

# Create a Django app

----

## Your first Django application

```bash
(venv) $ python manage.py startapp temperature
(venv) $ git add temperature
(venv) $ git commit -m 'Add temperature base application'
```

The `temperature` application should look like:

```
temperature
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

----

## Data models (1)

Look at the `GlobalLandTemperaturesByCountry.csv` dataset [1], and propose a relational model to store the data.

[1] https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data

----

## Data models (2)

Let's create our first Django models for the temperature application:

```python
# temperature/models.py
from django.db import models


class Country(models.Model):
    """Country where the data have been recorded"""

    name = models.CharField(
        max_length=100,
        unique=True
    )


class Record(models.Model):
    """Temperature record"""

    date = models.DateField()

    temperature = models.DecimalField(
        "Average temperature",
        help_text="In Celcius",
        decimal_places=3,
        max_digits=6,
        null=True,
        blank=True,
    )

    uncertainty = models.DecimalField(
        "Average temperature uncertainty",
        help_text="The 95% confidence interval around the average",
        decimal_places=3,
        max_digits=6,
        null=True,
        blank=True,
    )

    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = ('date', 'country')
```

----

## Add the application to the project

You should explicitely add your application to the project to activate it:

```python
# climate/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'temperature',  # your Django application
]
```

----

## Migrate data

Django migrations are suites of python scripts that incrementally makes your database schema evolve.

```bash
# create temperature app migrations
(venv) $ python manage.py makemigrations temperature

# Perform all migrations
(venv) $ python manage.py migrate
```

> You need to create a migration everytime you change your models or add new models to your application.

----

## Commit!

```bash
# Ignore sqlite database versioning
(venv) $ echo 'db.sqlite3' >> .gitignore

# Commit your work
(venv) $ git add \
	.gitignore \
	climate/settings.py \
	temperature/models.py \
	temperature/migrations/0001_initial.py 
(venv) $ git commit -m 'Add temperature models'
```

----

## Django Admin (1)

Make your data visible in Django admin interface:

```python
# temperature/admin.py
from django.contrib import admin

from .models import Country, Record


admin.site.register(Country)
admin.site.register(Record)
```

```bash
# Commit
(venv) $ git add temperature/admin.py
(venv) $ git commit -m 'Register temperature models for admin'
```

----

## Django Admin (2)

To access Django admin, we need to create a superuser (aka administrator) allowed to log in:

```bash
# create a super user
(venv) $ python manage.py createsuperuser \
	--username watson \
	--email watson@crick.io
```

> You will be asked to type `watson` user password twice

Now go to: http://127.0.0.1:8000/admin/ :tada:

---

# Import data from CSV files

----

## Fetch data

Download the file `GlobalLandTemperaturesByCountry.csv` from the [Climate Change: Earth Surface Temperature Data](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data) project.

```bash
# This is where we will store the data
(venv) $ mkdir temperature/fixtures

# Register to Kaggle, download it and save it as temperature/fixtures/temperature_by_country.csv
# or download it from this project repository
(venv) $ curl -qs 'https://github.com/tailordev-commons/climate/blob/master/temperature/fixtures/temperature_by_country.csv?raw=true' > temperature/fixtures/temperature_by_country.csv

# Commit the data
(venv) $ git add temperature/fixtures/temperature_by_country.csv
(venv) $ git commit -m 'Add temperatures by country fixture'
```

----

## Create a Django management command (1)

```bash
# Prepare management command tree
(venv) $ mkdir -p temperature/management/commands
(venv) $ touch \
	temperature/management/__init__.py \
	temperature/management/commands/__init__.py \
	temperature/management/commands/load_records.py
```

Your `management` folder should look like:

```
temperature/management
├── __init__.py
└── commands
    ├── __init__.py
    └── load_records.py
```

----

## Create a Django management command (2)

```python
# temperature/management/commands/load_records.py
import csv
import os.path

from datetime import datetime
from decimal import Decimal as D
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from temperature.models import Country, Record


def _import_record_from_csv_row(dt, temperature, uncertainty, country_name):
    """Import a record from a csv file row data"""

    country, _ = Country.objects.get_or_create(name=country_name)

    try:
        Record.objects.create(
            date=dt,
            temperature=temperature if len(temperature) else None,
            uncertainty=uncertainty if len(uncertainty) else None,
            country=country
        )
    except IntegrityError:
        # Unique constraint (date, country) raise an IntegrityError when trying
        # to save the same record twice. We ignore this error here as we want to
        # be able to run the load_records command more than once.
        pass


def load_data(csv_file_name):
    """Load data from input csv_file file"""

    # TODO
    # Optimize importation by using Record.objects.bulk_create on a country
    # basis
    with open(csv_file_name) as csv_file:
        dataset_reader = csv.DictReader(csv_file)
        for row in dataset_reader:
            _import_record_from_csv_row(*row.values())


class Command(BaseCommand):
    help = "Load temperature records from a csv file"

    def add_arguments(self, parser):
        parser.add_argument('CSV_FILE')

    def handle(self, *args, **options):
        csv_file_name = options['CSV_FILE']

        self.stdout.write(
            "Will import dataset from file: {}".format(csv_file_name)
        )

        # check that the file exists
        if not os.path.exists(csv_file_name):
            raise CommandError(
                "CSV file {} does not exists".format(csv_file_name)
            )

        load_data(csv_file_name)

        self.stdout.write(
            self.style.SUCCESS(
                "Temperature dataset has been successfully imported"
            )
        )
```

----

## Commit!

```
(venv) $ git add temperature/management
(venv) $ git commit -m 'Add load records management command'
```

----

## Improve Admin exploration (1)

Add `__str__` methods to your models:

```python
# temperature/models.py
class Country(models.Model):
    # [...]
    def __str__(self):
        return self.name
        
        
class Record(models.Model):
    # [...]
    def __str__(self):
    	return '{} - {}'.format(self.date, self.country)
```

> Remember to `git commit` this!

----

## Improve Admin exploration (2)

Make records exploration in the admin great again with a dedicated `ModelAdmin`:

```python
# temperature/admin.py
from django.contrib import admin

from .models import Country, Record


class RecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('country', 'date', 'temperature', 'uncertainty')
    list_filter = ('country', )


admin.site.register(Country)
admin.site.register(Record, RecordAdmin)
```

> What should you do? Hint: it starts with `git`.

---

# Create a Django view

---- 

## Record list view

In a first approach, we will define a generic view to list records:

```python
# temperature/views.py
from django.views.generic.list import ListView

from .models import Record


class RecordListView(ListView):

    model = Record
    paginate_by = 50
```

> Use http://ccbv.co.uk to help you develop your generic class-based view.

----

## Record list view url (1)

You must define an url that point to your view:
```python
# temperature/urls.py
from django.conf.urls import url

from .views import RecordListView

urlpatterns = [
    url(r'^$', RecordListView.as_view(), name='record_list'),
]
```
----

## Record list view url (2)

Add the `temperature` application urls to your project:

```python
# climate/urls.py
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('temperature.urls'))
]
```

Now browse to: http://127.0.0.1:8000 

> What is missing?

----

## Record list template (1)

Create a Django template for your view:

```bash
(venv) $ mkdir temperature/templates/temperature
(venv) $ touch temperature/templates/temperature/record_list.html
```
----

## Record list template (2)

This template could be designed as follows:

```html
<!-- temperature/templates/temperature/record_list.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Temperature records</title>
  </head>
  <body>
    <h1>Temperature records</h1>

    <table>
      <thead>
        <tr>
          <th>Date</th>
          <th>Average Temperature (° C)</th>
          <th>Uncertainty</th>
          <th>Country</th>
        </tr>
      </thead>
      <tbody>
        {% for record in record_list %}
        <tr>
          <td>{{ record.date | date }}</td>
          <td>{{ record.temperature | default:"N/A" }}</td>
          <td>{{ record.uncertainty | default:"N/A" }}</td>
          <td>{{ record.country.name }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>

    <div class="pagination">
      <span class="step-links">
        {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">&lt; previous</a>
        {% endif %}

        <span class="current">
          Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
        </span>

        {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">next &gt;</a>
        {% endif %}
      </span>
  </div>
  </body>
</html>
```

----

## Admire the view

Now browse to: http://127.0.0.1:8000 :tada:


And commit your work:

```bash
(venv) $  git add \
    temperature/views.py \
    temperature/urls.py \
    temperature/templates/ \
    climate/urls.py
(venv) $ git commit -m 'Add paginated record list view'
```

----

## Make it a little bit prettier\* (1)

```bash
(venv) $ mkdir -p temperature/static/temperature/css
(venv) $ touch temperature/static/temperature/css/temperature.css
```

*optional

----

## Make it a little bit prettier (2)

```css
// temperature/static/temperature/css/temperature.css
body {
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  color: #333;
}

h1 {
  text-align: center;
}

table {
  width: 100%;
}

table thead tr th {
  border-bottom: 1px solid #333;
}

table tr:nth-child(even) {
  background-color: #e6e6e6;
}

table tr > * {
  width: 25%;
  text-align: right;
  padding: 0.4rem;
}

table tr > *:first-child {
  text-align: left;
}

.pagination {
  margin-top: 1rem;
  padding-top: 1rem;
  text-align: center;
  border-top: 1px solid #333;
}
```

----

## Make it a little bit prettier (3)

Invite your stylesheet to join the party:

```html
{% load static %} <!-- load static templatetags -->

<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Temperature records</title>
    <!-- Add your stylesheet here -->
    <link rel="stylesheet" href="{% static "temperature/css/temperature.css" %}">
  </head>
  <body>
  <!-- [...] -->
```
> And don't forget to? Commit your work, yes!

---

# Test your Django application

----

## py.test

```bash
(venv) $ pip install pytest pytest-django
(venv) $ echo -e 'pytest\npytest-django' > requirements-dev.txt
(venv) $ touch pytest.ini
```

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE=climate.settings
addopts = -vs
testpaths = temperature/tests
```

----

## Tests tree

Prepare your test tree:

```bash
(venv) $ git rm temperature/tests.py
(venv) $ mkdir temperature/tests
(venv) $ touch temperature/tests/{__init__.py,test_views.py}
```

Commit your work before writting your first test:

```bash
(venv) $ git add pytest.ini requirements-dev.txt temperature/tests
(venv) $ git commit -m 'Add & configure pytest'
```

---- 

## Add your first test

Write a first test for your `record_list` view:

```python
# temperature/tests/test_views.py
import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase


@pytest.mark.django_db
class RecordListViewTests(TestCase):
    """Tests for the RecordListView"""

    def setUp(self):
        self.url = reverse('record_list')

    def test_get(self):
        """Test the RecordListView get method"""
        response = self.client.get(self.url)

        # Test response code and used template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('temperature/record_list.html')
```

----

# Run the test suite

Your smoke test should pass:

```bash
(venv) $ pytest
```

> We need to write many more tests now (management command, models, etc.)

---

## That's all folks!

![](https://media.giphy.com/media/Mp4hQy51LjY6A/giphy.gif)
