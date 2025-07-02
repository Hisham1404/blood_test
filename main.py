from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from celery.result import AsyncResult
import os
import uuid
from dotenv import load_dotenv
# Import the celery app instance
from celery_worker import celery_app, run_crew_task

load_dotenv()

app = FastAPI(title="Blood Test Report Analyser")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """
    Analyze blood test report asynchronously and provide comprehensive health recommendations.
    This endpoint now starts a background task and returns a task ID.
    """
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if not query:
            query = "Summarise my Blood Test Report"
            
        # Send the task to the Celery queue
        task = run_crew_task.delay(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "message": "Analysis started. Use the task_id to check the status.",
            "task_id": task.id,
            "file_processed": file.filename
        }
        
    except Exception as e:
        # Clean up the file if an error occurs before the task is sent
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error starting analysis: {str(e)}")

@app.get("/results/{task_id}")
async def get_analysis_result(task_id: str):
    """
    Fetches the result of an analysis task using its task_id.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.ready():
        if task_result.successful():
            return {
                "status": "completed",
                "task_id": task_id,
                "analysis": task_result.get()
            }
        else:
            return {
                "status": "failed",
                "task_id": task_id,
                "error": str(task_result.info)  # .info contains the exception
            }
    else:
        return {
            "status": "pending",
            "task_id": task_id,
            "message": "Analysis is still in progress."
        }

if __name__ == "__main__":
    import uvicorn
    # Note: reload=True is not recommended for production with Celery
    # as it can cause issues with task discovery.
    uvicorn.run(app, host="0.0.0.0", port=8000)