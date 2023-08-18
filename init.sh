git stash 
git pull 
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9 
uvicorn main:app --port 8000 --host 0.0.0.0