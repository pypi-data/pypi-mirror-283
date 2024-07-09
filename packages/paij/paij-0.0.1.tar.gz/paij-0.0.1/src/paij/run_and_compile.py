import os
import subprocess


def run_maven_commands(maven_home, project_dir):
    maven_executable = os.path.join(maven_home, 'mvn')

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
            [maven_executable, "test"],
            cwd=project_dir,
            capture_output=True, text=True, shell=True
        )

        if test_process.returncode != 0:
            print(f"Execution failed:\n{test_process.stderr}")
            return False
        else:
            print("Execution successful.")
            print(test_process.stdout)
            return True
