from util import set_ansible_display, get_cidr_blocks, get_args
display = set_ansible_display()
# Eep
from deploy import v2_run_playbook, BASE_DIR
import os


if __name__ == "__main__":
    args = get_args()

    project = args.project
    app = args.app
    use = args.use
    # Step one is find the right cidr blocks
    cidr_blocks = get_cidr_blocks(project, app, use)

    print "CD: ", cidr_blocks

    playbook_path = os.path.join(BASE_DIR, 'aca-aws', 'playbooks', 'provision-infrastructure.yml')
    inventory_path = os.path.join(BASE_DIR, 'aca-aws', 'hosts', 'localhost')
    role = 'infrastructure'

    v2_run_playbook('localhost', 'local', playbook_path, inventory_path, role, data={"subnets": cidr_blocks, "aws_tag_Application": app, "aws_tag_Project": project, "aws_service_level": use })
