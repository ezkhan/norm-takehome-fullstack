# import uvicorn
from fastapi import FastAPI, Query
from app.utils import Output, QdrantService, DocumentService

app = FastAPI()

"""
Please create an endpoint that accepts a query string, e.g., "what happens if I steal 
from the Sept?" and returns a JSON response serialized from the Pydantic Output class.
"""

# Initialize the Qdrant service and load documents
qdrant_service = None

def get_qdrant_service() -> QdrantService:
    global qdrant_service
    if qdrant_service is None:
        doc_service = DocumentService()
        laws_pdf = "docs/laws.pdf"
        docs = doc_service.create_documents(laws_pdf)
        
        qdrant_service = QdrantService()
        qdrant_service.connect()
        qdrant_service.load(docs)
    return qdrant_service


@app.get("/")
def get_hello():
    return {"message": "Hello World"}


@app.post("/query-laws")
def query_laws(inquiry: str):
    service = get_qdrant_service()
    result = service.query(inquiry)
    return result


# if __name__ == "__main__":
#     uvicorn.run(app=my_app, host="127.0.0.1", port=8000, reload=True)
