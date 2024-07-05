import os
from langchain_core.retrievers import BaseRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from base_rag import BaseRAG
from constant import INPUT_SYSTEM_PROMPT, INPUT_USER_PROMPT

class example_RAG(BaseRAG):
    def __init__(
            self,
            metadata_storage_path: str,
            num_docs_to_retrieve: int,
            ) -> None:
        self.embedding_function = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            api_key= os.environ["OPENAI_API_KEY"],
        )
        self.serving_llm = ChatOpenAI(
            model="gpt-4o",
            api_key= os.environ["OPENAI_API_KEY"],
        )
        super().__init__(metadata_storage_path, num_docs_to_retrieve)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", INPUT_SYSTEM_PROMPT),
                ("user", INPUT_USER_PROMPT),
            ]
        )
        self.serving_chain = (
            {"context": self.retriever, "question":RunnablePassthrough()} 
            | prompt 
            | self.serving_llm 
            | StrOutputParser()
        )

    def ingest(self, document_dir):
        loader = DirectoryLoader(document_dir, glob="**/*.*")
        docs = loader.load()
        vector_store = FAISS.from_documents(docs, self.embedding_function)
        vector_store.save_local(self.metadata_storage_path)
    
    def build_retriever(self) -> BaseRetriever:
        vector_store = FAISS.load_local(self.metadata_storage_path, self.embedding_function,allow_dangerous_deserialization=True)
        self.retriever = vector_store.as_retriever(search_kwargs={'k': self.num_docs_to_retrieve})
        return self.retriever
    
    def serve(self, query):
        return self.serving_chain.invoke(query)