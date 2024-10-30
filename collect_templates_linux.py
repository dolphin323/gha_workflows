import subprocess
import re


# TODO: Add "help command" for such commands as cd, pwd, echo, etc.


def get_command_help_output(command):
    try:
        help_output = subprocess.check_output(
            f"{command} --help", shell=True, stderr=subprocess.STDOUT, text=True
        )
        return help_output
    except subprocess.CalledProcessError:
        return ""


def extract_usages_and_description(help_output):
    usage_pattern = re.findall(
        r"(^\s*Usage:.*(?:\n\s*or:.*)*)", help_output, re.MULTILINE
    )

    if usage_pattern:
        usage_end_index = help_output.find(usage_pattern[0]) + len(usage_pattern[0])

        description_match = re.search(
            r"^\s*[^Usage|or:].*", help_output[usage_end_index:], re.MULTILINE
        )
        description = (
            description_match.group().strip()
            if description_match
            else "No description found."
        )

        return usage_pattern, description
    else:
        return None, "No usage patterns found."


def collect_command_info(commands):
    command_info = {}

    for command in commands:
        help_output = get_command_help_output(command)
        if help_output:
            usages, description = extract_usages_and_description(help_output)
            command_info[command] = {"usages": usages, "description": description}

    return command_info


commands = [
    "mv",
    "cp",
    "ls",
    "rm",
    "mkdir",
    "chmod",
    "chown",
    "cd",
    "pwd",
    "touch",
    "echo",
]

command_info = collect_command_info(commands)

for cmd, info in command_info.items():
    print(f"Command: {cmd}")
    print("Usages:")
    for usage in info["usages"]:
        print(usage.strip())
    print(f"Description: {info['description']}\n")
