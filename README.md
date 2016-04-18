To run:

  Copy ec2_vars/appservers-sample.yml to ec2_vars/appservers.yml, and fill it in.

  Copy ec2_vars/infrastructure-sample.yml to ec2_vars/infrastructure.yml, and fill it in.

These files will be merged at some point.

  Copy sample.settings.py to settings.py, and fill it in.

To use a virtualenv install of ansible, you'll need to run this:

  export PYTHONPATH=/$PATH_TO_YOUR_DJANGO_APPS/aca-aws/lib/python2.7/site-packages/

Example of deploy:
  python deploy.py <project_tag>
