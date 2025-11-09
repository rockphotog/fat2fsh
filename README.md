# fat2fsh

UNDER DEVELOPMENT - EXPERIMENTAL

A Python command line tool to download code systems from the FAT API (<https://fat.kote.helsedirektoratet.no>) and convert them to FHIR CodeSystem with FHIR Shorthand (FSH) notation.

## Features

- Download code systems from FAT API endpoint `/api/code-systems/adm/codelist/{id}`
- Convert to FHIR CodeSystem format
- Generate FHIR Shorthand (FSH) notation following Norwegian conventions
- Support for multiple code systems in a single run
- Control active/inactive code inclusion with `--include-inactive` flag
- Save raw JSON data and generated FSH files
- Verbose output option
- Simple setup - no virtual environments required
- Automatic metadata extraction (publisher, dates, OID identifiers)

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

With verbose output and including inactive codes:
```bash
python3 fat2fsh.py -c system1 -c system2 --verbose --include-inactive
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
# Download and convert a code system (active codes only)
python3 fat2fsh.py -c 1101 -v

# Download with inactive codes included
python3 fat2fsh.py -c 1101 --include-inactive -v

# Output:
# ✓ Successfully processed 1101
# Files created:
# - fat/1101.json (complete API response with metadata)
# - fsh/1101.fsh (Norwegian standard FHIR Shorthand format)
```

Generated FSH follows Norwegian conventions:
- CodeSystem: NoKodeverk{id} 
- Id: no-kodeverk-{id}.codesystem
- Canonical URL: http://helsedir.no/fhir/CodeSystem/no-kodeverk-{id}
- OID identifier: urn:oid:2.16.578.1.12.4.1.1.{id}
- Publisher: Helsedirektoratet (from API)
- Date: From API statusLastChanged

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

With optional query parameters:
- `includeInactive=false` - Controls whether inactive codes are included (use `--include-inactive` flag)
