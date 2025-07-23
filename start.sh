#!/bin/bash

set -e  # Sai imediatamente se um comando falhar
set -o pipefail  # Falha se qualquer comando em um pipeline falhar

log() {
  echo -e "\n\033[1;34m[INFO]\033[0m $1"
}

error_exit() {
  echo -e "\n\033[1;31m[ERRO]\033[0m $1"
  exit 1
}

log "Criando ambiente virtual..."
python3 -m venv venv || error_exit "Falha ao criar o ambiente virtual."
log "Ambiente virtual criado com sucesso."

log "Ativando ambiente virtual..."
source venv/bin/activate || error_exit "Não foi possível ativar o ambiente virtual."

log "Instalando dependências do Python..."
pip3 install --upgrade pip
pip3 install -r requirements.txt || error_exit "Erro ao instalar requirements.txt"
log "Dependências do Python instaladas com sucesso."

log "Instalando dependências do Node.js..."
cd reverso_scraper || error_exit "Pasta reverso_scraper não encontrada."

npm install || error_exit "Erro ao rodar 'npm install'"
npx playwright install || error_exit "Erro ao rodar 'npx playwright install'"

cd .. || error_exit "Erro ao voltar para o diretório anterior."
log "Dependências do Node.js instaladas com sucesso."

log "✅ Tudo concluído com sucesso!"
