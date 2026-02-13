from fastapi import FastAPI

app = FastAPI()

print("server running")

@app.get("/")
def root():
    return {"message": "FastAPI is running "}