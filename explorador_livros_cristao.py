import streamlit as st
import yaml
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import json
import openai
import tempfile
from pathlib import Path

# with open("config.yaml","r") as file:
#     config= yaml.safe_load(file)
# openai_key = config["OPENAI_API_KEY"]

openai_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

with open('sumario_livro.json', 'r') as file:
    sumario_livro = json.load(file)




template='''
Você é um professor cristão com profunda sabedoria bíblica e excelente didática, inspirado pelo estilo devocional, apaixonado e teológico de Charles Spurgeon.

Explique o conteúdo do capítulo: "{capitulo}" do livro "Descobrindo a sua identidade em Cristo, seja sua melhor versão" de Charles Spurgeon, como se estivesse ensinando para uma pessoa ocupada, mas com sede de aprender mais de Deus.

Use um estilo de explicação: {estilo}  
Profundidade: {profundidade}

Incorpore a linguagem bíblica reverente e o tom inspirador que Spurgeon usaria. Fale ao coração, mas também à mente.

Inclua:
- Um resumo claro e fiel do conteúdo
- Exemplos e histórias do cotidiano ou parábolas que facilitem a compreensão
- Aplicações práticas para a vida cristã hoje
- Versículos bíblicos relevantes com breves comentários
- Perguntas reflexivas que levem o leitor a um exame pessoal
- Sugestões de oração que se alinhem ao tema

Torne a explicação acessível, impactante e envolvente, mesmo para alguém que tenha poucos minutos por dia — como se fosse uma aula devocional compacta, mas poderosa.

 '''

prompt_template = PromptTemplate.from_template(template)

st.title('Explorador de Livro Cristão:')
st.subheader('LIVRO: Descobrindo sua identidade em Cristo')
st.write('''Este aplicativo gera conteúdo inspirado no  livro "Descobrindo a sua identidade em Cristo" de Charles Spurgeon.''')

# Selecionar Parte
part_titles = [part["title"] for part in sumario_livro["parts"]]
selected_part = st.selectbox("Escolha uma parte do livro", part_titles)

# Selecionar Subtópico
selected_topics = next(part["topics"] for part in sumario_livro["parts"] if part["title"] == selected_part)
selected_topic = st.radio("Escolha um tema específico", selected_topics)

estilo = st.selectbox("Escolha o estilo da explicação", [
    "Devocional simples",
    "Devocional com profundidade teológica",
    "Explicação pastoral",
    "Estudo bíblico estruturado",
    "Conversa informal entre irmãos na fé",
    "Reflexão poética e inspiradora"
])

profundidade = st.selectbox("Escolha a profundidade do conteúdo", [
    "Leve (para iniciantes ou pessoas com pouco tempo)",
    "Intermediária (equilíbrio entre doutrina e prática)",
    "Profunda (com base teológica sólida)"
])

if st.button('Gerar Explicação'):
    with st.spinner('Gerando explicação...'):
        prompt = prompt_template.format(capitulo=selected_topic, estilo=estilo, profundidade=profundidade)
        resposta = chat_model.invoke(prompt)
        st.success('Explicação gerada com sucesso!')
        st.subheader('Explicação Gerada:')
        st.write(resposta.content)
        st.download_button(
            label="Baixar Explicação",
            data=resposta.content,
            file_name="explicacao_livro.txt",
            mime="text/plain"
        )
        with st.spinner('Gerando áudio...'):
        # Inicializa cliente OpenAI (opcional se já estiver com a env var)
            client = openai.OpenAI(api_key=openai_key)

        # Gera o áudio com a voz desejada
            audio_response = client.audio.speech.create(
                model="tts-1",  # ou "tts-1-hd" para mais qualidade
                voice="onyx",   # vozes disponíveis: "nova", "alloy", "echo", "fable", "onyx", "shimmer"
                input=resposta.content
            )
            # Salva em um arquivo temporário
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_audio_path = Path(temp_audio.name)
            temp_audio.write(audio_response.content)
            temp_audio.close()
            # Player no Streamlit
            st.audio(str(temp_audio_path), format='audio/mp3')

            # Botão para download
            with open(temp_audio_path, "rb") as file:
                st.download_button(
                    label="Baixar Áudio",
                    data=file,
                    file_name="explicacao_audio.mp3",
                    mime="audio/mpeg"
                )