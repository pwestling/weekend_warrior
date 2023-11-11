# Weekend Warrior

Weekend Warrior is a Python script that automates the approval of GitHub pull requests. It queries a specified repository for open pull requests by given authors, and if the pull requests are older than a specified time, it automatically approves them.

## Installation

To install and run Weekend Warrior, you need to have Poetry installed on your system. If you don't have Poetry, you can install it by following the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

Once Poetry is installed, follow these steps:

1. **Clone the repository**: Clone this repository to your local machine using:

   ```
   git clone https://github.com/pwestling/weekend_warrior.git
   cd weekend_warrior
   ```

2. **Install dependencies**: Run the following command to install the necessary dependencies:

   ```
   poetry install
   ```

## Configuration

Before running the script, you need to set up a GitHub token:

1. **Generate a GitHub token**: Follow the instructions on [GitHub's documentation](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) to create a personal access token. Ensure you grant the necessary permissions to the token for managing pull requests.

2. **Set up environment variable**: Set the generated GitHub token as an environment variable. This can be done by adding the following line to your `.bashrc`, `.zshrc`, or equivalent shell configuration file:

   ```
   export GITHUB_TOKEN='your_github_token_here'
   ```

   Replace `your_github_token_here` with your actual GitHub token.

## Usage

To run the script, use the following command:

```
poetry run python weekend_warrior.py <owner/repo> "<author>" <minutes_old>
```

Replace `<owner/repo>` with the GitHub repository in the format 'owner/repo', `<author>` with the GitHub username of the author whose pull requests you want to check, and `<minutes_old>` with the age of the pull request in minutes for auto-approval.

For example:

```
poetry run python weekend_warrior.py owner/repo "author" 10
```

This will monitor the specified repository and automatically approve pull requests from the specified author that are at least 10 minutes old.
