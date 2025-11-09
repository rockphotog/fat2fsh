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
# Run the converter with one or more code system IDs
python3 fat2fsh.py -c <code-system-id> --verbose

# Example with multiple systems
python3 fat2fsh.py -c system1 -c system2 -c system3 -v
```

## 3. Finding Code System IDs

To find available code system IDs, you need to:

1. Visit the FAT API documentation at https://fat.kote.helsedirektoratet.no/index.html
2. Look for the `/api/code-systems/adm/codelist/` endpoint
3. Find the available code system IDs from the API documentation or by exploring the API

## 4. Example Workflow

```bash
# Download and convert a code system
python3 fat2fsh.py -c example-system -v

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
- Test the installation: `python3 test_setup.py`

## 7. Getting Help

```bash
# Show command line help
python3 fat2fsh.py --help

# Test the setup
python3 test_setup.py
```