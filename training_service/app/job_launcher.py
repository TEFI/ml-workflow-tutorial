import uuid
from google.cloud import run_v2
from google.cloud.run_v2.types import Job, TaskTemplate, Container, ExecutionTemplate

from app.config import PARENT

def launch_training_job(image_uri: str, args: list[str]) -> str:
    client = run_v2.JobsClient()
    job_id = f"train-job-{uuid.uuid4().hex[:8]}"

    job = Job(
        template=ExecutionTemplate(
            task_count=1,
            template=TaskTemplate(
                containers=[Container(image=image_uri, args=args)],
                max_retries=1,
                timeout={"seconds": 3600},
                service_account="terraform-deployer@sodium-pager-461309-p3.iam.gserviceaccount.com",
            ),
        )
    )

    operation = client.create_job(parent=PARENT, job=job, job_id=job_id)
    operation.result()

    client.run_job(name=f"{PARENT}/jobs/{job_id}")

    return job_id
