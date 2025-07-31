# Launch from terminal
uvicorn app.main:app --reload --port 8000

# Docker Launch with yaml file.
docker compose -f mpc_py_news_server.yaml up -d

