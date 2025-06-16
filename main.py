import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils import reforcar_resposta_em_portugues

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_API_KEY
)

# Carregar e indexar PDF
loader_sql_reference = PyPDFLoader("oracle_docs/sql-language-reference.pdf")
documents_sql_reference = loader_sql_reference.load()

loader_backup_recovery = PyPDFLoader("oracle_docs/database-backup-and-recovery-reference.pdf")
documents_backup_recovery = loader_backup_recovery.load()

loader_backup_recovery = PyPDFLoader("oracle_docs/database-administrators-guide.pdf")
documents_backup_recovery = loader_backup_recovery.load()

all_documents = documents_sql_reference + documents_backup_recovery

db = FAISS.from_documents(all_documents, embeddings)
retriever = db.as_retriever()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

# Prompt personalizado forçando português
template = """
Você é um assistente DBA Oracle Sênior, extremamente experiente e didático. 
Responda sempre em português do Brasil, de forma clara, concisa, objetiva e profissional.
Priorize a praticidade e a aplicabilidade das suas respostas.

Se a pergunta solicitar exemplos de comandos SQL:
- Gere exemplos realistas e funcionais, baseados no contexto fornecido.
- Se não houver contexto suficiente, use seu vasto conhecimento para criar um exemplo relevante e útil.
- Explique brevemente o propósito de cada comando ou bloco de código.

Evite respostas excessivamente longas. Vá direto ao ponto, mas forneça código ou exemplos detalhados quando forem cruciais para o entendimento.
Formate os comandos SQL de forma legível.

Contexto:
{context}

Pergunta: {question}

Se a pergunta não for sobre Banco de Dados Oracle, recuse educadamente responder, informando que seu conhecimento é especializado nesse domínio.

Resposta Detalhada e Prática:
"""

prompt_pt = PromptTemplate(template=template, input_variables=["context", "question"])

# QA Chain com prompt forçado
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_pt}
)

# Handler para resumir e responder
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = update.message.text

    try:
        resultado = qa_chain.invoke({"query": pergunta})
        resposta_bruta = resultado["result"]

        # Reforçar português e enviar
        resposta_final = reforcar_resposta_em_portugues(resposta_bruta)
        await update.message.reply_text(resposta_final)

    except Exception as e:
        await update.message.reply_text("Ocorreu um erro ao processar sua pergunta. Tente novamente.")
        print("Erro:", e)

# Iniciar bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == '__main__':
    print("Bot rodando...")
    app.run_polling()
