import subprocess

def get_aws_account_id():
    result = subprocess.run(['aws', 'sts', 'get-caller-identity', '--query', 'Account', '--output', 'text'], capture_output=True, text=True)
    return result.stdout.strip()
