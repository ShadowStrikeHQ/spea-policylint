import argparse
import json
import logging
import sys

try:
    import yaml
except ImportError:
    print("Please install pyyaml: pip install pyyaml")
    sys.exit(1)

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("Please install jsonschema: pip install jsonschema")
    sys.exit(1)


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="spea-PolicyLint: A tool to lint security policies written in YAML or JSON."
    )
    parser.add_argument(
        "policy_file",
        help="Path to the security policy file (YAML or JSON)."
    )
    parser.add_argument(
        "schema_file",
        help="Path to the JSON schema file."
    )
    parser.add_argument(
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Format of the policy file (yaml or json). Defaults to yaml."
    )
    parser.add_argument(
        "--log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level. Defaults to INFO."
    )
    return parser.parse_args()


def load_policy(policy_file, format="yaml"):
    """
    Loads the security policy from a YAML or JSON file.

    Args:
        policy_file (str): Path to the policy file.
        format (str): Format of the policy file ("yaml" or "json").

    Returns:
        dict: The loaded policy as a dictionary.

    Raises:
        FileNotFoundError: If the policy file does not exist.
        ValueError: If the format is invalid.
        yaml.YAMLError: If there is an error parsing the YAML file.
        json.JSONDecodeError: If there is an error parsing the JSON file.
    """
    try:
        with open(policy_file, "r") as f:
            if format == "yaml":
                try:
                    policy = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    logging.error(f"Error parsing YAML file: {e}")
                    raise
            elif format == "json":
                try:
                    policy = json.load(f)
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing JSON file: {e}")
                    raise
            else:
                raise ValueError("Invalid format. Must be 'yaml' or 'json'.")

        if not isinstance(policy, dict):
             raise ValueError("Policy file must contain a dictionary.")

        return policy

    except FileNotFoundError:
        logging.error(f"Policy file not found: {policy_file}")
        raise
    except ValueError as e:
        logging.error(e)
        raise


def load_schema(schema_file):
    """
    Loads the JSON schema from a file.

    Args:
        schema_file (str): Path to the schema file.

    Returns:
        dict: The loaded schema as a dictionary.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If there is an error parsing the JSON file.
    """
    try:
        with open(schema_file, "r") as f:
            try:
                schema = json.load(f)
            except json.JSONDecodeError as e:
                logging.error(f"Error parsing JSON file: {e}")
                raise
        return schema
    except FileNotFoundError:
        logging.error(f"Schema file not found: {schema_file}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {schema_file}")
        raise


def validate_policy(policy, schema):
    """
    Validates the security policy against the JSON schema.

    Args:
        policy (dict): The security policy to validate.
        schema (dict): The JSON schema to validate against.

    Returns:
        None

    Raises:
        jsonschema.ValidationError: If the policy is invalid according to the schema.
    """
    try:
        validate(instance=policy, schema=schema)
        logging.info("Policy validation successful.")
    except ValidationError as e:
        logging.error(f"Policy validation failed: {e}")
        raise


def main():
    """
    Main function of the spea-PolicyLint tool.
    """
    args = setup_argparse()

    # Set log level based on CLI argument
    logging.getLogger().setLevel(args.log_level)

    try:
        policy = load_policy(args.policy_file, args.format)
        schema = load_schema(args.schema_file)
        validate_policy(policy, schema)
        print("Policy validation successful.")

    except FileNotFoundError:
        print("One or more required files were not found.  See logs for details.")
        sys.exit(1)
    except ValueError:
        print("Invalid input provided.  See logs for details.")
        sys.exit(1)
    except yaml.YAMLError:
        print("Error parsing YAML. See logs for details.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error parsing JSON. See logs for details.")
        sys.exit(1)
    except ValidationError:
        print("Policy validation failed. See logs for details.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("An unexpected error occurred.  See logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()