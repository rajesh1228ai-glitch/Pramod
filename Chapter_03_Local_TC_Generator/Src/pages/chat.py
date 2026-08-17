import streamlit as st
from config_store import load_config
from jira_client import JiraClient
from llm_client import LLMClient
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def load_template() -> str:
    template_file = TEMPLATES_DIR / "testcase_template.txt"
    if template_file.exists():
        return template_file.read_text(encoding="utf-8")
    return "Create test cases from Jira issue summary and description.\n"


def build_prompt(issue_key: str, issue_data: dict[str, str], template: str) -> str:
    summary = issue_data.get("summary", "")
    description = issue_data.get("description", "")
    return (
        f"You are a QA automation tester. Generate a structured test case draft for Jira ticket {issue_key}.\n"
        f"Summary:\n{summary}\n\n"
        f"Description:\n{description}\n\n"
        f"Template:\n{template}\n\n"
        "Produce a clear, numbered test plan and related test cases."
    )


def render_chat(messages: list[dict[str, str]]) -> None:
    for message in messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")


def render() -> None:
    config = load_config()

    st.title("Jira Test Case Generator")
    st.write("Enter a Jira ticket key or ask for test cases for a Jira ID.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Show available issues in sidebar
    with st.sidebar:
        st.subheader("Jira Projects & Issues")
        st.write("Manage your Jira search")
        
        # Show available projects
        if st.button("📂 Show Available Projects"):
            try:
                jira = JiraClient(config.get("jira_url", ""), config.get("jira_email", ""), config.get("jira_api_token", ""))
                with st.spinner("Loading projects..."):
                    projects = jira.list_projects()
                    if projects:
                        st.success(f"Found {len(projects)} projects:")
                        for project in projects:
                            st.write(f"🔑 **{project['key']}**: {project['name']}")
                    else:
                        st.info("No projects found. Check your Jira credentials.")
            except Exception as e:
                st.error(f"Failed to list projects: {str(e)}")
        
        st.divider()
        st.subheader("Issue Search")
        st.write("Search for issues in your Jira workspace")
        
        # Input for project or issue key
        search_input = st.text_input(
            "Project Key or Issue Key",
            placeholder="e.g., KAN or KAN-150",
            help="Enter project key (KAN) or issue key (KAN-150) to search"
        )
        
        if st.button("🔍 Search Issues"):
            if not search_input:
                st.warning("Please enter a project or issue key")
            else:
                try:
                    jira = JiraClient(config.get("jira_url", ""), config.get("jira_email", ""), config.get("jira_api_token", ""))
                    with st.spinner("Searching for issues..."):
                        issues = jira.search_issues(project_key=search_input, limit=10)
                        if issues:
                            st.success(f"Found {len(issues)} issues:")
                            for issue in issues:
                                st.write(f"📋 **{issue['key']}**: {issue['summary']}")
                        else:
                            st.info("No issues found. Check your project key.")
                except Exception as e:
                    st.error(f"Search failed: {str(e)}")

    prompt_input = st.text_input("Message", key="prompt_input")
    submit = st.button("Send")

    if submit and prompt_input:
        st.session_state["messages"].append({"role": "user", "content": prompt_input})
        issue_key = prompt_input.strip().split()[-1].upper()

        try:
            jira = JiraClient(config.get("jira_url", ""), config.get("jira_email", ""), config.get("jira_api_token", ""))
            issue = jira.get_issue(issue_key)
            issue_data = jira.extract_issue_data(issue)
            template = load_template()
            prompt_text = build_prompt(issue_key, issue_data, template)
            llm = LLMClient(config)
            provider, response_text = llm.generate(prompt_text)
            answer = f"(via {provider})\n\n{response_text}"
        except Exception as exc:
            answer = f"Error: {exc}"

        st.session_state["messages"].append({"role": "assistant", "content": answer})

    render_chat(st.session_state["messages"])
