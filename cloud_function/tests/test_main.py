
import base64
import json
import os
import unittest
from unittest.mock import patch, MagicMock

from main import handler


class TestHandler(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "GCP_PROJECT": "test-project",
            "FUNCTION_REGION": "test-region",
            "TARGET_CLOUD_RUN_JOB": "test-job",
        },
    )
    @patch("main.run_job")
    def test_handler_success(self, mock_run_job):
        """Test that the function successfully decodes a valid Pub/Sub message."""
        message = {"key": "value"}
        data = base64.b64encode(json.dumps(message).encode("utf-8"))
        event = {"data": data}

        handler(event, None)

        mock_run_job.assert_called_once_with(
            "test-project", "test-region", "test-job", json.dumps(message)
        )

    @patch.dict(
        os.environ,
        {
            "GCP_PROJECT": "test-project",
            "FUNCTION_REGION": "test-region",
            "TARGET_CLOUD_RUN_JOB": "test-job",
        },
    )
    @patch("main.run_job")
    def test_handler_invalid_json(self, mock_run_job):
        """Test that the function handles a message that is not valid JSON."""
        data = base64.b64encode(b"not json")
        event = {"data": data}

        handler(event, None)

        mock_run_job.assert_not_called()

    @patch("main.run_v2.JobsClient")
    def test_run_job(self, mock_jobs_client):
        """Test that the run_job function is called with the correct arguments."""
        from main import run_job

        project = "test-project"
        region = "test-region"
        job_name = "test-job"
        message = json.dumps({"key": "value"})

        mock_client_instance = MagicMock()
        mock_jobs_client.return_value = mock_client_instance

        run_job(project, region, job_name, message)

        mock_jobs_client.assert_called_once()
        mock_client_instance.run_job.assert_called_once()


if __name__ == "__main__":
    unittest.main()
