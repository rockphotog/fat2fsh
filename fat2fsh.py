#!/usr/bin/env python3
"""
fat2fsh - Convert FAT API code systems to FHIR FSH notation.

A command-line tool to download Norwegian code systems from the FAT API
and convert them to FHIR Shorthand (FSH) notation following Norwegian standards.
"""

import json
from pathlib import Path
from typing import List, Optional
import click
import requests
from pydantic import BaseModel, Field


class CodeSystemConcept(BaseModel):
    """Represents a concept in a code system."""
    code: str
    display: str
    definition: Optional[str] = None
    
    
class FATCodeSystem(BaseModel):
    """Represents a code system from the FAT API."""
    id: str
    name: str
    title: str
    description: Optional[str] = None
    version: Optional[str] = None
    status: Optional[str] = None
    status_last_changed: Optional[str] = None
    owner: Optional[str] = None
    valid_from: Optional[str] = None
    active: Optional[bool] = None
    concepts: List[CodeSystemConcept] = Field(default_factory=list)


class FATAPIClient:
    """Client for interacting with the FAT API."""
    
    def __init__(self, base_url: str = "https://fat.kote.helsedirektoratet.no"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'fat2fsh-converter/1.0.0',
            'Accept': 'application/json'
        })
    
    def get_code_system(self, code_system_id: str, include_inactive: bool = False) -> FATCodeSystem:
        """Download a code system from the FAT API."""
        url = f"{self.base_url}/api/code-systems/adm/codelist/{code_system_id}"
        
        # Add query parameters
        params = {
            'includeInactive': str(include_inactive).lower()
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                raise ValueError(f"Empty response from API for code system {code_system_id}")
            
            # Parse the response and create FATCodeSystem object
            code_system = FATCodeSystem(
                id=code_system_id,
                name=data.get('name', code_system_id),
                title=data.get('title', data.get('name', code_system_id)),
                description=data.get('description'),
                version=data.get('version', '1.0.0'),
                status=data.get('status'),
                status_last_changed=data.get('statusLastChanged'),
                owner=data.get('owner', {}).get('name') if data.get('owner') else None,
                valid_from=data.get('validFrom'),
                active=data.get('active')
            )
            
            # Parse concepts/codes
            concepts = []
            if 'codeValues' in data:
                for code_data in data['codeValues']:
                    concept = CodeSystemConcept(
                        code=code_data.get('value', code_data.get('id', '')),
                        display=code_data.get('name', ''),
                        definition=code_data.get('description', '')
                    )
                    concepts.append(concept)
            elif 'codes' in data:
                for code_data in data['codes']:
                    concept = CodeSystemConcept(
                        code=code_data.get('code', ''),
                        display=code_data.get('display', code_data.get('name', '')),
                        definition=code_data.get('definition', code_data.get('description'))
                    )
                    concepts.append(concept)
            elif 'concepts' in data:
                for concept_data in data['concepts']:
                    concept = CodeSystemConcept(
                        code=concept_data.get('code', ''),
                        display=concept_data.get('display', concept_data.get('name', '')),
                        definition=concept_data.get('definition', concept_data.get('description'))
                    )
                    concepts.append(concept)
            
            code_system.concepts = concepts
            return code_system
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API error for {code_system_id}: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parse error for {code_system_id}: {e}")


class FSHGenerator:
    """Generates FHIR Shorthand (FSH) notation from FAT code systems."""
    
    @staticmethod
    def generate_fsh(code_system: FATCodeSystem) -> str:
        """Generate FSH notation for a code system in Norwegian standard format."""
        fsh_content = []
        
        # CodeSystem header following Norwegian conventions
        code_system_name = f"NoKodeverk{code_system.id}"
        code_system_id = f"no-kodeverk-{code_system.id}.codesystem"
        
        fsh_content.append(f"CodeSystem: {code_system_name}")
        fsh_content.append(f"Id: {code_system_id}")
        fsh_content.append(f"Title: \"{code_system.id} {code_system.title}\"")
        
        if code_system.description:
            fsh_content.append(f"Description: \"{code_system.description}\"")
        
        # Add canonical URL
        canonical_url = f"http://helsedir.no/fhir/CodeSystem/no-kodeverk-{code_system.id}"
        fsh_content.append(f"* ^url = \"{canonical_url}\"")
        
        # Add identifier with OID
        fsh_content.append("* ^identifier.system = \"urn:ietf:rfc:3986\"")
        oid = f"urn:oid:2.16.578.1.12.4.1.1.{code_system.id}"
        fsh_content.append(f"* ^identifier.value = \"{oid}\"")
        
        # Status and dates
        fsh_content.append("* ^status = #active")
        
        # Add date from statusLastChanged if available
        if code_system.status_last_changed:
            # Extract date part from ISO datetime
            date_part = code_system.status_last_changed.split('T')[0]
            fsh_content.append(f"* ^date = \"{date_part}\"")
        
        # Add publisher
        if code_system.owner:
            fsh_content.append(f"* ^publisher = \"{code_system.owner}\"")
        
        fsh_content.append("* ^content = #complete")
        fsh_content.append("")
        
        # Add concepts (only active ones by default)
        for concept in code_system.concepts:
            if concept.code and concept.display:
                fsh_content.append(f"* #{concept.code} \"{concept.display}\"")
                if concept.definition and concept.definition.strip():
                    fsh_content.append(f"  * ^definition = \"{concept.definition}\"")
        
        return "\n".join(fsh_content)


@click.command()
@click.option(
    '--code-systems', '-c',
    multiple=True,
    required=True,
    help='Code system IDs to download (can be specified multiple times)'
)
@click.option(
    '--output-dir', '-o',
    default='.',
    help='Output directory (default: current directory)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output'
)
@click.option(
    '--include-inactive',
    is_flag=True,
    default=False,
    help='Include inactive codes in the download'
)
def main(code_systems: tuple, output_dir: str, verbose: bool, include_inactive: bool):
    """
    Download code systems from the FAT API and convert them to FHIR CodeSystem with FSH notation.
    
    Example usage:
    
        python fat2fsh.py -c system1 -c system2
        
        python fat2fsh.py --code-systems system1 --code-systems system2 --output-dir /path/to/output
    """
    output_path = Path(output_dir)
    fat_dir = output_path / "fat"
    fsh_dir = output_path / "fsh"
    
    # Create output directories
    fat_dir.mkdir(parents=True, exist_ok=True)
    fsh_dir.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        click.echo(f"Output directory: {output_path.absolute()}")
        click.echo(f"FAT data will be saved to: {fat_dir.absolute()}")
        click.echo(f"FSH files will be saved to: {fsh_dir.absolute()}")
    
    # Initialize API client and FSH generator
    api_client = FATAPIClient()
    fsh_generator = FSHGenerator()
    
    for code_system_id in code_systems:
        if verbose:
            click.echo(f"\nProcessing code system: {code_system_id}")
        
        try:
            # Download code system from FAT API
            code_system = api_client.get_code_system(code_system_id, include_inactive)
            
            # Save raw JSON data
            fat_file = fat_dir / f"{code_system_id}.json"
            with open(fat_file, 'w', encoding='utf-8') as f:
                json.dump(code_system.model_dump(), f, indent=2, ensure_ascii=False)
            
            if verbose:
                click.echo(f"  Saved FAT data to: {fat_file}")
            
            # Generate and save FSH
            fsh_content = fsh_generator.generate_fsh(code_system)
            fsh_file = fsh_dir / f"no-kodeverk-{code_system_id}.fsh"
            
            with open(fsh_file, 'w', encoding='utf-8') as f:
                f.write(fsh_content)
            
            if verbose:
                click.echo(f"  Generated FSH file: {fsh_file}")
                click.echo(f"  Concepts found: {len(code_system.concepts)}")
            
            click.echo(f"✓ Successfully processed {code_system_id}")
            
        except Exception as e:
            click.echo(f"✗ Failed to process {code_system_id}: {e}", err=True)
            if verbose:
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    main()