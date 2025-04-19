# spea-PolicyLint
A command-line tool to lint security policies written in YAML or JSON format, checking for common errors like missing fields, invalid values, and potential contradictions based on a user-defined schema. - Focused on Validates configurations (JSON, YAML) against defined security policies (expressed as JSON Schema). Detects deviations from the policy, providing detailed reports highlighting non-compliant settings.  Supports customizable policy sets for various security standards (e.g., CIS benchmarks, NIST guidelines).

## Install
`git clone https://github.com/ShadowStrikeHQ/spea-policylint`

## Usage
`./spea-policylint [params]`

## Parameters
- `-h`: Show help message and exit
- `--format`: No description provided
- `--log_level`: Set the logging level. Defaults to INFO.

## License
Copyright (c) ShadowStrikeHQ
