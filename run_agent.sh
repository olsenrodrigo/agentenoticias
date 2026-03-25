#!/bin/bash
# Script para executar o Tech News Agent manualmente
cd /opt/tech-news-agent
source venv/bin/activate
set -a
source .env
set +a

python3 -u tech_news_agent.py

echo "$(date): Agente executado com sucesso" >> agent.log
