from fastapi import FastAPI, Query
from app.rag_engine import generate_tarot_response, generate_tarot_response_test

app = FastAPI()

@app.get("/predict")
def predict(question: str = Query(...)):
    result = generate_tarot_response_test(question)
    return {"result": result}
