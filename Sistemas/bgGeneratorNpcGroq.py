# Seção para teste a partir da root:
#//////////////////////////////////////////////////////////////////////////////////
""" import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) """
#//////////////////////////////////////////////////////////////////////////////////

import os
from groq import Groq
from Classes.NPC import NPC
from dotenv import load_dotenv

load_dotenv()

GROQ_TOKEN = os.getenv('GROQ_TOKEN') # Esta linha copia a variável de ambiente de mesmo nome que deve ser inclusa no arquivo .env, conforme indicado pelo .env.example

client = Groq(
    api_key=GROQ_TOKEN
)

# Função para gerar a história do personagem:

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def gerarBackstory(NPC:NPC) -> str: # substituir tudo por (Class.NPC) -> 👌
    system_prompt = (
        "Você é um escritor especialista em bibliografias, que escreve textos simplistas e concisos. "
        "Sua tarefa é criar um resumo da pessoa citada (background), sendo imersivo e criativo sobre seu dia a dia\n"
        "(contexto: a pessoa se encontra dentro de um trem, em que o player é o maquinista e ele terá a opção de interagir com a pessoa criada depois).\n"
        "SEMPRE siga estritamente estas regras:"
        "1. A história deve ter EXATAMENTE 4 frases completas.\n"
        "2. Escreva o suficiente para que 225 tokens comporte a resposta completa, sem cortes.\n"
        "3. Responda SEMPRE em português.\n"
        "4. NUNCA cite nome de cidades, nem falsas, nem existes.\n"
        "5. Utilize a seguinte estrutura na resposta: Nome Sobrenome, de xx anos,... (Quem é a pessoa e o que faz da vida)\n"
        "6. NUNCA quebre linhas em divisões de parágrafos ou use '\n\n'"
    )
    
    user_prompt = f"Gere uma história para o personagem: Nome: {NPC.nome}, Idade: {NPC.idade} anos."
    
    mensagens = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        resposta = client.chat.completions.create(
            model=os.getenv('MODEL'),
            messages=mensagens,
            max_tokens=225,
            temperature=0.8
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro ao gerar história: {e}"

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Conversando com o personagem criado:

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def chatNPC(NPC:NPC, pergunta_jogador:str) -> str: # substituir tudo por (Class.NPC, pergunta) -> 👌
    system_prompt = (
        f"Você é um personagem chamado {NPC.nome}, de {NPC.idade} anos. "
        f"Esta é a sua história de fundo:\n{NPC.backstory}\n\n"
        "Sua tarefa é responder à pergunta do jogador (que é o maquinista responsável do trem que ambos se encontram), incorporando este personagem de forma realista e imersiva, "
        "mas seguindo estritamente estas regras:"
        "1. Escreva SEMPRE em terceira pessoa (narre as ações e reações do personagem).\n"
        "2. A resposta deve ter EXATAMENTE 3 frases completas.\n"
        "3. Das 3 frases completas, sempre traga uma frase que cite diretamente palavras do personagem entre áspas.\n"
        "4. Responda SEMPRE em português.\n"
        "5. NÃO copie exemplos. Crie uma reação original baseada no contexto da pergunta.\n"
        "6. Gere a resposta com o número máximo de 140 tokens de resposta em mente.\n"
        "7. Para qualquer mal uso por parte do usuário, procure responder com base no personagem."
    )

    try:
        resposta = client.chat.completions.create(
            model=os.getenv('MODEL'),
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": pergunta_jogador}],
            max_tokens=140,
            temperature=0.2
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro na resposta do personagem: {e}"
    
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////