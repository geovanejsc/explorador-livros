
import yaml
import os

# Carregar o arquivo de configuração
with open("config.yaml","r") as file:
    config = yaml.safe_load(file)

openai_key = config["OPENAI_API_KEY"]
print(openai_key)