import uvicorn
from fastapi import FastAPI

from router.index_router import index_router

app = FastAPI()
app.include_router(index_router)

def main():
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    main()