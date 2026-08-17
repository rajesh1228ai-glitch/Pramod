import base64
import requests
from typing import Any
from urllib.parse import quote_plus


class JiraClient:
    def __init__(self, base_url: str, email: str, api_token: str) -> None:
        # Validate and normalize the base URL
        self.base_url = self._validate_jira_url(base_url).rstrip("/")
        self.email = email
        self.api_token = api_token
        self.auth_header = self._build_auth_header()

    def _validate_jira_url(self, url: str) -> str:
        """Validate and normalize Jira URL"""
        url = url.strip()
        if not url:
            raise ValueError("Jira URL cannot be empty")
        
        # Remove /browse/*, /jira/software/projects, and other paths if present
        if "/browse/" in url:
            url = url.split("/browse/")[0]
        if "/jira/" in url:
            url = url.split("/jira/")[0]
        
        # Ensure URL starts with https://
        if not url.startswith("http"):
            url = "https://" + url
        
        # Validate Jira Cloud URL format
        if not url.endswith(".atlassian.net"):
            raise ValueError(f"Invalid Jira Cloud URL. Expected URL like 'https://yourworkspace.atlassian.net', got: {url}")
        
        return url

    def _build_auth_header(self) -> dict[str, str]:
        token = f"{self.email}:{self.api_token}"
        encoded = base64.b64encode(token.encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {encoded}", "Content-Type": "application/json"}

    def get_issue(self, issue_key: str) -> dict[str, Any]:
        # Normalize issue key to uppercase
        issue_key = issue_key.strip().upper()
        if not issue_key:
            raise ValueError("Issue key cannot be empty")
        
        url = f"{self.base_url}/rest/api/3/issue/{quote_plus(issue_key)}"
        try:
            response = requests.get(url, headers=self.auth_header, params={"fields": "summary,description"}, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Timeout connecting to Jira at {self.base_url}. Check your network connection and Jira URL.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"Cannot connect to Jira at {self.base_url}. Check your Jira URL is correct.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise RuntimeError("Authentication failed. Check your Jira email and API token.")
            elif response.status_code == 403:
                raise RuntimeError("Access forbidden. Check if your API token has permission to access this issue.")
            elif response.status_code == 404:
                raise RuntimeError(
                    f"Issue '{issue_key}' not found in Jira.\n"
                    f"Please verify:\n"
                    f"1. Issue key is correct (e.g., KAN-150)\n"
                    f"2. Issue exists in your Jira workspace\n"
                    f"3. Your API token has access to the issue"
                )
            raise RuntimeError(f"Jira API error: {response.status_code} {response.reason}")
        
        if self._is_json(response):
            try:
                return response.json()
            except ValueError:
                raise RuntimeError(f"Jira returned invalid JSON for issue {issue_key}: {response.text[:500]}")
        
        # Detect if we got HTML (common when auth fails)
        if response.text.strip().startswith("<"):
            raise RuntimeError(
                f"Received HTML from Jira instead of JSON. This usually means:\n"
                f"1. Authentication failed (invalid email or API token)\n"
                f"2. Jira URL is incorrect\n"
                f"Please check your Jira settings.\n"
                f"Response: {response.text[:200]}"
            )
        
        raise RuntimeError(f"Jira returned a non-JSON response for issue {issue_key}: {response.status_code} {response.text[:500]}")

    def _is_json(self, response: requests.Response) -> bool:
        return "application/json" in response.headers.get("Content-Type", "")

    def test_connection(self) -> tuple[bool, str]:
        """Test Jira connection and authentication
        
        Returns:
            tuple[bool, str]: (success, message)
        """
        try:
            url = f"{self.base_url}/rest/api/3/myself"
            response = requests.get(url, headers=self.auth_header, timeout=10)
            
            if response.status_code == 200 and self._is_json(response):
                data = response.json()
                return True, f"✓ Connected to Jira as {data.get('displayName', 'User')}"
            elif response.status_code == 401:
                return False, "✗ Authentication failed: Invalid email or API token"
            elif response.status_code == 403:
                return False, "✗ Access forbidden: API token doesn't have required permissions"
            elif response.text.strip().startswith("<"):
                return False, f"✗ Jira URL may be incorrect. Got HTML instead of JSON."
            else:
                return False, f"✗ Connection failed: HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "✗ Connection timeout. Check your network and Jira URL."
        except requests.exceptions.ConnectionError:
            return False, f"✗ Cannot connect to {self.base_url}. Check if the URL is correct."
        except Exception as e:
            return False, f"✗ Error: {str(e)}"

    def search_issues(self, project_key: str = None, limit: int = 10) -> list[dict[str, Any]]:
        """Search for issues in Jira
        
        Args:
            project_key: Optional project key to filter by (e.g., 'KAN')
            limit: Maximum number of issues to return
        
        Returns:
            List of issues with key and summary
        """
        try:
            # Build JQL query
            if project_key:
                jql = f"project = {project_key.upper()}"
            else:
                jql = "ORDER BY updated DESC"
            
            url = f"{self.base_url}/rest/api/3/search"
            params = {
                "jql": jql,
                "fields": "key,summary",
                "maxResults": limit
            }
            
            response = requests.get(url, headers=self.auth_header, params=params, timeout=10)
            response.raise_for_status()
            
            if self._is_json(response):
                data = response.json()
                issues = data.get("issues", [])
                return [
                    {"key": issue.get("key"), "summary": issue.get("fields", {}).get("summary")}
                    for issue in issues
                ]
            return []
        except Exception as e:
            raise RuntimeError(f"Failed to search issues: {str(e)}")

    def extract_issue_data(self, issue: dict[str, Any]) -> dict[str, str]:
        fields = issue.get("fields", {})
        summary = fields.get("summary", "") or ""
        description = ""
        desc_field = fields.get("description")
        if isinstance(desc_field, dict):
            desc_content = desc_field.get("content", [])
            text_parts: list[str] = []
            for block in desc_content:
                for content in block.get("content", []):
                    if content.get("type") == "text":
                        text_parts.append(content.get("text", ""))
            description = "\n".join(text_parts)
        elif isinstance(desc_field, str):
            description = desc_field
        return {"summary": summary, "description": description}
