"""ALTAB: tutor de APC que responde dúvidas de alunos usando o Ollama."""

import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/chat"  # API local do Ollama
MODELO = "qwen3.5:4b"
NOME_PLATAFORMA = "ALTAB"

# Instruções que definem o comportamento do tutor
PROMPT_SISTEMA = """
Você é o tutor do ALTAB, uma plataforma de apoio à disciplina de Algoritmos e Programação de Computadores (APC) em Python.
Seu objetivo é fazer o aluno aprender, não apenas entregar respostas prontas.

Regras:
1. Responda em português, com linguagem simples e clara.
2. Antes de dar a solução completa, faça perguntas que ajudem o aluno a raciocinar.
3. Quando mostrar código, use exemplos curtos e comentados.
4. Se o aluno pedir a resposta de um exercício, dê uma dica e peça que ele tente antes.
5. Se não tiver certeza de algo, diga isso e sugira conferir na documentação oficial do Python.
6. Nunca invente fontes, bibliotecas ou funções.
"""

st.set_page_config(page_title=f"{NOME_PLATAFORMA} - Tutor de APC", page_icon="🎓")
st.title(f"{NOME_PLATAFORMA}: tire suas dúvidas de APC")

# Guarda o histórico da conversa enquanto a página estiver aberta
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Mostra as mensagens anteriores
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada e resposta do tutor
pergunta = st.chat_input("Digite sua dúvida sobre Python...")

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # O prompt do sistema vem primeiro, seguido do histórico
    historico = [{"role": "system", "content": PROMPT_SISTEMA}] + st.session_state.mensagens

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                r = requests.post(
                    OLLAMA_URL,
                    json={"model": MODELO, "messages": historico, "stream": False},
                    timeout=300,  # o modelo pode ser lento em computadores sem GPU
                )
                r.raise_for_status()
                resposta = r.json()["message"]["content"]
            except requests.RequestException as erro:
                resposta = (
                    "Não consegui falar com o modelo. Verifique se o Ollama está rodando "
                    f"em http://localhost:11434. Detalhe: {erro}"
                )
        st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})