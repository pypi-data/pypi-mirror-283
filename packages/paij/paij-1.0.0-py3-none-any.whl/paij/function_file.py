import os
import shutil

import openai
import requests

import config


def generate_method_from_tests(api_key, unit_tests, language="Java"):
    openai.api_key = api_key
    prompt = f"""
        Write the corresponding {language} method that satisfies the following unit tests:
        {unit_tests}

        Note:
        - Do not include any imports related to testing frameworks such as JUnit or Mockito.
        - Only include necessary imports for the functionality of the generated methods.
        - Assume the class name is the same as the given unit test class name.
        - Do not provide explanations, just the complete class and package name.
        - Make the class name {config.CLASS_NAME}

        Method:
        """
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
                        "Please complete all methods and write the best possible code"
             },
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,  # Adjust the length based on your need
        temperature=0.5
    )

    method_code = response.choices[0].message['content'].strip()
    method_code = method_code.replace('```java', '').replace('```', '').rstrip()

    return method_code


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
