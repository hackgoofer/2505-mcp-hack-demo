Install dependency with "pip install -r requirements.txt"

Run backend:
`uvicorn app:app --host=0.0.0.0 --port=10001`

Curl with:

```
curl -X POST "http://0.0.0.0:10001/run" \
  -H "Content-Type: application/json" \
  -d '{"query": "Can you change a file on this repo? https://github.com/edshen17/mcp-hackathon. Can you add an empty file.txt?"}'
```
