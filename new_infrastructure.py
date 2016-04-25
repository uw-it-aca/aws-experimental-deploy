from util import set_ansible_display
display = set_ansible_display()
# Eep
from deploy import v2_run_playbook, BASE_DIR
import os


if __name__ == "__main__":
    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'provision-infrastructure.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    role = 'infrastructure'

    v2_run_playbook('localhost', 'local', playbook_path, inventory_path, role)
