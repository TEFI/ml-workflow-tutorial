from fastapi import FastAPI, Request, UploadFile, Form
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
    gcs_path: str = Form(default=""),
    n_estimators: int = Form(...),
    max_depth: int = Form(...),
    min_samples_split: int = Form(...),
    min_samples_leaf: int = Form(...),
):

    #job_name = launch_training_job(payload)
    #return {"message": f"Training job {job_name} started!"}
    return {
        "message": "Received submission",
        "dataset": dataset.filename if dataset else None,
        "gcs_path": gcs_path,
        "model": "random_forest",
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "min_samples_split": min_samples_split,
        "min_samples_leaf": min_samples_leaf
    }





