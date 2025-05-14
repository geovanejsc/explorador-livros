import streamlit as st
import yaml
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Carregar o arquivo de configuração
with open("config.yaml","r") as file:
    config = yaml.safe_load(file)

openai_key = config["OPENAI_API_KEY"]
os.environ["OPENAI_API_KEY"] = openai_key

openai = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

template='''
Você é um analista financeiro. escreva um relatório financeiro detalhado sobre a empresa "{empresa}" para o periodo "{periodo}" 
O relatório deve ser escrito em {idioma} e incluir a seguinte análise:
{analise}

Certifique-se de fornecer insights e conclusões para esta seção.
'''

prompt_template = PromptTemplate.from_template(template)


empresas = ['ACME Corp', 'Globex Corporation', 'Soylent Corp', 'Initech', 'Umbrella Corporation']
trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
anos = [2021, 2022, 2023, 2024]
idiomas = ['Português', 'Inglês', 'Espanhol', 'Francês', 'Alemão']
analises = [
    "Análise do Balanço Patrimonial",
    "Análise do Fluxo de Caixa",
    "Análise de Tendências",
    "Análise de Receita e Lucro",
    "Análise de Posição de Mercado"
]


st.title('Gerador de Relatório Financeiro:')

empresa = st.selectbox('Selecione a empresa:', empresas)
trimestre = st.selectbox('Selecione o trimestre:', trimestres)
ano = st.selectbox('Selecione o ano:', anos)
idioma = st.selectbox('Selecione o idioma:', idiomas)
analise = st.selectbox('Selecione a análise:', analises)
if st.button('Gerar Relatório'):
    with st.spinner('Gerando relatório...'):
        prompt = prompt_template.format(empresa=empresa, periodo=f'{trimestre} {ano}', idioma=idioma, analise=analise)
        resposta = openai.invoke(prompt)
        st.success('Relatório gerado com sucesso!')
        st.subheader('Relatório Gerado:')
        st.write(resposta.content)