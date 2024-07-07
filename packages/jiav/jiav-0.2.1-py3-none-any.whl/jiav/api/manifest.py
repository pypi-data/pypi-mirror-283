#!/usr/bin/env python

import jsonschema
import jsonschema.exceptions
import yaml
import yaml.composer
import yaml.parser
import yaml.scanner

import jiav.api.backends
import jiav.constants
from jiav import exceptions, logger
from jiav.api.schemas.jiav import schema as jiav_schema
from jiav.api.schemas.verification_step import schema as step_schema

jiav_logger = logger.subscribe_to_logger()


class Manifest(object):
    """
    A jiav Manifest Execution

    Attributes:
        manifest           - Manifest
        successful         - Result of manifest execution
        verified_status    - Jira status to transition to
        verification_steps - Verification steps to perform
        backend_steps      - Parsed backend steps to execute
    """

    def __init__(self, manifest):
        self.manifest = manifest
        self.successful = True  # Will stay true unless failed
        self.execution_output = None
        self.verified_status = str()
        self.verification_steps = list()
        self.backend_steps = list()

    def backend_is_valid(self, backend=jiav.api.backends.BaseBackend()):
        """
        Validates requested backend

        Params:
            backend - Requested backend

        Returns a boolean representing if requested backend is valid
        """
        return backend in jiav.constants.EXPOSED_BACKENDS

    def validate_verification_step(self, step=dict({})):
        """
        Validates verification step

        Arguments:
            step - Verification step

        Returns True if successfully validated verification step
        """
        verified_backend = step.get("backend")
        backend_class = jiav.constants.EXPOSED_BACKENDS[verified_backend]
        # Construct initial class
        backend_instance = backend_class()
        # Remove unnecessary keys for schema validation
        del step["backend"]
        del step["name"]
        backend_instance.step = step
        # Validate backend schema
        backend_instance.validate_schema()
        self.backend_steps.append(backend_instance)
        return True

    def execute_manifest(self):
        """
        Executes manifest

        Returns:
            execution_output - jiav manifest execution output
        """
        # Init variables
        execution_output = list()
        # Iterate over steps in manifest
        for step in self.backend_steps:
            jiav_logger.debug("Executing backend '{}'".format(step.name))
            execution_output.append("Output of backend '{}':\n".format(step.name))
            step.execute_backend()
            if step.result.successful:
                execution_output.append(step.result.output)
            # If one of the steps failed, immediately fail and don't continue
            else:
                self.successful = False
                # If stderr contains output, log it
                if step.result.errors:
                    execution_output.append(step.result.errors)
                else:
                    execution_output.append(step.result.output)
                break
        self.execution_output = execution_output
        if self.successful:
            jiav_logger.info("Manifest was executed successfully")
        else:
            jiav_logger.error("Manifest has failed to execute")


def validiate_text_contains_manifest(manifest=str()):
    """
    Performs initial validation of text, checks if text is a valid
    manifest

    Arguments:
        manifest - Text parsed from comment

    Returns a JSON object if initial manifest has passed schema validation
    """
    # Attempt to parse YAML from comment
    try:
        manifest = yaml.safe_load(manifest)
    except yaml.scanner.ScannerError as e:
        raise exceptions.InvalidYAMLException(e)
    except yaml.parser.ParserError as e:
        raise exceptions.InvalidYAMLException(e)
    except yaml.composer.ComposerError as e:
        raise exceptions.InvalidYAMLException(e)
    # Attempt to validate YAML according to schema
    try:
        jsonschema.validate(instance=manifest, schema=jiav_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise exceptions.InvalidManifestException(e) from None
    return manifest["jiav"]


def validate_verifications_steps(manifest_obj=type(Manifest)):
    """
    Validates verification_steps from jiav manifest

    Arguments:
        manifest_obj - jiav.api.manifest.Manifest object
    """
    steps = manifest_obj.verification_steps
    # Iterate over steps in manifest
    for step in steps:
        step_backend = step.get("backend")
        # Attempt to validate step according to schema
        try:
            jsonschema.validate(instance=step, schema=step_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.InvalidManifestException(e)

        if not manifest_obj.backend_is_valid(step_backend):
            raise exceptions.InvalidBackend(step_backend)
        manifest_obj.validate_verification_step(step)


def validate_manifest(text=type(str)):
    """
    Attempt to validate manifest from text

    Arguments:
        text - Text containing potential manifest

    Returns:
        manifest - jiav.api.manifest.Manifest object
    """
    # Attempt to validate initial manifest
    try:
        # If manifest is verified, create Manifest object
        manifest = Manifest(validiate_text_contains_manifest(manifest=text))
        # Update manifest attributes based on validated manifest
        manifest.verified_status = manifest.manifest.get("verified_status")
        manifest.verification_steps = manifest.manifest.get("verification_steps")
        # Validate verification steps
        try:
            validate_verifications_steps(manifest_obj=manifest)
        except exceptions.InvalidManifestException as e:
            jiav_logger.debug(e)
            manifest = False
        except exceptions.InvalidBackend as e:
            jiav_logger.debug(e)
            manifest = False
    except exceptions.InvalidYAMLException:
        manifest = False
        jiav_logger.debug("No valid YAML was found in comment")
    return manifest
