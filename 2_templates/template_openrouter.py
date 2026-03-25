import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# 1. Configuration initiale
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# 2. Initialisation du modèle via OpenRouter
chat = ChatOpenAI(
    model="openrouter/free",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model_kwargs={
        "extra_headers": {
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "LangChain Chat Script",
        }
    }
)

# 3. Création du Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un extracteur de données. Tu dois transformer chaque demande de l'utilisateur en un objet JSON valide.
    Le JSON doit contenir trois clés : 
    - 'sujet' : le thème principal.
    - 'sentiment' : (positif/neutre/négatif).
    - 'action_requise' : ce que l'utilisateur attend de toi.
    Ne réponds rien d'autre que le JSON."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

# 4. Création de la chaîne avec LCEL (LangChain Expression Language)
chain = prompt | chat

# 5. Initialisation de l'historique
chat_history = []

# 6. Boucle de conversation
while True:
    try:
        user_input = input("\nVous: ").strip()
    except (KeyboardInterrupt, EOFError):
        break

    if not user_input:
        continue

    if user_input.lower() in ("quit", "exit"):
        print("Au revoir !")
        break

    try:
        # On passe les variables attendues par le template
        response = chain.invoke({
            "chat_history": chat_history,
            "question": user_input
        })
        
        assistant_reply = response.content
        print(f"\nIA: {assistant_reply}\n")
        
        # Mise à jour de l'historique avec l'échange actuel
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=assistant_reply))

    except Exception as e:
        print(f"\nErreur rencontrée : {e}\n")