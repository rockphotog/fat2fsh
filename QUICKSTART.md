# Quick Start Guide for fat2fsh

## 1. Initial Setup (One-time)

```bash
# Clone or navigate to the project directory
cd fat2fsh

# Run the setup script
./setup.sh
```

## 2. Daily Usage

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the converter with one or more code system IDs
python fat2fsh.py -c <code-system-id> --verbose

# Example with multiple systems
python fat2fsh.py -c system1 -c system2 -c system3 -v

# When done, deactivate the virtual environment
deactivate
```

## 3. Finding Code System IDs

To find available code system IDs, you need to:

1. Visit the FAT API documentation at https://fat.kote.helsedirektoratet.no/index.html
2. Look for the `/api/code-systems/adm/codelist/` endpoint
3. Find the available code system IDs from the API documentation or by exploring the API

## 4. Example Workflow

```bash
# Activate environment
source venv/bin/activate

# Download and convert a code system
python fat2fsh.py -c example-system -v

# Check the results
ls fat/        # Raw JSON files
ls fsh/        # Generated FSH files

# View a generated FSH file
cat fsh/example-system.fsh
```

## 5. Output Structure

After running the tool, you'll have:

```
fat2fsh/
├── fat/                    # Raw JSON data from FAT API
│   └── system-id.json
├── fsh/                    # Generated FSH files
│   └── system-id.fsh
└── ...
```

## 6. Troubleshooting

### Connection Issues
- Ensure you have internet connectivity
- Check if the FAT API is accessible: https://fat.kote.helsedirektoratet.no

### Invalid Code System ID
- Verify the code system ID exists in the FAT API
- Check the API documentation for available systems

### Permission Issues
- Ensure you have write permissions in the current directory
- Try using a different output directory with `-o /path/to/output`

### Python Environment Issues
- Re-run the setup script: `./setup.sh`
- Manually activate the virtual environment: `source venv/bin/activate`

## 7. Getting Help

```bash
# Show command line help
python fat2fsh.py --help

# Test the setup
python test_setup.py
```