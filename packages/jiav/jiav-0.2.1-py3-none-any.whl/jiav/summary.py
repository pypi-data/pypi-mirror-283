#!/usr/bin/env python

import json

import yaml
from prettytable import SINGLE_BORDER, PrettyTable


def prepare_summary(issues=list(), format="table"):
    """
    Prepares a summary or verified issues

    Arguments:
        issues - Jira issues

        format - Output format
    """
    if format == "json":
        print_json("verified_issues", issues)
    elif format == "yaml":
        print_yaml("verified_issues", issues)
    else:
        print_table("Verified Issues", issues)


def construct_dict(title=str(), issues=list()):
    """
    Constructs a dictionary from received items

    Arguments:
        title - Name of the key

        issues - Jira issues that will populate the value
    """
    dictionary = dict({title.lower(): list()})
    for issue in issues:
        dictionary[title].append(
            dict(
                {
                    "issue": issue.key,
                    "summary": issue.fields.summary,
                    "status": issue.fields.status.name,
                    "assignee": issue.fields.assignee.displayName,
                    "reporter": issue.fields.reporter.displayName,
                    "comments": issue.fields.comment.total,
                }
            )
        )
    return dictionary


def print_json(title=str(), issues=list()):
    """
    Prints a JSON of issues

    Arguments:
        title  - Name of the key

        issues - List of issues
    """
    print(json.dumps(construct_dict(title, issues)))


def print_yaml(title=str(), issues=list()):
    """
    Prints a YAML of issues

    Arguments:
        title  - Name of the key

        issues - List of issues
    """
    print(
        yaml.dump(
            construct_dict(title, issues),
            explicit_start=False,
            default_flow_style=False,
        )
    )


def print_table(title=str(), issues=list()):
    """
    Prints a table of issues

    Arguments:
        title  - Title of the table

        issues - List of issues
    """
    table = PrettyTable()
    table.field_names = [
        "Issue",
        "Summary",
        "Status",
        "Assignee",
        "Reporter",
        "Comments",
    ]
    for issue in issues:
        table.add_row(
            [
                issue,
                issue.fields.summary,
                issue.fields.status,
                (f"{issue.fields.assignee.displayName} "),
                (f"{issue.fields.reporter.displayName} "),
                issue.fields.comment.total,
            ]
        )
    table.set_style(SINGLE_BORDER)
    table.title = title
    print(table)
