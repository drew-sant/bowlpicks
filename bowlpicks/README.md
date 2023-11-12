## Bowl Picks
A small personal project to practice my Django skills and knowlegde.

This web app is made to help facilitate collecting and sharing college
football bowl picks in a group of people.

# Setup

### Setting's File
There are two settings files for the Django project. One for dev and the other for production.
The production one is the default and the dev one needs to activated using the prefix of:

```
DJANGO_DEV=true
```

The full line with runserver would be:

```
DJANGO_DEV=true python manage.py runserver
```

The production settings is included in this repository because I didn't include any sensitive
informantion.

I have this at the bottom of bowlpicks/settings.py:

```
if os.getenv('DJANGO_DEV') == 'true':
    from settings_dev import *
```

This will override the variables from the production settings file with the specified variable in the
settings_dev file. I got this idea from this [form](https://stackoverflow.com/questions/10664244/django-how-to-manage-development-and-production-settings). It has a few other solutions for keeping dev
and production settings seperate if your interested.

# Resources
* [Django Setup](https://medium.com/@sjhomem/creating-a-django-project-base-template-f5bab9f2114c)
* [Django Setup - Structure Files](https://studygyaan.com/django/best-practice-to-structure-django-project-directories-and-files#:~:text=The%20way%20I%20like%20to,content%20in%20the%20media%20folder)
* [Base Templates](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page)
* [Class Based Views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/)
* [Static Files](https://docs.djangoproject.com/en/4.2/howto/static-files/) (Read at deployment)
* [Add Bootstrap to Django](https://www.w3schools.com/django/django_add_bootstrap5.php)
* [Bootstrap Navbar](https://www.quackit.com/bootstrap/bootstrap_5/tutorial/bootstrap_navbars.cfm)
* [CSS Layouts](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout)