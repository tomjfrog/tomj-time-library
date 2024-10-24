import argparse
import http.client

def get_build_dependencies(build_name, build_number, access_token):
  conn = http.client.HTTPSConnection("tomjfrog.jfrog.io")

  payload = f"""builds.find({{
    "name": "{build_name}",
    "number": "{build_number}"}}).include("module", "module.dependency")"""

  headers = {
      'Content-Type': "text/plain",
      'Authorization': f"Bearer {access_token}"
  }

  conn.request("POST", "/artifactory/api/search/aql", payload, headers)

  res = conn.getresponse()
  data = res.read()

  print(data.decode("utf-8"))
  conn.close()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Search builds by GitHub SHA.")
    parser.add_argument("--build_name", help="The Build Name for which to copy dependencies.")
    parser.add_argument("--build_number", help="The Build Number for which to copy dependencies.")
    parser.add_argument("--access_token", help="A valid JFrog access token to make the request.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the search function with the provided GitHub SHA
    get_build_dependencies(args.build_name, args.build_number, args.access_token)

if __name__ == "__main__":
    main()