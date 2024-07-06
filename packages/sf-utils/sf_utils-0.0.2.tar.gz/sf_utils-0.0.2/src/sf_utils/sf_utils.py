"""Various utilities built around sf-cli"""

import json
import sys
import subprocess
import fire


class SfUtils(object):
    """Various utilities built around sf-cli"""

    def reauth(self, target_org: str = None):
        """Reauthenticate the given org

        Keyword arguments:
        target_org -- org-alias to reauthenticate
        """

        org_details_command = ["sf", "org", "display"]
        if target_org:
            org_details_command.append("--target-org")
            org_details_command.append(target_org)
        org_details_command.append("--json")

        org_details = {}
        try:
            print("Finding org details...")
            org_details = json.loads(
                subprocess.run(
                    org_details_command, check=True, shell=True, capture_output=True
                ).stdout
            )["result"]
        except subprocess.CalledProcessError as e:
            if target_org:
                print(f"FATAL: Failed to get org details of '{target_org}'")
                print(e)
            else:
                print("FATAL: No default org found")
                print(e)
            sys.exit(1)

        org_alias = ""
        try:
            org_alias = org_details["alias"]
            print(f"Logging out of '{org_alias}'...")
            org_logout_command = [
                "sf",
                "org",
                "logout",
                "--noprompt",
                "--targetusername",
                org_alias,
            ]
            subprocess.run(
                org_logout_command, check=True, shell=True, capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print(f"FATAL: Failed to logout of '{org_alias}'")
            print(e)
            sys.exit(1)
        except KeyError:
            print("FATAL: Couldn't find 'alias' in org details")
            print(org_details)
            sys.exit(1)

        try:
            print(f"Logging back into '{org_alias}'...")
            org_authenticate_command = [
                "sf",
                "org",
                "login",
                "web",
                "--alias",
                org_alias,
                "--instance-url",
                org_details["instanceUrl"],
            ]

            if not target_org:
                # As no org was passed, we found this org as default
                # so setting this org back as default
                org_authenticate_command.append("--setdefaultusername")

            subprocess.run(
                org_authenticate_command, check=True, shell=True, capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print(f"FATAL: Failed to authenticate {org_alias}")
            sys.exit(1)
        except KeyError:
            print("FATAL: Couldn't find 'instanceUrl' in org details")
            sys.exit(1)

        print(f"Re-authenticated '{org_alias}' Successfully!")
        print("IMPORTANT: Please restart VS Code, if open, for changes to take effect!")


def __sf_utils__():
    fire.Fire(SfUtils)
