from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pathlib import Path
import shutil
from .pipeline import evaluate_resume
from .role_loader import load_roles

app = FastAPI(title="Candidate Readiness Evaluator")

# Templates directory (absolute path)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    roles = list(load_roles().keys())
    return templates.TemplateResponse("index.html", {"request": request, "roles": roles})


@app.post("/evaluate-web")
async def evaluate_web(request: Request, resume: UploadFile = File(...), role_name: str = Form(...), jd_text: str | None = Form(None)):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Resume must be a PDF")

    tmp_dir = Path("./tmp")
    tmp_dir.mkdir(exist_ok=True)
    dest = tmp_dir / resume.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    try:
        report = evaluate_resume(dest, role_name, jd_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # render result page
    return templates.TemplateResponse("result.html", {"request": request, "report": report, "role_name": role_name})


@app.post("/evaluate")
async def evaluate(resume: UploadFile = File(...), role_name: str = Form(...), jd_text: str | None = Form(None)):
    # save uploaded file to a temp path
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Resume must be a PDF")

    tmp_dir = Path("./tmp")
    tmp_dir.mkdir(exist_ok=True)
    dest = tmp_dir / resume.filename
    with open(dest, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    try:
        report = evaluate_resume(dest, role_name, jd_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(report)


@app.post("/evaluate-batch")
async def evaluate_batch(files: List[UploadFile] = File(...), role_name: str = Form(...), jd_text: str | None = Form(None)):
    results = []
    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            continue
        tmp_path = Path("./tmp") / f.filename
        with open(tmp_path, "wb") as out:
            shutil.copyfileobj(f.file, out)
        try:
            r = evaluate_resume(tmp_path, role_name, jd_text)
        except Exception as e:
            r = {"error": str(e), "filename": f.filename}
        results.append({"filename": f.filename, "report": r})
    return JSONResponse({"results": results})


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port)
