# Deploybot

Deploybot is a command-line interface (CLI) tool designed to deploy ECS and Lambda services. It allows users to configure their AWS account and environment, and then build and deploy services with ease.

## Prerequisites

* Python 3.6 or higher
* [Poetry](https://python-poetry.org/) for dependency management
* AWS CLI configured with the necessary credentials

## Installation




1. Clone the repository:

   ```bash
   git clone git@github.com:respond-io/deploybot-cli.git
   cd deploybot-cli
   ```
2. Install dependencies using Poetry:

   ```bash
   poetry install
   
   Run all commands in poetry shell run bellow command
   
   poetry shell
   ```

## Configuration

Before using Deploybot, you need to configure it with your AWS account ID, environment, and base path.




1. Run the configure command:

   ```bash
   deploybot configure
   
   ```

   Follow the prompts to enter your AWS account ID, select the environment (staging or production), and provide the base path to your services.

   Example:

   ```bash
   Enter your AWS account ID: 123456789012
   Select environment: [staging, production]: staging
   Enter the base path: /home/ubuntu/staging (for example)
   ```

## Usage

Deploybot supports two main commands: `ecs` and `lambda`.

### Deploying ECS Services




1. Build and deploy an ECS service:

   ```bash
   deploybot ecs deploy <service_name>
   ```

   Example:

   ```bash
   deploybot ecs deploy auth
   ```
2. Build an ECS service:

   ```bash
   deploybot ecs build <service_name>
   ```

   Example:

   ```bash
   deploybot ecs build auth
   ```

### Deploying Lambda Services




1. Deploy a Lambda service:

   ```bash
   deploybot lambda deploy <service_name>
   ```

   Example:

   ```bash
   deploybot lambda deploy data-export
   ```



## Testing

To run the tests, use the following command:

```bash
pytest  tests/test_*.py
```


