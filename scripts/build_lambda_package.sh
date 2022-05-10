#!/usr/bin/env bash

cd ../infrastructure

# Declara variavel para reutilizacao nas validacoes do diretorio
PACKAGE="package"

# Cria o diretorio e instala as dependencias da funcao lambda
if [ -d $PACKAGE ]
then
    echo "O diretório "$PACKAGE" já existe."
else
    echo "================================================================"
    echo "Criando o diretório "$PACKAGE"..."
    mkdir $PACKAGE
    echo "O diretório "$PACKAGE" foi criado."
    echo "================================================================"
fi

# Declara variavel qye localiza o requirements com as dependencias do projeto
FILE_REQUIREMENTS=../etl/lambda_requirements.txt

if [ -f $FILE_REQUIREMENTS ]
then
    echo "================================================================"
    echo "Instalando dependencias localizadas no "$FILE_REQUIREMENTS""
    pip install --target ./package -r $FILE_REQUIREMENTS
    echo "Dependencias instaladas com sucesso"
    echo "================================================================"
fi

cd $PACKAGE

# Declara variavel que localiza a funcao lambda para reutilizacao no codigo.
LAMBDA_FUNCTION=../../etl/lambda_function.py

# Verifica se o arquivo lambda_function.py existe
if [ -f $LAMBDA_FUNCTION ]
then
    echo "================================================================"
    echo "Copiando funcao Handler..."
    cp -i $LAMBDA_FUNCTION .
    echo "Compactando o arquivo lambda_function_payload.zip"
    zip -r9 ../lambda_function_payload.zip . ## Compacta o pacote para o deploy
    echo "Arquivo compactado com sucesso!"
    echo "================================================================"
fi

cd ..

