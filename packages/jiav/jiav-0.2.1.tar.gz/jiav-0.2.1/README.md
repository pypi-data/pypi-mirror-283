# jiav

> [!NOTE]
> This repository is a **Proof of Concept.**

## Limitations And Words Of Caution

Since this tool executes commands locally, we should avoid trusting public comments as much as possible.  
It will default to scanning only private comments (regardless of the visibility group). It is possible to read from public comments **if you understand the potential risk, this might cause to your systems**.

The output of verification steps is also not uploaded as attachments by default because it is impossible to limit attachments' visibility, refer to [JRASERVER-3893](https://jira.atlassian.com/browse/JRASERVER-3893). It is possible to attach the output **if you understand the potential risk, this might expose sensitive information**.

## General

![jiav flow](https://jiav.readthedocs.io/en/latest/_images/Flow.jpeg)

Jira Issues Auto Verification.  
This tool aims to provide an auto-verification framework for Jira issues.  
Users provide a YAML-formatted comment in Jira issues, and the tool will execute it.
On successful execution, the issue will move to the desired status.

Example of a manifest:

```yaml
---
jiav:
  verified_status: "Done" # Status has to be present in the project workflow
  verification_steps:
    - name: Check line exists in file
      backend: line
      path: /path/to/file
      line: hello_world
```

`jiav` allows developers to build custom backends; refer to the [documentation guide](docs/source/developing_backends.rst).  
An example of a backends shipped externally:

- [jiav-backend-ansible](https://github.com/vkhitrin/jiav-backend-ansible) **this is a risky backend since it allows users to run arbitrary code. Be cautious when enabling it.**
- [jiav-backend-command](https://github.com/vkhitrin/jiav-backend-command) **This is a risky backend since it allows users to run arbitrary code. Be cautious when enabling it.**

## Requirements

`jiav` requires Python `>= 3.8`.

Personal Access Tokens (PATs) are supported [`>=8.14`](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)

## Documentation

Visit <https://jiav.readthedocs.io>.

If you do not have access to a Jira instance or wish to attempt this tool in an isolated environment, refer to [demo](docs/source/demo_try_it_yourself.rst).

## Installation

### Remote

Install from remote using `pip3`:

```bash
pip3 install jiav
```

Install from remote using `pipx`:

```bash
pipx install jiav
```

### Local

Clone the local repository:

```bash
git clone https://github.com/vkhitrin/jiav.git
cd jiav
```

Install using `pip3`:

```bash
pip3 install .
```

Install using `pipx`:

```bash
pipx install .
```

## Usage

After installing this tool `jiav` command is available.

There are several sub-commands available, to view them execute `jiav`:

```bash
usage: jiav [-v | --version] [-d | --debug] <command> [<args>]

Global flags
  -v --version  prints version
  -d --debug   show debug

Available commands
  verify        Verifies issues
  list-backends    List available backends
  validate-manifest  Validate jiav manifest
```

### Verify

Attempt to verify issues from a list of issues:

```bash
jiav --debug verify --jira='<JIRA_URL>' --access-token='<ACCESS_TOKEN>' --issue='<KEY-1>' --issue='<KEY-2>'
```

Attempt to verify issues from a JQL and output the result in JSON format:

```bash
jiav --debug verify --jira='<JIRA_URL>' --access-token='<ACCESS_TOKEN>' --query='issue = "KEY-1"' --format='json'
```

### List backends

List installed backends:

```bash
jiav list-backends
```

### Validate manifest

Validate `jiav` manifest from a file:

```bash
jiav —debug validate-manifest —from-file=/path/to/file
```

## Contributing

**All contributions are welcome!**

To install in development mode, use `poetry`:

```bash
poetry install --with=main,dev
```

If proposing new pull requests, please ensure that new/existing tests are passing:

```bash
pytest
```
