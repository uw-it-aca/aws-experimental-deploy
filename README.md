To run:

  Copy ec2_vars/appservers-sample.yml to ec2_vars/appservers.yml, and fill it in.

To use a virtualenv install of ansible, you'll need to run this:

  export PYTHONPATH=/$PATH_TO_YOUR_DJANGO_APPS/aca-aws/lib/python2.7/site-packages/

To configure your aws credentials (this will change?)

  export AWS_ACCESS_KEY_ID='AK123'
  export AWS_SECRET_ACCESS_KEY='abc123'
