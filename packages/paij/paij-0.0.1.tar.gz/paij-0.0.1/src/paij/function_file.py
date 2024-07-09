import os
import shutil

import openai
import requests


def generate_method_from_tests(api_key, unit_tests, language="Java"):
    openai.api_key = api_key
    prompt = f"Write the corresponding {language} method that satisfies the following unit tests:\n\n{unit_tests}\n\nMethod:"

    response = openai.ChatCompletion.create(
        # Model is changeable into gpt-4o, gpt-4-turbo, or gpt-3.5-turbo.
        # Gpt-4o and gpt-4-turbo are also less likely than gpt-3.5-turbo to make up information,
        # a behavior known as "hallucination". Finally, gpt-4o and gpt-4-turbo have a context window
        # that supports up to 128,000 tokens compared to 4,096 tokens for gpt-3.5-turbo, meaning they
        # can reason over much more information at once.
        # You can look into https://platform.openai.com/docs/guides/text-generation
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that writes up to multiple methods to satisfy unit tests. "
                        "Please complete all methods and write the best possible code. "
                        "Assume that class name is the same as the given unit test class name, generate a class with written methods. "
                        "Don't give an explanation, just the whole class and package name is enough."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,  # Adjust the length based on your need
        temperature=0.5
    )

    method_code = response.choices[0].message['content'].strip()
    method_code = method_code.replace('```', '')
    method_code = method_code.rstrip()
    if method_code.endswith(' '):
        method_code = method_code[:-1].rstrip()
    valid_imports = [
        "import java.time.LocalDateTime;",
        "import java.util.List;",
        "import java.util.Map;",
        "import java.util.stream.Collectors;",
        "import java.util.Collections;"
    ]
    cleaned_code_lines = []
    for line in method_code.split('\n'):
        if line.strip().startswith('import'):
            for valid_import in valid_imports:
                if valid_import in line.strip():
                    cleaned_code_lines.append(valid_import)
                    break
        elif not line.strip().startswith('java'):
            cleaned_code_lines.append(line)

    cleaned_method_code = '\n'.join(cleaned_code_lines)

    return cleaned_method_code


def read_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content


def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def download_file(url, dest):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest, 'wb') as file:
            shutil.copyfileobj(response.raw, file)


def create_project_structure(base_dir, project_name):
    project_path = os.path.join(base_dir, project_name)
    os.makedirs(project_path, exist_ok=True)
    return project_path


def process_unit_tests(unit_tests):
    import_lines = []
    code_lines = []
    unit_test_lines = unit_tests.split('\n')

    for line in unit_test_lines:
        if line.startswith('import'):
            import_lines.append(line)
        elif not line.startswith('package'):
            code_lines.append(line)

    import_package = '\n'.join(import_lines)
    real_codes = '\n'.join(code_lines)

    return import_package, real_codes
