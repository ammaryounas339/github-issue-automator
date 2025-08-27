import os
import requests
from dotenv import load_dotenv
from typing import List, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")


class GitHubIssue(BaseModel):
    """Represents a single, actionable GitHub issue."""

    title: str = Field(description="A concise, descriptive title for the issue.")
    body: str = Field(
        description="A detailed description of the task using Markdown. Include context from the report and suggest what needs to be done."
    )
    labels: List[
        Literal[
            "bug",
            "enhancement",
            "student-login",
            "teacher-login",
            "mentor-login",
            "official-login",
            "ui/ux",
            "documentation",
        ]
    ] = Field(description="A list of relevant labels for the issue.")


class IssueList(BaseModel):
    """A list of GitHub issues to be created from the provided text."""

    issues: List[GitHubIssue]


def generate_issues_from_text(problem_description: str):
    """
    Uses Groq and LangChain to parse a problem description into structured GitHub issues.
    """

    llm = ChatGroq(
        temperature=0, model_name="openai/gpt-oss-120b", api_key=GROQ_API_KEY
    )
    structured_llm = llm.with_structured_output(IssueList)

    system_prompt = """
    You are an expert project manager. Your task is to read the following problem description or feedback report
    and break it down into a series of distinct, actionable GitHub issues.

    For each issue, you must generate a concise title, a detailed body in Markdown, and assign relevant labels.
    The labels must be chosen from the provided list.
    Focus on creating one issue for each numbered point in the report under each user login section.
    Aggregate related points into a single issue if it makes sense.
    The issue body should provide enough context for a developer to understand the problem and the required changes.
    """
    human_prompt = "{text}"
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", human_prompt)]
    )
    chain = prompt | structured_llm

    print("Calling Groq LLM to generate issues...")
    response = chain.invoke({"text": problem_description})
    print(f"LLM generated {len(response.issues)} issues.")
    return response.issues


def create_github_issue(repo: str, token: str, issue: GitHubIssue):
    """
    Creates a single issue in the specified GitHub repository.
    """
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "title": issue.title,
        "body": issue.body,
        "labels": issue.labels,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Successfully created issue: '{issue.title}'")
    else:
        print(f"Failed to create issue: '{issue.title}'")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    return response.json()


if __name__ == "__main__":
    problem_statement = """
    Subject: Some quick thoughts on the LearnSphere platform
        Hey team,

        I just spent some time playing around with the new LearnSphere alpha build. It's looking great! I just jotted down a few things that came to mind as I was using it.

        First off, the "Forgot Password" link on the login page seems to be broken. I clicked it and nothing happened.

        On my dashboard, it would be really helpful if the courses I'm enrolled in were sorted by my most recent activity, not alphabetically. Right now I have to search for the course I was just in.

        When I'm watching a video lecture and I close the browser, it doesn't remember my progress. I have to manually find where I left off, which is a bit annoying. Can we have it auto-save the timestamp?

        I tried to update my name in the user profile section, but the "Save Changes" button is greyed out and I can't click it. Seems like a bug.

        Also, just a small content thing, the description for the "Advanced Python" course has a typo. It says "learing" instead of "learning".

        Let me know if you need more details on any of these.

        Keep up the great work!

        Best,
        John 
    """
    generated_issues = generate_issues_from_text(problem_statement)
    if generated_issues:
        print(
            f"\nStarting to create {len(generated_issues)} issues on GitHub repo: {GITHUB_REPO}"
        )
        for issue_to_create in generated_issues:
            create_github_issue(GITHUB_REPO, GITHUB_TOKEN, issue_to_create)
