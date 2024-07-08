"""Various utilities built around sf-cli"""

import json
import sys
import subprocess
import fire


class SfUtils(object):
    """
    Various utilities built around sf-cli
    """

    def reauth(self, target_org: str = None):
        """
        This command re-authenticates a sf-cli authenticated org.

        Often we need to re-authenticate an org with the same alias & credentials, due to expired refresh tokens etc.
        By default, This command re-authenticates the default org, if ran in a project folder. 
        Or Optionally, you can pass alias of the org which you want to re-authenticate.


        :param target_org: If present, re-authenticates the org with given alias instead of the default org
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
            )

            assert "result" in org_details.keys(), "'Result' not found in Org Details!"
            org_details = org_details["result"]

        except subprocess.CalledProcessError as e:
            if target_org:
                print(f"FATAL: Failed to get org details of '{target_org}'")
                print(e)
            else:
                print("FATAL: No default org found")
                print(e)
            sys.exit(1)

        assert "alias" in org_details.keys(), "'alias' not found in org details!"
        org_alias = org_details["alias"]

        try:
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

        assert (
            "instanceUrl" in org_details.keys()
        ), "'instanceUrl' not found in org details!"
        org_instance_url = org_details["instanceUrl"]

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
                org_instance_url,
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

        print(f"Re-authenticated '{org_alias}' Successfully!")
        print("IMPORTANT: Please restart the VS Code, if still getting authentication errors!")


def __sf_utils__():
    fire.Fire(SfUtils)
