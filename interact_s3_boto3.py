#
## Script python utilizado para efetuar upload do arquivo MICRODADOS_ENEM_2020.csv para um Bucket S3 do AWS
#

import boto3
import pandas as pd
import os
import io
import requests
import zipfile
import wget
import urllib3

urllib3.disable_warnings()

## Baixa o arquivo zip, descompacta e salva em pasta local no computador
URL = 'https://download.inep.gov.br/microdados/microdados_enem_2020.zip'

response = requests.get(URL, verify = False, stream = True)

file = zipfile.ZipFile(io.BytesIO(response.content))
path = './data'
os.makedirs(path, exist_ok = True)
file.extractall(path)

# Cria um client para interagir com o AWS S3
s3 = boto3.client('s3')

# Efetua download de um arquivo do AWS S3 para o disco local
# s3.download_file("datalake-jorge-igti-mba-engenharia-dados",
#                  "data/ITENS_PROVA_2020.csv",
#                  "data/ITENS_PROVA_2020.csv")

# csvFile = path + "/DADOS/MICRODADOS_ENEM_2020.csv";
# print (csvFile)

# Le o arquivo csv e mostra em formato de tabela (separador ;)
# df = pd.read_csv(csvFile, encoding='utf8', sep=";")
# print(df)

# Faz upload do arquivo MICRODADOS_ENEM_2020.csv para a pasta raw-data do AWS S3
s3.upload_file("data/MICRODADOS_ENEM_2020.csv",
              "datalake-jorge-igti-tf-producao-431738431676",
              "raw-data/MICRODADOS_ENEM_2020.csv")
