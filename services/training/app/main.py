from fastapi import FastAPI, Request, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.job_launcher import launch_training_job

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit_training(
    dataset: UploadFile = None,
    gcs_path: str = Form(""),
    n_estimators: int = Form(...),
    max_depth: int = Form(...),
    min_samples_split: int = Form(...),
    min_samples_leaf: int = Form(...),
):
    # Check if either dataset was uploaded or gcs_path is provided
    if not dataset and not gcs_path:
        raise HTTPException(status_code=400, detail="Please upload a dataset file or provide a GCS path.")


    # Prepare the training job arguments
    args = [
        f"--n_estimators={n_estimators}",
        f"--max_depth={max_depth}",
        f"--min_samples_split={min_samples_split}",
        f"--min_samples_leaf={min_samples_leaf}",
        f"--gcs_path={gcs_path}"
    ]

    # Docker image for training job
    image_uri = "us-central1-docker.pkg.dev/sodium-pager-461309-p3/trainer/training:latest"

    # Launch training job (GKE or Cloud Run)
    job_id = launch_training_job(image_uri=image_uri, args=args)

    return {
        "message": f"✅ Training job `{job_id}` launched!",
        "image": image_uri,
        "gcs_path": gcs_path,
        "args": args
    }
