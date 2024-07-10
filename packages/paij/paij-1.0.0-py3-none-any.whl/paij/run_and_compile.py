import os
import subprocess

import config


def run_maven_commands(maven_home, project_dir, test_class_name, max_retries=3):
    maven_executable = os.path.join(maven_home, 'mvn')
    retries = 0

    while retries < max_retries:
        compile_process = subprocess.run(
            [maven_executable, "clean", "compile", "test-compile"],
            cwd=project_dir,
            capture_output=True, text=True, shell=True
        )

        if compile_process.returncode != 0:
            print(f"Compilation failed:\n{compile_process.stderr}")
            return False
        else:
            print("Compilation successful.")

            test_process = subprocess.run(
                [maven_executable, "test", f"-Dtest={test_class_name}"],
                cwd=project_dir,
                capture_output=True, text=True, shell=True
            )

            if test_process.returncode != 0:
                print(f"Test execution failed (attempt {retries + 1}/{max_retries}):\n{test_process.stderr}")
                retries += 1
            else:
                print("Test execution successful.")
                print(test_process.stdout)
                return True

    print("Test execution failed after maximum retries.")
    return False


run_maven_commands(config.MAVEN_HOME, config.PROJECT_DIR, "TDDOrderServiceTest")
