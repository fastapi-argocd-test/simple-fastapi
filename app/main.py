from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os
import markdown

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
CONTENT_DIR = Path(os.getenv("CONTENT_DIR", str(BASE_DIR / "content"))).expanduser().resolve()
DEFAULT_MD = os.getenv("DEFAULT_MD", "portfolio.md")
MD_PATH = CONTENT_DIR / DEFAULT_MD


app = FastAPI()

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

PROFILE_NAME = os.getenv("PROFILE_NAME", "Your Name")

def render_markdown(md_text: str) -> tuple[str, str]:
    md = markdown.Markdown(
        extensions=["toc", "fenced_code", "tables", "codehilite", "smarty"],
        extension_configs={
            "toc": {
                "toc_depth": "2-2",
                "slugify": lambda s, sep: "-".join(
                    "".join(ch.lower() if ch.isalnum() else " " for ch in s).split()
                ),
            }
        },
        output_format="html5",
    )
    body_html = md.convert(md_text)
    toc_html = md.toc
    return body_html, toc_html


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if not MD_PATH.exists():
        return HTMLResponse(
            content=f"<h1>Markdown not found</h1><p>{MD_PATH}</p>",
            status_code=404,
        )

    md_text = MD_PATH.read_text(encoding="utf-8")
    body_html, toc_html = render_markdown(md_text)
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "body": body_html,
            "toc": toc_html,
            "title": "Portfolio",
            "profile_name": PROFILE_NAME,
        },
    )

@app.get("/files/{filename}", include_in_schema=False)
def serve_file(filename: str):
    file_path = (CONTENT_DIR / filename).resolve()

    if CONTENT_DIR not in file_path.parents and file_path != CONTENT_DIR:
        raise HTTPException(status_code=404, detail="Not found")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    media_type = "application/pdf" if file_path.suffix.lower() == ".pdf" else None

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{file_path.name}"'
        }
    )