import subprocess
import re
import os

def execute_maven_dependency_tree():
    """Executes the Maven dependency:tree command and returns the output."""
    result = subprocess.run(['mvn', 'dependency:tree'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise Exception(f"Maven command failed: {result.stderr}")
    return result.stdout

def parse_dependency_tree(tree_output):
    """Parses the output of mvn dependency:tree to extract groupId, artifactId, and version."""
    dependency_pattern = re.compile(r'([\w\.-]+):([\w\.-]+):([\w\.-]+):([\w\.-]+):([\w\.-]+)')
    dependencies = []

    for line in tree_output.splitlines():
        match = dependency_pattern.search(line)
        if match:
            group_id, artifact_id, packaging, version, scope = match.groups()
            dependencies.append({
                'group_id': group_id,
                'artifact_id': artifact_id,
                'version': version,
                'packaging': packaging
            })

    return dependencies

def construct_maven_paths(dependencies):
    """Constructs the expected paths with 'mavencentral-remote/' as the base prefix for the given dependencies."""
    prefix = 'mavencentral-remote'
    file_paths = []

    for dep in dependencies:
        group_path = dep['group_id'].replace('.', '/')
        artifact_path = dep['artifact_id']
        version = dep['version']
        packaging = dep['packaging']

        # Construct the full path for the dependency file with 'mavencentral-remote/' as the prefix
        file_name = f"{artifact_path}-{version}.{packaging}"
        full_path = os.path.join(prefix, group_path, artifact_path, version, file_name)
        file_paths.append(full_path)

    return file_paths

def escape_special_chars_except_slashes(path):
    """Escapes special regex characters except for slashes (/) and hyphens (-)."""
    # Escape only necessary characters for regex and keep slashes and hyphens intact
    return re.sub(r'([\\^$+*?{}[\]()])', r'\\\1', path)

def generate_regex_pattern(file_paths):
    """Generates a regular expression pattern that matches the 'mavencentral-remote/' file paths."""
    # Do not escape slashes (/) and hyphens (-)
    escaped_paths = [escape_special_chars_except_slashes(path) for path in file_paths]
    regex_pattern = '|'.join(escaped_paths)
    return regex_pattern

if __name__ == '__main__':
    try:
        # Step 1: Execute the Maven command
        tree_output = execute_maven_dependency_tree()

        # Step 2: Parse the dependency tree output
        dependencies = parse_dependency_tree(tree_output)

        # Step 3: Construct the paths with the 'mavencentral-remote/' prefix
        file_paths = construct_maven_paths(dependencies)

        # Step 4: Generate a RegEx pattern to match the files with 'mavencentral-remote/' prefix
        regex_pattern = generate_regex_pattern(file_paths)

        print(regex_pattern)

    except Exception as e:
        print(f"Error: {e}")
