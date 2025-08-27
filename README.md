GitHub Issue Creator from Text 
A simple yet powerful Python script that uses a Large Language Model (LLM) to automatically parse a problem statement, feedback report, or any unstructured text and create well-defined issues in a GitHub repository.

This tool is perfect for project managers, developers, and teams looking to streamline their workflow by converting meeting notes, QA reports, or user feedback directly into actionable development tasks.

✨ Features
AI-Powered Parsing: Leverages the power of Groq's OSS GPT to understand context and break down large documents into individual, actionable issues.

Structured Output: Uses LangChain and Pydantic to force the LLM's output into a clean, structured JSON format, ensuring reliability.

Automatic Labeling: Intelligently assigns relevant labels (e.g., bug, enhancement, ui/ux) to each issue.

GitHub Integration: Seamlessly creates issues in your specified GitHub repository using the GitHub REST API.

Easy to Configure: Requires minimal setup with a simple .env file for your API keys and repository name.

⚙️ How It Works
The workflow is straightforward:

Input: You provide a block of text (the "problem statement") to the script.

Prompting: The script wraps your text in a carefully crafted prompt that instructs the LLM to act as a project manager.

LLM Processing: The prompt is sent to the Groq API. The LLM analyzes the text and generates a list of issues in a structured JSON format, complete with titles, detailed bodies, and appropriate labels.

Issue Creation: The script iterates through the JSON response and makes API calls to GitHub to create each issue in your repository.

!

🚀 Setup and Installation
Follow these steps to get the project up and running.

1. Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

4. Configure Environment Variables
You'll need to provide API keys for Groq and GitHub.

Create a file named .env in the root of your project directory.

Add the following content to the file, replacing the placeholder values with your actual credentials:

# .env file

# Get your Groq API Key from https://console.groq.com/keys
GROQ_API_KEY="gsk_YourGroqApiKey"

# Generate a GitHub Personal Access Token with 'repo' scope
# https://github.com/settings/tokens
GITHUB_TOKEN="ghp_YourGitHubPersonalAccessToken"

# The full name of your target repository (e.g., "codeforpakistan/tarbiyat")
GITHUB_REPO="your-username/your-repo-name"

🛠️ Usage
Once the setup is complete, running the script is simple.

Open the Python script (main.py or your script's name).

Paste your problem statement or feedback text into the problem_statement variable within the if __name__ == "__main__": block.

Run the script from your terminal:

python main.py

The script will then connect to the Groq API, generate the issues, and post them to your configured GitHub repository. You'll see progress and success messages printed in your terminal.

📝 Customization
Changing the LLM
You can easily switch to a different model supported by Groq by changing the model_name in the script:

# In the generate_issues_from_text function
llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768", api_key=GROQ_API_KEY)

Adjusting Issue Labels
To add, remove, or change the available labels, modify the Literal type hint in the GitHubIssue Pydantic model:

# In the GitHubIssue class definition
class GitHubIssue(BaseModel):
    # ...
    labels: List[Literal["bug", "feature-request", "refactor", "testing"]]
