#!/usr/bin/env python


class jiavException(Exception):
    """
    Base jiav exception
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class NoJiraRestAPIEndpoint(jiavException):
    """
    Raised when the provided URL is not a valid Jira Rest API endpoint
    """

    def __init__(self, url, endpoint):
        message = f"Provided url '{url}' does not serve Jira Rest API at '{endpoint}'"
        super().__init__(message)


class JiraMissingCredentials(jiavException):
    """
    Raised when user did not provide all required credentials
    """

    def __init__(self, missing_credentials):
        message = f"{missing_credentials} is required for this instance"
        super().__init__(message)


class JiraAuthenticationFailed(jiavException):
    """
    Raised when user did not authenticate correctly with Jira instance
    """

    def __init__(self, url):
        message = (
            f"Failed to authenticate with instance {url}, please check your credentials"
        )
        super().__init__(message)


class PermissionsError(jiavException):
    """
    Raised when failed to fetch content because of permissions
    """

    def __init__(self, issue):
        message = (
            f"You do not have permissions to view {issue}, "
            "please ensure you are using the correct token."
        )
        super().__init__(message)


class IssueNotExists(jiavException):
    """
    Raised when no valid issues were found
    """

    def __init__(self, issue):
        message = f"Issue {issue} does not exist."
        super().__init__(message)


class JQLError(jiavException):
    """
    Raised when JQL error occurs
    """

    def __init__(self, jql, err):
        message = f"{err}.\nQuery is: {jql}"
        super().__init__(message)


class JQLReturnedNothing(jiavException):
    """
    Raised when JQL returns no issues
    """

    def __init__(self, jql):
        message = (
            "No issues returned by query, please ensure your query is "
            "and you are using the correct token."
            f"\nQuery is: {jql}"
        )
        super().__init__(message)


class InvalidKeyInJQL(jiavException):
    """
    Raised when an invalid key in JQL
    """

    def __init__(self, jql, err):
        message = f"{err}.\nQuery is: {jql}"
        super().__init__(message)


class JiraUnhandledException(jiavException):
    """
    Raised when an unhandled exception is raised by
    requests.exceptions.HTTPError
    """

    def __init__(self):
        message = "Unhandled excpetion was raised, please report it"
        super().__init__(message)


class InvalidYAMLException(jiavException):
    """
    Raised when an invalid YAML is supplied
    """

    def __init__(self, py_err):
        super().__init__(str(py_err))


class InvalidManifestException(jiavException):
    """
    Raised when an invalid manifest is supplied
    """

    def __init__(self, py_err):
        super().__init__(str(py_err))


class InvalidBackend(jiavException):
    """
    Raised when an unsupported backend is requested
    """

    def __init__(self, backend):
        message = "{} is not a supported backend".format(backend)
        super().__init__(message)
