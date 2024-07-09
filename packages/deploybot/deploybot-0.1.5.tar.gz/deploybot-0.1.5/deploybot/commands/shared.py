import subprocess
import os
from deploybot.utils.config import get_config

def git_command(command, cwd, capture_output=True, check=True):
    result = subprocess.run(command, cwd=cwd, capture_output=capture_output, text=True)
    if capture_output:
        print(result.stdout)
    if result.returncode != 0 and check:
        raise subprocess.CalledProcessError(result.returncode, command)
    return result

def pull_latest_changes(base_path):
    try:
        git_command(['git', 'pull'], cwd=base_path)
        print("Git pull successful.")
    except subprocess.CalledProcessError as e:
        print(f"Git pull failed: {e}")
        return False
    return True

def switch_branch(base_path, target_branch):
    try:
        git_command(['git', 'checkout', target_branch], cwd=base_path)
        print(f"Switched to branch: {target_branch}")
    except subprocess.CalledProcessError:
        print(f"Failed to switch to branch: {target_branch}. Stashing changes and retrying...")
        git_command(['git', 'stash'], cwd=base_path)
        git_command(['git', 'checkout', target_branch], cwd=base_path)
        print(f"Switched to branch: {target_branch} after stashing changes.")

    return pull_latest_changes(base_path)

def check_and_switch_branch(environment, base_path):
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=base_path).decode('utf-8').strip()
    target_branch = 'dev' if environment == 'staging' else 'master'

    print(f"Environment: {environment}")
    print(f"Current Branch: {current_branch}")

    if current_branch != target_branch:
        if not switch_branch(base_path, target_branch):
            return False
        current_branch = target_branch
    else:
        # Always pull the latest changes if the branch is correct
        if not pull_latest_changes(base_path):
            return False

    if (environment == 'staging' and current_branch != 'dev') or (environment == 'production' and current_branch != 'master'):
        print(f"Warning: {environment} environment selected but branch is {current_branch}. Exiting.")
        return False

    print(f"Branch check passed for environment {environment} and branch {current_branch}")
    return True

def run_script(script_path, env_vars, base_path):
    script_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)
    subprocess.run(['bash', '-c', f'cd {base_path} && bash {script_dir}/{script_name}'], env=env_vars)

def deploy(service_type, action, service_name):
    print(f"Starting deploy function with action: {action}, service_type: {service_type}, service_name: {service_name}")
    
    if action not in ['build', 'deploy']:
        print("Invalid action. Only 'build' and 'deploy' are supported.")
        return
    
    config = get_config()
    aws_account_id = config['DEFAULT']['aws_account_id']
    environment = config['DEFAULT']['environment']
    base_path = config['DEFAULT']['base_path']
    
    if not aws_account_id or not environment or not base_path:
        print("Configuration not found. Please run 'deploybot configure' first.")
        return

    os.environ['ENVIRONMENT'] = environment
    os.environ['AWS_ACCOUNT_ID'] = aws_account_id

    if environment == 'production':
        env_path = f'{base_path}/service'
    elif environment == 'staging':
        env_path = f'{base_path}/service'
    else:
        print("Invalid environment.")
        return

    if service_type == 'ecs':
        if service_name == 'auth':
            build_script_path = f'{env_path}/auth/api/.buildkite/scripts/docker-build'
            deploy_script_path = f'{env_path}/auth/api/.buildkite/scripts/deploy'
        else:
            build_script_path = f'{env_path}/{service_name}/.buildkite/scripts/docker-build'
            deploy_script_path = f'{env_path}/{service_name}/.buildkite/scripts/deploy'
    elif service_type == 'lambda':
        build_script_path = None
        deploy_script_path = f'{env_path}/lambda/{service_name}/.buildkite/scripts/deploy'
    else:
        print("Invalid service type. Only 'ecs' or 'lambda' are supported.")
        return

    if not check_and_switch_branch(environment, base_path):
        print("Branch check failed. Exiting action.")
        return

    if action == 'build':
        if build_script_path and not os.path.exists(build_script_path):
            print("Build script not found. Please provide the correct service name.")
            return
        if build_script_path:
            print(f"Running build script: {build_script_path}")
            run_script(build_script_path, os.environ, base_path)
        else:
            print("Build action is not supported for lambda services.")
    elif action == 'deploy':
        if build_script_path and not os.path.exists(build_script_path):
            print("Build script not found. Please provide the correct service name.")
            return
        if not os.path.exists(deploy_script_path):
            print("Deploy script not found. Please provide the correct service name.")
            return
        if build_script_path:
            print(f"Running build script: {build_script_path}")
            run_script(build_script_path, os.environ, base_path)
        print(f"Running deploy script: {deploy_script_path}")
        run_script(deploy_script_path, os.environ, base_path)
