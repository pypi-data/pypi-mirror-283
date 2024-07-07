#!/usr/bin/env python

import argparse
import sys

import jiav.constants
from jiav import logger, summary, verification
from jiav.api import manifest
from jiav.utils.jira import JiraConnection


# NOTE(vkhitrin): I am not sure argparse is the best tool for parsing
#                 subcommands, but right now this is one less dependency
#                 to manage
class JiavCLI(object):
    def __init__(self):
        self.debug = False
        self.parser = type(argparse.ArgumentParser)
        self.arguments = list()

    def parse(self, in_args):
        """
        Parse arugmunets passed from command line

        Arguments:
            in_args - Arguments passed via command line
        """
        self.arguments = in_args
        self.parser = argparse.ArgumentParser(
            description="Jira Issues Auto Verification Tool",
            usage="""jiav [-v | --version] [-d | --debug] <command> [<args>]

Global flags
    -v --version    prints version
    -d --debug      show debug

Available commands
    verify               Verifies issues
    list-backends        List available backends
    validate-manifest    Validate jiav manifest
""",
            add_help=True,
        )
        self.parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=jiav.constants.__VERSION__,
        )
        self.parser.add_argument(
            "-d", "--debug", help="show debug", action="store_true"
        )
        self.parser.add_argument(
            "command",
            help="Subcommand to run",
            choices=["verify", "list-backends", "validate-manifest"],
        )
        # Exclude the first argument which is the program
        args = self.parser.parse_known_args(self.arguments[1:])
        self.debug = args[0].debug
        self.arguments.remove(args[0].command)
        if "-" in args[0].command:
            args[0].command = args[0].command.replace("-", "_")
        if not hasattr(self, args[0].command):
            self.parser.print_help()
            exit(1)
        # We remove the action '_StoreAction...dest='command' which
        # in our case is always last in the list
        del self.parser._actions[-1]
        # Use dispatch pattern to invoke method with same name
        getattr(self, args[0].command)()

    def verify(self):
        self.parser.usage = """jiav [-v | --version] [-d | --debug] verify [<args>]

Global flags
    -v --version    prints version
    -d --debug      show debug

Mandatory arguments
    -j --jira                      instance URL
    -u --username                  Jira Cloud username (not required for self-hosted
                                   instances)
    -a --access-token              the personal access token

Mutual exclusive arguments related to issues
    -i --issue                     issue to be verified
    -q --query                     JQL query

Optional arguments
    -f --format                    output format
    --upload-attachment-unsafe     uploads attachment of execution, this is not
                                   safe since all users who can access the
                                   ticket will be able to view it; refer to:
                                   https://jira.atlassian.com/browse/JRASERVER-3893
    --allow-public-comments        allows to read manifest from non-private
                                   comments; this is potentially dangerous
                                   since unexpected users will be able to
                                   provide a manifest
    --dry-run                      execute manifests without updating issues
"""
        self.parser.add_argument(
            "-f",
            "--format",
            choices=["table", "json", "yaml"],
            type=str,
            default="table",
        )
        self.parser.add_argument("-j", "--jira", required=True, type=str)
        self.parser.add_argument("--upload-attachment-unsafe", action="store_true")
        self.parser.add_argument("--allow-public-comments", action="store_true")
        self.parser.add_argument("--dry-run", action="store_true")
        login_group = self.parser.add_argument_group(title="Login")
        login_group.add_argument("-a", "--access-token", type=str, required=True)
        login_group.add_argument("-u", "--username", type=str)
        arg_group = self.parser.add_mutually_exclusive_group(required=True)
        arg_group.add_argument("-i", "--issue", action="append", type=str)
        arg_group.add_argument("-q", "--query", type=str)
        args = self.parser.parse_args(sys.argv[1:])
        # Init logger
        jiav_logger = logger.configure_logger(args.debug)
        # Init variables
        issues = list()
        verifeid_issues = list()
        # If user requested to upload attachment, warn them
        if args.upload_attachment_unsafe:
            jiav_logger.warn(
                """Will upload attachment of the execution, this might leak sensitive
                information, refer to: https://jira.atlassian.com/browse/JRASERVER-3893"""  # noqa
            )
        # If user requested to include public comments, warn them
        if args.allow_public_comments:
            jiav_logger.warn("Will include public comments in search")
        # Try to authenticate with Jira
        jira_connection = JiraConnection(
            url=args.jira,
            username=args.username,
            access_token=args.access_token,
        )
        # Fetch issues from authenticated Jira instance
        issues = jira_connection.fetch_issues(issues=args.issue, jql=args.query)
        # Iterate over valid issues and attempt to update and verify them
        verifeid_issues = verification.verify_issues(
            issues=issues,
            jira_connection=jira_connection,
            upload_attachment=args.upload_attachment_unsafe,
            allow_public_comments=args.allow_public_comments,
            dry_run=args.dry_run,
        )
        # Print summary
        summary.prepare_summary(issues=verifeid_issues, format=args.format)

    def list_backends(self):
        """
        List installed backends
        """
        self.parser.usage = """jiav [-v | --version] [-d | --debug] list-backends

Global flags
    -v --version    prints version
    -d --debug      show debug

List backends located in 'jiav/backends' directory
"""
        self.parser.parse_args(self.arguments[1:])
        print(jiav.constants.EXPOSED_BACKENDS)

    def validate_manifest(self):
        """
        Validate manifest
        """
        self.parser.usage = """jiav [-v | --version] [-d | --debug] validate-manifest [<args>]

Global flags
    -v --version    prints version
    -d --debug      show debug

Mandatory arguments
    -f --from-file    path to local file containing manifest
"""  # noqa
        verification, content = None, None
        self.parser.add_argument(
            "-f", "--from-file", type=argparse.FileType("r"), required=True
        )
        args = self.parser.parse_args(self.arguments[1:])
        jiav_logger = logger.configure_logger(debug=True)
        if args.from_file:
            content = args.from_file.read()
            jiav_logger.info(f"Provided manifest via file:\n{content}")
        verification = manifest.validate_manifest(text=content)
        if verification:
            jiav_logger.info("Provided YAML is valid")
        else:
            jiav_logger.error("Provided manifest is not valid")
            sys.exit(1)


def main():
    cli_client = JiavCLI()
    cli_client.parse(sys.argv)


if __name__ == "__main__":
    main()
