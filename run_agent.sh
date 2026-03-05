#!/bin/bash
# Script para executar o Tech News Agent automaticamente

# Diretório do projeto
cd "/Users/olsenrodrigo/Google Drive/Meu Drive/Claude/AgenteBuscaNoticias"

# Carregar variáveis de ambiente
export $(cat .env | xargs)

# Executar o agente (teste completo)
/usr/bin/python3 tech_news_agent.py

# Log de execução
echo "$(date): Agente executado com sucesso" >> agent_log.txt
