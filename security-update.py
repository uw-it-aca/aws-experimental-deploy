from util import set_ansible_display
display = set_ansible_display()
# Eep
import settings
from deploy import v2_run_playbook, BASE_DIR, find_instance_by_tag
import os
import time
import random
import hashlib


if __name__ == "__main__":

    timestamp = int(time.time())
    random_id = hashlib.md5("%s" % random.random()).hexdigest()
    tag_name = "build-%s" % timestamp

    print "TN: ", tag_name, random_id
    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'playbooks', 'create-host-for-updates.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    role = 'infrastructure'
    stats = v2_run_playbook('localhost', 'local', playbook_path, inventory_path, role,
                            extra_tags={ tag_name: random_id })
    print "Stats: ", stats

    host = find_instance_by_tag(tag_name, random_id)
    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'playbooks', 'run-security-updates.yml')
    private_key_file = getattr(settings, 'AWS_PRIVATE_KEY_FILE', None)
    print host.public_dns_name
    print host.id

    stats = v2_run_playbook("%s" % host.public_dns_name, 'ssh', playbook_path,
                            host.public_dns_name, role,
                            data={"instance_id": host.id, "source_ami": host.image_id, "timestamp": time.time(), "host_count": 2 })

    skipped_count = 0
    for host in stats.skipped:
        skipped_count = stats.skipped[host]

    # Steps are skipped if there are no changes in the upgrade step
    if skipped_count == 0:
        playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'playbooks', 'launch-next-ami.yml')
        inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
        v2_run_playbook("localhost", 'local', playbook_path, inventory_path, role, data={"host_count": 2})
