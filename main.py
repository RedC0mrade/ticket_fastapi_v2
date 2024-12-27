import fastapi
import uvicorn


app = fastapi()

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)