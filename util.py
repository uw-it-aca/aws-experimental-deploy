import settings
import argparse
from boto import ec2
from boto import vpc

def _get_ec2_conn():
    ec2conn = ec2.connect_to_region(settings.AWS_REGION,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return ec2conn


def get_vpc_conn():
    vpc_conn = vpc.connect_to_region(settings.AWS_REGION,
                                     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return vpc_conn


def set_ansible_display():
    from ansible.utils.display import Display
    verbosity = getattr(settings, 'VERBOSITY', 0)
    display = Display(verbosity=verbosity)
    return display


def get_cidr_blocks(project, app, use):
    vpc_conn = get_vpc_conn()
    vpcs = vpc_conn.get_all_vpcs(filters={"tag:Use": use, "tag:Project": project})

    prefix = "10.1.0"
    if len(vpcs) > 0:
        subnets = vpc_conn.get_all_subnets(filters={"vpcId": vpcs[0].id, "tag:Use": use, "tag:Project": project, "tag:Application": app})

        print "S: ", subnets

        if len(subnets) == 0:
            subnets = vpc_conn.get_all_subnets()
            print "S2: ", subnets
            for subnet in subnets:
                print subnet.cidr_block

    return {
        "app_subnet1": "%s.0/27" % prefix,
        "app_subnet2": "%s.32/27" % prefix,
        "db_subnet1": "%s.64/28" % prefix,
        "db_subnet2": "%s.80/28" % prefix,
        "elasticache_subnet1": "%s.96/28" % prefix,
        "elasticache_subnet2": "%s.112/28" % prefix,
    }

def get_args():
    parser = argparse.ArgumentParser(description='The project to deploy.')
    parser.add_argument('--project', nargs='?')
    parser.add_argument('--app', nargs='?')
    parser.add_argument('--use', nargs='?', help="Service level (production, test, ...)")
    args = parser.parse_args()

    if not args.project:
        raise Exception("--project is required")
    if not args.app:
        raise Exception("--app is required")
    if not args.use:
        raise Exception("--use is required")

    return args
