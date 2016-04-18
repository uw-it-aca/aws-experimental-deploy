#!/usr/bin/env python

""" deploy.py- a harness for the ec2_provision playbook. This will probably
    become a django management command eventually.

    This borrows heavily from https://serversforhackers.com/running-ansible-programmatically
"""
# DO NOT change the order of these imports, there's a circular dependency in
# ansible 1.9 that will cause things to break
from ansible.playbook import Playbook
from ansible.inventory import Inventory
from ansible import utils

# v2
from runner import Runner

from boto import ec2

import argparse
import os
import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def v2_run_playbook(hostnames, connection, playbook_path, inventory_path, role, private_key_file=None):
    run_data = {
        'type': role
    }

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


def inventory_for_project(args):
    ec2conn = ec2.connect_to_region(settings.AWS_REGION,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    all_reservations = ec2conn.get_all_reservations()
    reservations = [
        i for a in all_reservations for i in a.instances if 'Project' in i.tags and args.project in i.tags['Project']]
    output = ""
    for i in reservations:
        output += "{0}\n".format(
            i.public_dns_name)
    return output


if __name__ == "__main__":
    # In a django management command, the parser is already instantiated.
    parser = argparse.ArgumentParser(description='The project to deploy.')

    parser.add_argument('project', nargs='?')
    args = parser.parse_args()

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'provision-ec2.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    host = 'localhost'
    role = 'appservers'
    v2_run_playbook(host, 'local', playbook_path, inventory_path, role)

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'simple.yml')
    hosts = inventory_for_project(args)
    private_key_file = settings.AWS_PRIVATE_KEY_FILE
    print hosts

    v2_run_playbook(hosts, 'ssh', playbook_path, hosts, role, private_key_file)
