# fat2fsh

A Python command line tool to download code systems from the FAT API (<https://fat.kote.helsedirektoratet.no>) and convert them to FHIR CodeSystem with FHIR Shorthand (FSH) notation.

## Features

- Download code systems from FAT API endpoint `/api/code-systems/adm/codelist/{id}`
- Convert to FHIR CodeSystem format
- Generate FHIR Shorthand (FSH) notation
- Support for multiple code systems in a single run
- Save raw JSON data and generated FSH files
- Verbose output option
- Simple setup - no virtual environments required

## Setup

Install dependencies directly to your system Python:

```bash
./setup.sh
```

## Usage

Basic usage:
```bash
python3 fat2fsh.py -c <code-system-id>
```

Download multiple code systems:
```bash
python3 fat2fsh.py -c system1 -c system2 -c system3
```

With verbose output:
```bash
python3 fat2fsh.py -c system1 -c system2 --verbose
```

Specify output directory:
```bash
python3 fat2fsh.py -c system1 --output-dir /path/to/output
```

Get help:
```bash
python3 fat2fsh.py --help
```

## Output

The tool creates two directories:
- `fat/` - Contains the raw JSON data downloaded from the FAT API
- `fsh/` - Contains the generated FHIR Shorthand (.fsh) files

## Example

```bash
# Download and convert a code system
python3 fat2fsh.py -c example-system -v

# Output:
# ✓ Successfully processed example-system
# Files created:
# - fat/example-system.json
# - fsh/example-system.fsh
```

## Dependencies

- Python 3.7+
- requests - For HTTP API calls
- click - For command line interface
- pydantic - For data validation and parsing

## API Endpoint

The tool uses the FAT API endpoint:
```
https://fat.kote.helsedirektoratet.no/api/code-systems/adm/codelist/{id}
```
