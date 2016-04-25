#!/usr/bin/env python

""" deploy.py- a harness for the ec2_provision playbook. This will probably
    become a django management command eventually.

    This borrows heavily from https://serversforhackers.com/running-ansible-programmatically
"""
# DO NOT change the order of these imports, there's a circular dependency in
# ansible 1.9 that will cause things to break
from util import set_ansible_display
display = set_ansible_display()

from ansible.playbook import Playbook
from ansible.inventory import Inventory
from ansible import utils

# v2
from runner import Runner

from boto import ec2

import argparse
import os
import settings

import time
import hashlib
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def v2_run_playbook(hostnames, connection, playbook_path, inventory_path, role, private_key_file=None, extra_tags={}):
    run_data = {
        'type': role,
        'extra_tags': extra_tags,
        'tag_hash_values': '',
    }

    for key in extra_tags:
        run_data['tag_hash_values'] += ',"%s":"%s"' % (key, extra_tags[key])

    # The playbooks can require env set here :(
    if "AWS_ACCESS_KEY_ID" not in os.environ:
        os.environ['AWS_ACCESS_KEY_ID'] = settings.AWS_ACCESS_KEY_ID
        os.environ['AWS_SECRET_ACCESS_KEY'] = settings.AWS_SECRET_ACCESS_KEY

    runner = Runner(
        connection=connection,
        private_key_file=private_key_file,
        hostnames=hostnames,
        playbook=playbook_path,
        run_data=run_data,
        verbosity=8,
    )

    stats = runner.run()

def _get_ec2_conn():
    ec2conn = ec2.connect_to_region(settings.AWS_REGION,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return ec2conn

def inventory_for_project(args):
    ec2conn = _get_ec2_conn()

    all_reservations = ec2conn.get_all_reservations()
    reservations = [
        i for a in all_reservations for i in a.instances if 'Project' in i.tags and args.project in i.tags['Project']]
    output = ""
    for i in reservations:
        output += "{0}\n".format(
            i.public_dns_name)
    return output

def find_instance_by_tag(tag_name, tag_value):
    ec2conn = _get_ec2_conn()
    val = ec2conn.get_all_instances(filters={"tag:%s" % tag_name : tag_value })
    if len(val) > 1:
        raise Exception("Multiple matches?  Inconceivable!")

    instances = [i for r in val for i in r.instances]
    if len(instances) > 1:
        raise Exception("Multiple matches?  Inconceivable!")
    return instances[0]

if __name__ == "__main__":
    # In a django management command, the parser is already instantiated.
    parser = argparse.ArgumentParser(description='The project to deploy.')

    parser.add_argument('project', nargs='?')
    args = parser.parse_args()

    timestamp = int(time.time())
    random_id = hashlib.md5("%s" % random.random()).hexdigest()
    tag_name = "build-%s" % timestamp

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'provision-ec2.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    host = 'localhost'
    role = 'appservers'
    v2_run_playbook(host, 'local', playbook_path, inventory_path, role,
                    extra_tags={ tag_name: random_id })

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'simple.yml')
    host = find_instance_by_tag(tag_name, random_id)
    private_key_file = getattr(settings, 'AWS_PRIVATE_KEY_FILE', None)
    print host.public_dns_name

    v2_run_playbook("%s" % host.public_dns_name, 'ssh', playbook_path,
                    host.public_dns_name, role, private_key_file)
