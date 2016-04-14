#!/usr/bin/env python

""" deploy.py- a harness for the ec2_provision playbook. This will probably
    become a django management command eventually.

    This borrows heavily from https://serversforhackers.com/running-ansible-programmatically
"""
# DO NOT change the order of these imports, there's a circular dependency in
# ansible 1.9 that will cause things to break.
from ansible.playbook import Playbook
from ansible.inventory import Inventory
try:
    from ansible import callbacks
except:
    pass
from ansible import utils

# v2
from runner import Runner

from boto import ec2

import argparse
import os
import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_playbook(playbook_path, inventory_path, role):

    utils.VERBOSITY = 0
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(
        stats, verbose=utils.VERBOSITY)

    deploy_ec2 = Playbook(
        playbook=playbook_path,
        host_list=inventory_path,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        extra_vars={'type': role}
    )
    results = deploy_ec2.run()


def v2_run_playbook(hostnames, connection, playbook_path, inventory_path, role, private_key_file=None):
    run_data = {
        'type': role
    }

    runner = Runner(
        connection=connection,
        private_key_file=private_key_file,
        hostnames=hostnames,
        playbook=playbook_path,
        run_data=run_data,
        verbosity=3,
    )

    stats = runner.run()


def inventory_for_project(args):
    ec2conn = ec2.connect_to_region(settings.AWS_REGION,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    all_reservations = ec2conn.get_all_reservations()
    reservations = [
        i for a in all_reservations for i in a.instances if 'Project' in i.tags and args.project in i.tags['Project']]
    output = "{"
    for i in reservations:
        output += "'{0}' : [ '{1}' ],".format(
            i.private_dns_name, i.private_ip_address)
    output += "}"
    return output


if __name__ == "__main__":
    # In a django management command, the parser is already instantiated.
    parser = argparse.ArgumentParser(description='The project to deploy.')

    parser.add_argument('project', nargs='?')
    args = parser.parse_args()

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'provision-ec2.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    host = 'localhost'  # This doesn't take a list yet
    role = 'appservers'
    v2_run_playbook(host, 'local', playbook_path, inventory_path, role)

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'simple.yml')
    inv = inventory_for_project(args)
    print inv
    #run_playbook(playbook_path, inv, role)
