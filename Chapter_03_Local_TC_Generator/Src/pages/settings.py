import streamlit as st
from config_store import load_config, save_config
from jira_client import JiraClient


def render():
    config = load_config()
    st.title("Settings")
    st.write("Configure Jira and LLM settings.")

    with st.form("settings_form"):
        jira_url = st.text_input("Jira URL", value=config.get("jira_url", ""), help="e.g., https://yourworkspace.atlassian.net")
        jira_email = st.text_input("Jira Email", value=config.get("jira_email", ""), help="Email address for Jira account")
        jira_api_token = st.text_input("Jira API Token", value=config.get("jira_api_token", ""), type="password", help="API token from https://id.atlassian.com/manage/api-tokens")
        provider = st.selectbox("LLM Provider", ["ollama", "groq"], index=0 if config.get("llm_provider", "ollama") == "ollama" else 1)
        ollama_url = st.text_input("Ollama URL", value=config.get("ollama_url", "http://localhost:11434"))
        ollama_model = st.text_input("Ollama Model", value=config.get("ollama_model", "gemma3:1b"))
        groq_api_key = st.text_input("Groq API Key", value=config.get("groq_api_key", ""), type="password")
        save = st.form_submit_button("Save Settings")

    if save:
        config.update({
            "jira_url": jira_url,
            "jira_email": jira_email,
            "jira_api_token": jira_api_token,
            "llm_provider": provider,
            "ollama_url": ollama_url,
            "ollama_model": ollama_model,
            "groq_api_key": groq_api_key,
        })
        save_config(config)
        st.success("Settings saved.")

    # Test Jira Connection
    st.divider()
    st.subheader("Test Jira Connection")
    if st.button("Test Connection"):
        try:
            if not jira_url or not jira_email or not jira_api_token:
                st.error("❌ Please fill in Jira URL, Email, and API Token to test connection.")
            else:
                client = JiraClient(jira_url, jira_email, jira_api_token)
                success, message = client.test_connection()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
