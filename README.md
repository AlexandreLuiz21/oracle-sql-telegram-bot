# 🤖 Bot Telegram Oracle SQL com LangChain + Gemini

Este é um bot que responde perguntas sobre Oracle SQL via Telegram. Ele usa IA para entender o que o usuário pergunta e busca a resposta na documentação oficial da Oracle.

---

## 🎯 Objetivo

Criar um bot inteligente, em português, que ajude desenvolvedores e DBAs com dúvidas sobre comandos e conceitos do Oracle SQL. O bot busca a resposta no conteúdo oficial e entrega de forma clara, com exemplos práticos sempre que possível.

---

## 🚧 O que esse projeto usa

### ✅ LangChain

O LangChain ajuda a conectar a IA com fontes externas (como documentos PDF). Ele:

- Carrega os PDFs da documentação da Oracle (`sql-language-reference.pdf` e `database-backup-and-recovery-reference.pdf`);
- Combina o conteúdo de ambos os documentos;
- Quebra o conteúdo combinado em partes menores;
- Gera vetores para facilitar a busca semântica (com FAISS) em toda a base de conhecimento;
- Utiliza a técnica de Retrieval Augmented Generation (RAG) para encontrar os trechos mais relevantes nos documentos e, com base neles, usa a IA para gerar respostas.

### ✅ Gemini

O Gemini é o modelo de linguagem da Google (tipo ChatGPT). Aqui, usamos:

- `gemini-2.0-flash` para gerar respostas rápidas;
- `embedding-001` para transformar textos em vetores e comparar a pergunta com o conteúdo.

### ✅ Embeddings

Transformam textos em números (vetores). Assim, a IA entende qual trecho do PDF tem mais a ver com a pergunta feita.

### ✅ PromptTemplate

O prompt é o texto que "instrui" a IA. Criamos um template que:

- Obriga a IA a responder sempre em português;
- Incentiva que as respostas sejam **curtas e objetivas**;
- Gera exemplos de código quando o usuário pedir.

Exemplo do prompt usado:

```python
Você é um assistente DBA especializado em Oracle. Responda sempre em português de forma clara, objetiva e profissional.

Se a pergunta pedir um exemplo (como comandos SQL), gere um exemplo real baseado no contexto. 
Se não houver exemplo no contexto, use seu conhecimento para gerar um com base na pergunta.

Evite respostas muito longas, mas forneça código ou exemplos quando forem úteis.
