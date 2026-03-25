import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fpdf import FPDF
from langchain_openai import ChatOpenAI

load_dotenv()

class CVAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.llm = ChatOpenAI(
            model="openrouter/free",
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
            model_kwargs={
                "extra_headers": {
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "RAG CV Analyzer",
                }
            }
        )
        self.vector_store = None
        self.retriever = None

    def prepare_data(self, paths):
        """Charge les documents (CV, Offre) et prépare le retriever."""
        documents = []
        for path in paths:
            if os.path.exists(path):
                loader = PyPDFLoader(path)
                documents.extend(loader.load())
            else:
                print(f"⚠️  Attention: le fichier '{os.path.basename(path)}' est introuvable.")

        if not documents:
            raise ValueError("Aucun document trouvé.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)

        self.vector_store = Chroma.from_documents(
            documents=docs, 
            embedding=self.embeddings,   
            collection_name="cv_collection"
        )

        self.retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 20, "lambda_mult": 0.5}
        )

    def generate_letter(self, query):
        """Génère la lettre de motivation via le RAG."""
        prompt = PromptTemplate(
            template="""
Tu es un expert en recrutement et un coach en carrière. Utilise les informations suivantes, qui proviennent du CV du candidat et de l'offre d'emploi/stage, pour rédiger une lettre de motivation personnalisée et sur mesure.

La lettre générée doit :
- Mettre en valeur les compétences issues du CV du candidat
- Répondre de manière ciblée aux exigences de l'offre d'emploi
- Ne génère QUE le contenu de la lettre de motivation (pas de blabla inutile avant ou après).

Contexte documents :
{context}

Consigne : {question}
Lettre de motivation générée :
""",
            input_variables=["context", "question"]
        )

        parser = StrOutputParser()

        def format_docs(docs):
            return "\n\n".join([doc.page_content for doc in docs])

        rag_chain = (
           {"context": self.retriever | format_docs, "question": lambda x: x} 
           | prompt 
           | self.llm 
           | parser 
        )

        return rag_chain.invoke(query)

    def export_pdf(self, content, output_path="lettre_de_motivation.pdf"):
        """Exporte le contenu dans un fichier PDF."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        
        cleaned_txt = content.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("œ", "oe")
        cleaned_txt = cleaned_txt.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 7, txt=cleaned_txt)
        pdf.output(output_path)
        return output_path

if __name__ == "__main__":
    # Comportement original en CLI
    analyzer = CVAnalyzer()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [
        os.path.join(script_dir, "cv.pdf"),
        os.path.join(script_dir, "offre.pdf")
    ]
    
    try:
        analyzer.prepare_data(paths)
        query = "Rédige une lettre de motivation complète et adaptée à l'offre en te basant sur mon CV."
        response = analyzer.generate_letter(query)
        print("\n----- LETTRE GÉNÉRÉE -----\n")
        print(response)
        
        analyzer.export_pdf(response)
        print("\n✅ La lettre a été exportée avec succès sous : lettre_de_motivation.pdf\n")
    except Exception as e:
        print(f"\nUne erreur est survenue : {e}\n")