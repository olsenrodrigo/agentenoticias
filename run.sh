#!/bin/bash
# Tech News Agent - Execução automática semanal
cd /opt/tech-news-agent
source venv/bin/activate
set -a
source .env
set +a

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando coleta de notícias..." >> /opt/tech-news-agent/agent.log
python3 -u tech_news_agent.py >> /opt/tech-news-agent/agent.log 2>&1
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Coleta finalizada." >> /opt/tech-news-agent/agent.log
echo '---' >> /opt/tech-news-agent/agent.log
