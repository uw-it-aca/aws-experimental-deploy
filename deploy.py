#!/usr/bin/env python

""" deploy.py- a harness for the ec2_provision playbook. This will probably
    become a django management command eventually.

    This borrows heavily from https://serversforhackers.com/running-ansible-programmatically
"""
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
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
    print results


if __name__ == "__main__":
    main()
