## Bowl Picks
A small personal project to practice my Django skills and knowlegde.

Bowlpicks is a small web app created with the
[Django](https://www.djangoproject.com/) web framework.

This web app is made to help facilitate collecting and sharing college
football bowl picks in a group of people.

# Setup

### My Development Environment

I am using Visual Studio Code IDE, git and Github for version control,
OS is Ubuntu 22 LTS and Python 3.11.12. I am using venv and all needed
packages are listed in the requirments.txt

### Production Environment

I am hosting the app on DigitalOcean's App Platform. They make it easy and they have this
[guide](https://docs.digitalocean.com/developer-center/deploy-a-django-app-on-app-platform/)
that walks you through the setup.

### Setting's File
When your desiring the development settings, set an evironment variable called ```DEVELOPMENT_MODE```
to True or append it to you command like this:

```
DEVELOPMENT_MODE=True python manage.py runserver
```

If settings.py doesn't find this environment variable then the default value is False.

# mysecrets.py File
mysecrets.py is a file that is gitignored and so this is what it contains so you don't
have to hunt down any errors you would get.

DEV_KEY - a django secret key that I use for development. It doesn't really need to be secret and
you really don't need it because the key will just be auto generated. I have it just because I don't
want users signed out each time I reload my app as I make changes.

CFBD_KEY - An API key for [collegefootballdata.com's](collegefootballdata.com) API. You can get yours
for free [here](https://collegefootballdata.com/key).

# Tests

All tests are in the picks/test/ directory.

Run tests (in dev environment) using:

```
DEVELOPMENT_MODE=True python3 manage.py test
```

# Resources
* [Django Setup](https://medium.com/@sjhomem/creating-a-django-project-base-template-f5bab9f2114c)
* [Django Setup - Structure Files](https://studygyaan.com/django/best-practice-to-structure-django-project-directories-and-files#:~:text=The%20way%20I%20like%20to,content%20in%20the%20media%20folder)
* [Base Templates](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page)
* [Class Based Views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/)
* [Static Files](https://docs.djangoproject.com/en/4.2/howto/static-files/) (Read at deployment)
* [Add Bootstrap to Django](https://www.w3schools.com/django/django_add_bootstrap5.php)
* [Bootstrap Navbar](https://www.quackit.com/bootstrap/bootstrap_5/tutorial/bootstrap_navbars.cfm)
* [CSS Layouts](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout)
* [Testing in Django - Mozilla](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#other_recommended_test_tools)