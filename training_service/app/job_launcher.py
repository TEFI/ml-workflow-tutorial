import uuid
import datetime
from kubernetes import client, config

def launch_training_job(payload):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    job_name = f"training-job-{timestamp}-{short_uuid}"

    config.load_incluster_config()
    batch_v1 = client.BatchV1Api()

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="trainer",
                            image="us-central1-docker.pkg.dev/YOUR_PROJECT_ID/training-repo/training-image:latest",
                            env=[
                                client.V1EnvVar(name="DATASET_PATH", value=payload.get("dataset_path", "")),
                                client.V1EnvVar(name="OUTPUT_PATH", value=payload.get("output_path", ""))
                            ],
                            resources=client.V1ResourceRequirements(
                                limits={"cpu": "2", "memory": "4Gi"}
                            )
                        )
                    ],
                    restart_policy="Never"
                )
            ),
            backoff_limit=2
        )
    )

    batch_v1.create_namespaced_job(namespace="default", body=job)
    return job_name
