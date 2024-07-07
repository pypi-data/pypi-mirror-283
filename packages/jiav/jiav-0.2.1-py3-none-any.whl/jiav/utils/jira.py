#!/usr/bin/env python

import jira.exceptions
from jira import JIRA

from jiav import exceptions, logger

jiav_logger = logger.subscribe_to_logger()


class JiraConnection(object):
    """
    Jira connection

    Attributes:
        jira - jira.JIRA object if authenticated successfully.
    """

    def __init__(self, url=str(), username=str(), access_token=str()):
        """
        Attempts to authenticate with Jira API

        Arguments:
            url           - Jira URL
            instance_type - Instance type (cloud or hosted)
            access_token  - Personal Access Token to authenticate with
        """
        # Initiall connection is used to discover details about the Jira instance
        try:
            self.jira = JIRA(server=url)
        except jira.exceptions.JIRAError as e:
            if "JiraError HTTP 404 url" in str(e):
                raise exceptions.NoJiraRestAPIEndpoint(self.jira, e.url) from None
            else:
                raise exceptions.JiraUnhandledException()
        instance_type = self.jira.deploymentType
        # Authenticate with a Jira cloud instance
        if instance_type == "Cloud":
            if not username:
                raise exceptions.JiraMissingCredentials("Username") from None
            self.jira = JIRA(server=url, basic_auth=(username, access_token))
        # Authenticate with a self-hosted Jira instance
        elif instance_type == "Server":
            if username:
                jiav_logger.warning(
                    "Username argument is omitted for self-hosted Jira instances"
                )
            self.jira = JIRA(server=url, token_auth=access_token)
        # Check if authentication was successful
        try:
            self.jira.myself()
        except jira.exceptions.JIRAError as e:
            if "JiraError HTTP 401 url" in str(e):
                raise exceptions.JiraAuthenticationFailed(url) from None
            else:
                raise exceptions.JiraUnhandledException()

    def fetch_issues(self, issues=list(), jql=str()):
        """
        Attempt to fetch issues from Jira
        Requires jira attribute to contain jira.JIRA
        (successful authentication using authenticate method)

        Arguments:
            issues - List of Jira issues
            jql    - Jira Query Language query

        Returns:
            fetched_issues - Fetched Jira issues
        """
        fetched_issues = list()

        # Iterate over provided issues
        if issues:
            for issue in issues:
                try:
                    fetched_issue = self.jira.issue(issue)
                    fetched_issues.append(fetched_issue)
                except jira.exceptions.JIRAError as e:
                    # Full text:
                    # You do not have the permission to see the specified issue
                    if "You do not have the permission to see " in e.text:
                        raise exceptions.PermissionsError(issue) from None
                    elif e.text == "Issue Does Not Exist":
                        raise exceptions.IssueNotExists(issue) from None
                    else:
                        raise exceptions.JiraUnhandledException()
        # Perform JQL query
        elif jql:
            try:
                fetched_issues = self.jira.search_issues(jql)
            except jira.exceptions.JIRAError as e:
                if "Error in the JQL Query:" in e.text:
                    raise exceptions.JQLError(jql, e.text) from None
                elif "for field" and "is invalid" in e.text:
                    raise exceptions.InvalidKeyInJQL(jql, e.text) from None
                else:
                    raise exceptions.JiraUnhandledException()
            if not issues:
                raise exceptions.JQLReturnedNothing(jql)

        jiav_logger.info(f"Discovered issues: {fetched_issues}")
        return fetched_issues

    def check_if_status_is_valid(self, issue=None, desired_status=str()):
        """
        Checks if desired status is a valid status for this issue

        Arguments:
            issue          - Jira issue
            desired_status - Desired status requested by jiav manifest

        Returns:
            transition_id - Workflow transition ID to use when updating
                            the status of the issue
        """
        transition_id = None
        issue_transitions = self.jira.transitions(issue)
        for status in issue_transitions:
            if desired_status == status["name"]:
                transition_id = status["id"]
        return transition_id

    def upload_attachment(self, issue=None, file_path=str()):
        """
        Uploads an attachment to issue

        Arguments:
            issue    - Jira issue
            filename - Path of the file to add as an attachment
        """
        try:
            self.jira.add_attachment(issue=issue, attachment=file_path)
            jiav_logger.info(f"Uploaded attachment to issue {issue}")
        except jira.exceptions.JIRAError:
            raise exceptions.JiraUnhandledException()

    def update_issue_status(self, issue=JIRA.issue, transition_id=str()):
        """
        Update issue status using transition ID discovered by
        jiav.utils.jira.JiraConnection.check_if_status_is_valid

        Arguments:
            issue         - Jira issue
            transition_id - Workflow transition ID to use when updating
                            the status of the issue
        """
        try:
            self.jira.transition_issue(issue, transition=transition_id)
            issue.update()
            jiav_logger.info(f"Updated status for '{issue}'")
        except jira.exceptions.JIRAError:
            raise exceptions.JiraUnhandledException()

    def post_comment(self, issue=None, comment=str()):
        """
        Posts a comment with the result of verification process

        Arguments:
            issue   - Jira issue
            comment - Comment to post
        """
        try:
            self.jira.add_comment(issue, comment)
            jiav_logger.info(f"Posted comment in '{issue}'")
        except jira.exceptions.JIRAError:
            raise exceptions.JiraUnhandledException()
