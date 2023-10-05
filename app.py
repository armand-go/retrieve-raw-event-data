import uvicorn


if __name__ == "__main__":
    uvicorn.run("app:serve", host="0.0.0.0", port=8000, reload=True)  # nosec
