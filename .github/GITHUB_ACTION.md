# GitHub Action: Generate FSH from FAT API

This repository includes a GitHub Action that allows you to generate FHIR Shorthand (FSH) files from Norwegian FAT API code systems without setting up a local development environment.

## How to Use

1. **Navigate to Actions**
   - Go to the **Actions** tab in this GitHub repository
   - Find the workflow named **"Generate FSH from FAT API"**

2. **Run the Workflow**
   - Click **"Run workflow"**
   - Enter the required inputs:
     - **Code System ID**: Enter a valid FAT API code system ID (e.g., `1101`, `1102`, `7426`)
     - **Include Inactive**: Check this box to include inactive codes (optional)
   - Click **"Run workflow"** to start

3. **Monitor Progress**
   - Watch the workflow execution in real-time
   - View the generated files in the workflow logs
   - Check the workflow summary for details

4. **Download Results**
   - Once completed, scroll down to the **Artifacts** section
   - Download the artifact named `no-kodeverk-{code-system-id}.fsh`
   - The artifact contains a single FSH file (no ZIP extraction needed)
   - File is ready to use immediately

## Benefits

- **No Local Setup**: Run without installing Python or dependencies
- **Quick Testing**: Validate code system conversions easily
- **Single File Download**: Get just the FSH file you need (no ZIP extraction)
- **Ready to Use**: FSH file is immediately usable in your FHIR projects
- **Shareable Results**: Download and share generated FSH files easily
- **Temporary Storage**: Artifacts are kept for 30 days
- **Full Transparency**: View all generated content in workflow logs

## Example Workflow

```yaml
# The action will run with inputs like:
Code System ID: "1101"
Include Inactive: false

# And generate a downloadable file:
no-kodeverk-1101.fsh (single file download)
```

## Use Cases

- **Quick Validation**: Test specific code systems without local setup
- **Collaboration**: Generate FSH files to share with team members
- **CI/CD Integration**: Automate FSH generation in your workflows
- **Documentation**: Create examples and demos easily

## Limitations

- Currently supports FAT API "adm" endpoint only ("Kodeverk i standarder")
- Artifacts expire after 30 days
- Generated files are not committed to the repository
- Requires manual download of artifacts

For local development and automation, consider using the command-line tool directly.
