import uvicorn
from fastapi import FastAPI

serve = FastAPI()


@serve.get("/")
def ping():
    return "."

if __name__ == "__main__":
    uvicorn.run("api:serve", host="0.0.0.0", port=8000, reload=True)
