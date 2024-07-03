import subprocess
import os
import logging
import time
from google.cloud import aiplatform

def execute_process(command: str, to_null: bool):
        """Executes an external shell process.

        Args:
            command: The string of the command to execute.
            to_null: Determines where to send output.
        Raises:
            Exception: If an error occurs in executing the script.
        """
        stdout = subprocess.DEVNULL if to_null else None
        try:
            subprocess.run([command], shell=True, check=True,
                stdout=stdout,
                stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as err:
            raise RuntimeError(f'Error executing process. {err}') from err

def string_execute_process(command: str, to_null: bool = False) -> str:
    """Executes an external shell process and captures its output.

    Args:
        command: The string of the command to execute.
        to_null: If True, output will be sent to /dev/null; otherwise, it's captured.

    Returns:
        The combined standard output (stdout) and standard error (stderr) as a string.

    Raises:
        RuntimeError: If an error occurs during command execution.
    """

    try:
        result = subprocess.run(
            command,
            shell=True,  # Interpret the command as a shell command
            check=True,   # Raise an exception if the command returns a non-zero exit code
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            text=True,     # Decode output as text (Python 3.7+)
        )

        if to_null:
            return ""  # Return an empty string if output is directed to /dev/null
        else:
            return result.stdout  # Return the captured output as a string

    except subprocess.CalledProcessError as err:
        raise RuntimeError(f'Error executing process: {err}') from err



def teardown_gcloud_artifact_registry(project_id, artifact_repo_location, artifact_repo_name="dry-beans-dt-inferencing-artifact-registry"): 
    artifact_list = string_execute_process(f'gcloud artifacts repositories list --project={project_id} --location={artifact_repo_location}', False)
    if artifact_repo_name in artifact_list:
        print("This is the artifact list: ", artifact_list)
        outputs = string_execute_process(f"gcloud artifacts repositories delete {artifact_repo_name} --location={artifact_repo_location} --quiet")
        print(outputs)
    else:
        print(f"The artifact registry {artifact_repo_name} doesn't exist in {artifact_repo_location}")

from google.cloud import storage


def teardown_gcs_bucket(project_id, bucket_name):
    """Deletes a Google Cloud Storage bucket if it exists.

    Args:
        project_id: The ID of the Google Cloud project.
        bucket_name: The name of the bucket to delete.
    """
    storage_client = storage.Client(project=project_id)
    try:
        bucket = storage_client.get_bucket(bucket_name)  
        bucket.delete(force=True) 
        print(f"Bucket '{bucket_name}' deleted successfully.")
    except:
        print(f"Bucket '{bucket_name}' does not exist.")

# teardown_gcloud_artifact_registry("airflow-sandbox-392816", "us-central1")

teardown_gcs_bucket("airflow-sandbox-392816", "nim-tests-mm")

    
