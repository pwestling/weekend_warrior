import os
import time
import argparse
import requests
from datetime import datetime, timedelta
from typing import List

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

def get_pull_requests(owner: str, repo: str) -> List[dict]:
    query = """
    query($repo: String!, $owner: String!) {
        repository(name: $repo, owner: $owner) {
            pullRequests(first: 100, states: OPEN) {
                nodes {
                    id
                    number
                    title
                    createdAt
                    reviews(first: 10) {
                        nodes {
                            state
                        }
                    }
                    author {
                        login
                    }
                }
            }
        }
    }
    """
    variables = {"repo": repo, "owner": owner}
    response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=HEADERS)
    if response.status_code == 200:
        return response.json()['data']['repository']['pullRequests']['nodes']
    else:
        raise Exception(f"Query failed to run with a {response.status_code}")

def approve_pull_request(pull_request_id: str) -> None:
    mutation = """
    mutation($pullRequestId: ID!) {
        addPullRequestReview(input: {pullRequestId: $pullRequestId, event: APPROVE}) {
            clientMutationId
        }
    }
    """
    variables = {"pullRequestId": pull_request_id}
    response = requests.post('https://api.github.com/graphql', json={'mutation': mutation, 'variables': variables}, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Mutation failed to run with a {response.status_code}")

def is_approved(reviews: List[dict]) -> bool:
    return any(review['state'] == 'APPROVED' for review in reviews)


def main(repo: str, authors: List[str], minutes_old: int, dry_run: bool = False) -> None:
    while True:
        owner, repo = repo.split('/')
        pull_requests = get_pull_requests(owner, repo)
        for pr in pull_requests:
            if pr['author']['login'] in authors:
                pr_created_at = datetime.strptime(pr['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
                if datetime.utcnow() - pr_created_at > timedelta(minutes=minutes_old) and not is_approved(pr['reviews']['nodes']):
                    if not dry_run:
                        approve_pull_request(pr['id'])
                        print(f"Approved PR #{pr['number']} '{pr['title']}' by {pr['author']['login']}")
                    else:
                        print(f"Would have approved PR #{pr['number']} '{pr['title']}' by {pr['author']['login']}")
        time.sleep(60)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically approve GitHub pull requests.")
    parser.add_argument("repo", type=str, help="GitHub repository in the format 'owner/repo'")
    parser.add_argument("authors", nargs='+', help="List of GitHub usernames")
    parser.add_argument("minutes_old", type=int, help="Age of the pull request in minutes to auto-approve")
    # add dry run boolean arg for testing
    parser.add_argument("--dry-run", action="store_true", help="Dry run - don't actually approve the pull request")


    args = parser.parse_args()

    main(args.repo, args.authors, args.minutes_old, args.dry_run)
