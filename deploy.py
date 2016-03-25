#!/usr/bin/env python

""" deploy.py- a harness for the ec2_provision playbook. This will probably
    become a django management command eventually.

    This borrows heavily from https://serversforhackers.com/running-ansible-programmatically
"""
# DO NOT change the order of these imports, there's a circular dependency in
# ansible 1.9 that will cause things to break.
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

import argparse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def launch_ec2():

    playbook_path = os.path.join(BASE_DIR, 'aws', 'provision-ec2.yml')
    inventory_path = os.path.join(BASE_DIR, 'aws', 'hosts', 'localhost')
    print playbook_path
    print inventory_path

    utils.VERBOSITY = 0
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    deploy_ec2 = PlayBook(
        playbook = playbook_path,
        host_list=inventory_path,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        extra_vars = {'type': 'appservers'}
    )
    results = deploy_ec2.run()
    print '-'*79
    print results


if __name__ == "__main__":
    # In a django management command, the parser is already instantiated.
    parser = argparse.ArgumentParser(description='The project to deploy.')

    parser.add_argument('project', nargs='?')
    project = parser.parse_args()
    print project

    launch_ec2()
