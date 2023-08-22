import argparse
from models import IAC
from iac_operation import iac_operation

def main():
    parser = argparse.ArgumentParser(description="CI parameters for IAC operation")
    parser.add_argument("--iac", help="IAC provider: terraform or pulumi")
    parser.add_argument("--cloud", help="Cloud provider: aws, gcp, azure, ali, tencent")
    parser.add_argument("--resource", help="Resource type: vhost, vpc, subnet, s3, rds, etc.")
    parser.add_argument("--config", help="Custom configuration file")
    args = parser.parse_args()

    iac = IAC(
        IAC_provider=args.iac,
        cloud_provider=args.cloud,
        service_or_resource_type=args.resource,
        status="create",  # or update/delete/read/migrate based on your needs
        config=args.config
    )

    print(iac_operation(iac))

if __name__ == "__main__":
    main()


import argparse
from models import IAC, Playbook
from iac_operation import iac_operation, run_playbook

def main():
    parser = argparse.ArgumentParser(description="CI parameters for IAC operation")
    # ... existing arguments here ...

    parser.add_argument("--inventory", help="Inventory type: dynamic or static")
    parser.add_argument("--playbook", help="Playbook directory or git url")
    parser.add_argument("--config", help="Custom configuration for playbook")
    args = parser.parse_args()

    # ... existing IAC operation here ...

    if args.inventory and args.playbook:
        playbook = Playbook(
            inventory=args.inventory,
            playbook=args.playbook,
            config=args.config
        )
        print(run_playbook(playbook))

if __name__ == "__main__":
    main()
