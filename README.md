## Run Locally (Python)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
---

## Run with Docker

build image
```bash
docker build -t portfolio .
```
run container
```bash
docker run --rm -p 8000:8000 \
  -e PROFILE_NAME="user" \
  -v ./content:/docs:ro \
  portfolio
```

## Credits

This project uses the **Start Bootstrap - Resume** template.

- Template: https://github.com/StartBootstrap/startbootstrap-resume
- License: MIT License
- Copyright (c) Start Bootstrap
