import http.client
import argparse

# Function to make the HTTP request
def search_builds(build_name, access_token):

   conn = http.client.HTTPSConnection("tomjfrog.jfrog.io")

   payload = f"""builds.find({{
           "name":"{build_name}"
       }}).include("name", "number", "created").sort({{"$desc": ["created"]}}).limit(1)"""

   headers = {
       'Content-Type': "text/plain",
       'Authorization': f"Bearer {access_token}"
   }

   conn.request("POST", "/artifactory/api/search/aql", payload, headers)

   res = conn.getresponse()
   data = res.read()

   print(data.decode("utf-8"))

# Main function to handle command-line input
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Search builds by GitHub SHA.")
    parser.add_argument("--access_token", help="A valid JFrog access token to make the request.")
    parser.add_argument("--build_name", help="The name of the build to query for it's latest.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the search function with the provided GitHub SHA
    search_builds(args.build_name, args.access_token)

if __name__ == "__main__":
    main()
