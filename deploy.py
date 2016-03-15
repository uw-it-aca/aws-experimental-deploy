#!/usr/bin/env python

""" deploy.py- a harness for the ec2_provision playbook. This will probably
    become a django management command eventually.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    print BASE_DIR

if __name__ == "__main__":
    main()
