import re
from pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import Document
from llama_index.core import (
    VectorStoreIndex,
    ServiceContext,
)
from dataclasses import dataclass
import os

from pypdf import PdfReader

key = "OPENAI_API_KEY"  # os.environ['OPENAI_API_KEY']
HEADING_PATTERN = re.compile(r"^\d+\.\d*\s*(?:[A-Za-z]+\s*){1,5}$", re.MULTILINE)

@dataclass
class Input:
    query: str
    file_path: str

@dataclass
class Citation:
    source: str
    text: str

class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]

class DocumentService:

    """
    Update this service to load the pdf and extract its contents.
    The example code below will help with the data structured required
    when using the QdrantService.load() method below. Note: for this
    exercise, ignore the subtle difference between llama-index's 
    Document and Node classes (i.e, treat them as interchangeable).

    # example code
    def create_documents() -> list[Document]:

        docs = [
            Document(
                metadata={"Section": "Law 1"},
                text="Theft is punishable by hanging",
            ),
            Document(
                metadata={"Section": "Law 2"},
                text="Tax evasion is punishable by banishment.",
            ),
        ]

        return docs

     """
    def create_documents(self, file_path: str) -> list[Document]:
        reader = PdfReader(file_path)
        docs: list[Document] = []
        text = ""
        
        # Extract text from all pages
        for i, page in enumerate(reader.pages):
            # NOTE: never got it properly identify whitespaces
            # text = page.extract_text(space_width=1)

            # NOTE `extract_text` docs note:Do not rely on the order of text coming out of this function, as it will change if this function is made more sophisticated.
            # TODO: consider parsing per page/doc to avoid ordering misalignments (skipped for now, none observed)
            text += page.extract_text(extraction_mode="layout")

            # print(text)  # DEBUG

        # Split text into sections
        text_sections = HEADING_PATTERN.split(text)
        section_headings = HEADING_PATTERN.findall(text)

        # NOTE no numbered heading for title, so extract independently
        # TODO smarter regex (or another method) for unified title/section extraction
        docs.append(Document(
            metadata={"Section": "Title"},
            text=text_sections[0]
        ))

        # TODO additional sanity checks that we extracted all the text correctly
        assert len(text_sections) == len(section_headings) + 1, "Number of sections and headings do not match"

        for section, heading in zip(text_sections[1:], section_headings):
            doc = Document(
                metadata={"Section": heading},
                text=section
            )
            docs.append(doc)

        return docs

class QdrantService:
    def __init__(self, k: int = 2):
        self.index = None
        self.k = k
    
    def connect(self) -> None:
        client = qdrant_client.QdrantClient(location=":memory:")
                
        vstore = QdrantVectorStore(client=client, collection_name='temp')

        service_context = ServiceContext.from_defaults(
            embed_model=OpenAIEmbedding(),
            llm=OpenAI(api_key=key, model="gpt-4")
            )

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vstore, 
            service_context=service_context
            )

    def load(self, docs = list[Document]):
        self.index.insert_nodes(docs)
    
    def query(self, query_str: str) -> Output:

        """
        This method needs to initialize the query engine, run the query, and return
        the result as a pydantic Output class. This is what will be returned as
        JSON via the FastAPI endpount. Fee free to do this however you'd like, but
        a its worth noting that the llama-index package has a CitationQueryEngine...

        Also, be sure to make use of self.k (the number of vectors to return based
        on semantic similarity).

        # Example output object
        citations = [
            Citation(source="Law 1", text="Theft is punishable by hanging"),
            Citation(source="Law 2", text="Tax evasion is punishable by banishment."),
        ]

        output = Output(
            query=query_str, 
            response=response_text, 
            citations=citations
            )
        
        return output

        """
       

if __name__ == "__main__":
    # Example workflow
    doc_serivce = DocumentService() # implemented

    laws_pdf = "docs/laws.pdf"
    docs = doc_serivce.create_documents(laws_pdf) # WIP

    print(f"Created {len(docs)} documents from {laws_pdf}")
    for d in docs:
        print(d.metadata)
        print(d.text)

    # index = QdrantService() # implemented
    # index.connect() # implemented
    # index.load() # implemented

    # index.query("what happens if I steal?") # NOT implemented





