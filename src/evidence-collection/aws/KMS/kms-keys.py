import os
import subprocess
import datetime
import json

# Set the current year
current_year = datetime.datetime.now().year

# Environment configurations
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/aws_kms_evidence.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/aws_kms_evidence.json"
    }
}

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.splitlines()

# Process each environment
for env_name, config in environments.items():
    # Set the environment variables for AWS credentials
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']
    
    # Prepare output data
    output = []
    
    # Commands to execute
    commands = [
        ['aws', 'kms', 'list-keys', '--region', config['region'], '--output', 'json'],
        ['aws', 'kms', 'list-key-rotations', '--region', config['region'], '--output', 'json'],
        ['aws', 'kms', 'list-key-policies', '--region', config['region'], '--output', 'json']
    ]
    
    # Run commands and collect output
    for command in commands:
        output.append(run_command(' '.join(command)))

    # Determine the output file based on environment
    output_file = config.get(f"{env_name}_output_file", "")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the output to a file
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("KMS evidence generation complete.")