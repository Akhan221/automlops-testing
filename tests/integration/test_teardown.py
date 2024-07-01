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

def teardown_gcloud_resources(project_id, artifact_repo_location): 
    execute_process(f"gcloud artifacts repositories list --project={project_id} --location={artifact_repo_location}", False)

teardown_gcloud_resources("airflow-sandbox-392816", "us-central1")

    
