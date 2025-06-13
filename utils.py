def reforcar_resposta_em_portugues(resposta: str) -> str:
    if "Language Reference" in resposta or "section" in resposta.lower():
        return resposta + "\n\n🤖 Esta explicação foi gerada com base na documentação oficial da Oracle. Tradução automática para português."
    return resposta
