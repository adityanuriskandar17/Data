# ============================================
# BACKEND — FastAPI + Database + File Scanner
# ============================================

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import markdown as md_lib
from pathlib import Path

# Ensure backend package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))
from database import init_db, toggle_progress, get_all_progress, get_db_session
from sqlalchemy import text

app = FastAPI(title="Data Engineering Learning Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # web/../ (latihan_de)
IGNORE_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv", "web"}
CODE_EXTENSIONS = {".py", ".sql", ".sh", ".js", ".yml", ".yaml", ".tf", ".css", ".html"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
MARKDOWN_EXTENSIONS = {".md"}

# ============================================
# INIT DATABASE ON STARTUP
# ============================================

@app.on_event("startup")
async def startup():
    await init_db()

# ============================================
# BUILD FILE TREE
# ============================================

def build_tree(path: Path, base: Path) -> dict | None:
    name = path.name
    if name.startswith(".") or name in IGNORE_DIRS:
        return None
    if path.is_dir():
        children = []
        for child in sorted(path.iterdir()):
            node = build_tree(child, base)
            if node:
                children.append(node)
        if not children:
            return None
        rel = path.relative_to(base)
        return {
            "name": name,
            "path": str(rel),
            "type": "folder",
            "children": children
        }
    else:
        ext = path.suffix.lower()
        if ext not in CODE_EXTENSIONS | IMAGE_EXTENSIONS | MARKDOWN_EXTENSIONS:
            return None
        rel = path.relative_to(base)
        file_type = "markdown" if ext == ".md" else "image" if ext in IMAGE_EXTENSIONS else "code"
        return {
            "name": name,
            "path": str(rel),
            "type": "file",
            "file_type": file_type,
            "ext": ext.replace(".", "")
        }


@app.get("/api/tree")
async def get_tree():
    tree = build_tree(BASE_DIR, BASE_DIR)
    if tree is None:
        return {"name": "latihan_de", "path": "", "type": "folder", "children": []}
    return tree


# ============================================
# READ FILE CONTENT
# ============================================

@app.get("/api/file")
async def get_file(path: str = Query(...)):
    full_path = (BASE_DIR / path).resolve()
    if not full_path.exists() or not str(full_path).startswith(str(BASE_DIR)):
        raise HTTPException(404, "File not found")

    ext = full_path.suffix.lower()
    content = full_path.read_text(encoding="utf-8", errors="replace")

    if ext == ".md":
        html = md_lib.markdown(
            content,
            extensions=["fenced_code", "tables", "sane_lists", "toc"]
        )
        return {"type": "markdown", "content": html, "raw": content}
    else:
        lang_map = {
            ".py": "python", ".sql": "sql", ".sh": "bash",
            ".js": "javascript", ".yml": "yaml", ".yaml": "yaml",
            ".tf": "hcl", ".css": "css", ".html": "html", ".json": "json"
        }
        lang = lang_map.get(ext, "")
        return {"type": "code", "content": content, "language": lang}


# ============================================
# SEARCH
# ============================================

@app.get("/api/search")
async def search(q: str = Query("", min_length=1)):
    results = []
    q_lower = q.lower()
    for file_path in BASE_DIR.rglob("*"):
        if file_path.suffix.lower() not in CODE_EXTENSIONS | MARKDOWN_EXTENSIONS:
            continue
        rel = str(file_path.relative_to(BASE_DIR))
        if any(ign in rel.split(os.sep) for ign in IGNORE_DIRS):
            continue
        if q_lower in rel.lower():
            results.append({
                "path": rel,
                "name": file_path.name,
                "match": "filename"
            })
            if len(results) >= 20:
                break
    if len(results) < 20:
        for file_path in BASE_DIR.rglob("*"):
            if file_path.suffix.lower() not in CODE_EXTENSIONS | MARKDOWN_EXTENSIONS:
                continue
            rel = str(file_path.relative_to(BASE_DIR))
            if any(ign in rel.split(os.sep) for ign in IGNORE_DIRS):
                continue
            if any(r["path"] == rel for r in results):
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
                if q_lower in content.lower():
                    results.append({
                        "path": rel,
                        "name": file_path.name,
                        "match": "content"
                    })
                    if len(results) >= 30:
                        break
            except Exception:
                continue
    return {"results": results, "total": len(results)}


# ============================================
# PROGRESS TRACKING
# ============================================

@app.get("/api/progress")
async def get_progress():
    rows = await get_all_progress()
    return {row["file_path"]: row["completed"] for row in rows}


@app.post("/api/progress/toggle")
async def toggle_progress_endpoint(file_path: str = Query(...)):
    result = await toggle_progress(file_path)
    return result


# ============================================
# ROOT — SERVE FRONTEND
# ============================================

from fastapi.responses import FileResponse

@app.get("/", response_class=HTMLResponse)
async def index():
    index_path = BASE_DIR / "web" / "templates" / "index.html"
    if index_path.exists():
        return HTMLResponse(index_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>index.html not found</h1>")


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "web" / "static")), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
