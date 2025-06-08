from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from model import predict_bias
from extract import get_details
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks_progress = {}

class PredictRequest(BaseModel):
    headline: str
    content: str

def run_prediction(task_id, headline, content):
    start_time = time.time()
    prediction = predict_bias(headline, content)
    elapsed = time.time() - start_time
    tasks_progress[task_id] = {
        "progress": 100,
        "eta_seconds": 0,
        "result": prediction,
        "elapsed": elapsed
    }

@app.post("/api/predict")
def predict_endpoint(data: PredictRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks_progress[task_id] = {"progress": 0, "eta_seconds": None, "result": None, "elapsed": None}
    background_tasks.add_task(run_prediction, task_id, data.headline, data.content)
    return {"task_id": task_id}

@app.post("/api/extract")
async def content_extract(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return {"error": "No URL provided."}
    article = get_details(url)

    if not article or (not article[0] and not article[1]):
        return {"error": "Failed to extract content from the URL."}
    return {"headline": article[0], "content": article[1]}

@app.get("/api/result/{task_id}")
def get_result(task_id: str):
    task = tasks_progress.get(task_id)
    if not task:
        return {"status": "not_found"}
    if task["result"] is None:
        return {"status": "pending"}
    return {
        "status": "done",
        "prediction": task["result"],
        "elapsed": task.get("elapsed", None)
    }