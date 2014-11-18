You can deploy locally.

Just install python then install django and requests and MySQL-python

Install Mysql and it's lib sudo apt-get install libmysqlclient-dev mysql on ubuntu

From the root of the submission, run  python manage.py syncdb
then python manage.py runserver



To deploy to heroku you need to setup a virtual environment.
Follow https://devcenter.heroku.com/articles/getting-started-with-django

To use Amazon RDS mysql you need to create an account and a database from http://aws.amazon.com/rds/mysql/
Then go to mashtaton/settings.py and changes the host user and password for DATABASES configuration (line 60)

Those were not provided for anonymous submission

