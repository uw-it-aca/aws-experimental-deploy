# Eep
from deploy import run_playbook, BASE_DIR
import os


if __name__ == "__main__":
    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'provision-infrastructure.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    role = 'infrastructure'

    run_playbook(playbook_path, inventory_path, role)
