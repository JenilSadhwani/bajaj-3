from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from utils import extract_lab_tests

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        tests = extract_lab_tests(file.file)
        return JSONResponse(content={
            "is_success": True,
            "tests": tests
        })
    except Exception as e:
        return JSONResponse(content={
            "is_success": False,
            "error": str(e)
        }, status_code=500)
