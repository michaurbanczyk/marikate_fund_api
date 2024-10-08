from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get('/hello')
def another_endpoint():
    print("Here is the endpoint!")
    return {
        "fieldA": "fieldA"
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)