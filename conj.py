import requests

def login_conjur(auth_url, account, username, api_key):
    """
    Authenticate with Conjur and get the access token.
    """
    headers = {"Content-Type": "text/plain"}
    response = requests.post(f"{auth_url}/{account}/authenticate", headers=headers, data=api_key, verify=False)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to authenticate: {e.response.status_code} {e.response.reason}")
        return None
    return response.text

def load_policy(api_url, account, policy_name, policy_file, token):
    """
    Load or update a policy in Conjur.
    """
    headers = {
        "Authorization": f"Token token=\"{token}\"",
        "Content-Type": "application/x-yaml"
    }
    with open(policy_file, 'rb') as file:
        policy_data = file.read()
    
    response = requests.post(f"{api_url}/{account}/policies/{policy_name}", headers=headers, data=policy_data, verify=False)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to load policy: {e.response.status_code} {e.response.reason}")
        return None
    return response.json()

# Example usage
if __name__ == "__main__":
    conjur_auth_url = "https://conjur.example.com/authn"
    conjur_api_url = "https://conjur.example.com/policies"
    conjur_account = "my-account"
    username = "admin"
    api_key = "your-api-key"
    policy_name = "root"  # Or the appropriate policy branch
    policy_file = "path/to/your/policy/file.yml"
    
    # Log in to Conjur
    token = login_conjur(conjur_auth_url, conjur_account, username, api_key)
    if token:
        print("Successfully authenticated.")
        # Load or update the policy
        result = load_policy(conjur_api_url, conjur_account, policy_name, policy_file, token)
        if result:
            print("Policy loaded successfully:", result)
        else:
            print("Failed to load policy.")
    else:
        print("Authentication failed.")
