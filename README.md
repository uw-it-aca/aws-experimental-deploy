To run:

  Copy vars/app-sample.yml to vars/app.yml, and fill it in.

  Copy sample.settings.py to settings.py, and fill it in.

To use a virtualenv install of ansible, you'll need to run this:

  export PYTHONPATH=/$PATH_TO_YOUR_DJANGO_APPS/aca-aws/lib/python2.7/site-packages/

Example of deploy:
  python deploy.py <project_tag>
