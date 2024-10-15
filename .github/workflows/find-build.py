import http.client
import argparse

# Function to make the HTTP request
def search_builds(github_sha, access_token):
    # Create a connection to the server
    conn = http.client.HTTPSConnection("tomjfrog.jfrog.io")

    # Define the payload (AQL query), inserting the GitHub SHA
    payload = f"""builds.find({{
        "@buildInfo.env.GITHUB_SHA":"{github_sha}"
    }}).include("name", "number")"""

    # Set the headers, including Authorization
    headers = {
        'Content-Type': "text/plain",
        'Authorization': f"Bearer {access_token}"
    }

    # Make the POST request to the AQL API
    conn.request("POST", "/artifactory/api/search/aql", payload, headers)

    # Get the response
    res = conn.getresponse()

    # Read and decode the response data
    data = res.read().decode("utf-8")

    # Print the decoded response
    print(data)

    # Close the connection
    conn.close()

# Main function to handle command-line input
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Search builds by GitHub SHA.")
    parser.add_argument("--github_sha", help="The GitHub SHA to for which to search.")
    parser.add_argument("--access_token", help="A valid JFrog access token to make the request.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the search function with the provided GitHub SHA
    search_builds(args.github_sha, args.github_sha)

if __name__ == "__main__":
    main()
