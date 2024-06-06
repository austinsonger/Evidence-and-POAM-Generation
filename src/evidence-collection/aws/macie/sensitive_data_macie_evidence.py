import os
import subprocess
import datetime
import json

# Define the current year
current_year = datetime.datetime.now().year

# Setup environments dictionary with AWS credentials and output file paths
environments = {
    'commercial': {
        'access_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_CORP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'commercial_output_file': f"/evidence-artifacts/{current_year}/commercial/macie_data_monitoring.json"
    },
    'federal': {
        'access_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('DEVOPS_DOOP_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
        'region': 'us-east-1',
        'federal_output_file': f"/evidence-artifacts/{current_year}/federal/macie_data_monitoring.json"
    }
}

# Function to run shell commands and capture the output
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    if result.returncode == 0:
        return result.stdout.strip().split('\n')
    else:
        raise Exception(f"Command failed: {result.stderr}")

# Iterate over each environment to set credentials and generate output
for env_name, config in environments.items():
    # Set the AWS credentials for the current environment
    os.environ['AWS_ACCESS_KEY_ID'] = config['access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = config['secret_key']
    os.environ['AWS_DEFAULT_REGION'] = config['region']

    # AWS CLI command to list all Macie classification jobs
    macie_command = [
        'aws', 'macie2', 'list-classification-jobs',
        '--region', config['region'],
        '--output', 'json'
    ]

    # Run the AWS CLI command to gather information about Macie classification jobs
    macie_info = run_command(macie_command)
    macie_data = json.loads(macie_info[0])

    # Initialize an empty list to store JSON output
    output = [{"Macie_Classification_Jobs": macie_data}]

    # Determine the output file based on environment
    output_file = config.get(f"{env_name}_output_file")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the JSON output to the specified file path
    with open(output_file, 'w') as file:
        json.dump(output, file, indent=4)

print("Macie data monitoring evidence files generated successfully.")
