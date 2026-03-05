# 🤖 Tech News Agent

Agente inteligente para busca automatizada de notícias sobre tecnologia e IA, com dashboard interativo para criadores de conteúdo em vídeo.

## 🎯 Funcionalidades

- ✅ **Busca automatizada** de notícias nas principais áreas tech
- ✅ **Dashboard HTML interativo** com filtros e busca
- ✅ **Análise inteligente** usando Claude (Anthropic)
- ✅ **Pontos-chave** para roteiro de vídeos
- ✅ **Score de relevância** para priorizar conteúdo
- ✅ **Execução agendada** (semanal, diária ou sob demanda)

## 📋 Categorias Cobertas

1. **IA Generativa e LLMs**
   - Novos modelos e releases
   - Desenvolvimentos em IA generativa
   - Pesquisas e papers relevantes

2. **Startups e Investimentos Tech**
   - Funding rounds
   - Venture capital
   - IPOs e aquisições

3. **Desenvolvimento e Programação**
   - Novas ferramentas e frameworks
   - Linguagens de programação
   - Tendências de desenvolvimento

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave de API da Anthropic ([obter aqui](https://console.anthropic.com/))

### Passo a passo

1. **Clone ou baixe os arquivos do projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure sua API key:**

Crie um arquivo `.env` na raiz do projeto:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave:
```
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
```

## 💻 Uso

### Execução Básica

Execute o agente para coletar notícias da última semana:

```bash
python tech_news_agent.py
```

Isso vai:
1. Buscar notícias nas 3 categorias configuradas
2. Analisar e estruturar o conteúdo
3. Gerar um dashboard HTML interativo
4. Salvar como `tech_news_dashboard.html`

### Uso Programático

Você pode usar o agente em seus próprios scripts:

```python
from tech_news_agent import TechNewsAgent

# Inicializar o agente
agent = TechNewsAgent()

# Coletar notícias dos últimos 7 dias
dashboard_path = agent.run_weekly_collection(days_back=7)

print(f"Dashboard gerado: {dashboard_path}")
```

### Personalização

**Alterar período de busca:**
```python
# Buscar notícias dos últimos 3 dias
agent.run_weekly_collection(days_back=3)
```

**Buscar categoria específica:**
```python
# Buscar apenas notícias de IA
raw_news = agent.search_news('ai_llms', days_back=7)
structured = agent.analyze_and_structure_news(raw_news, 'ai_llms')
```

**Personalizar categorias:**

Edite o dicionário `self.categories` no arquivo `tech_news_agent.py`:

```python
self.categories = {
    'ai_llms': 'IA Generativa e LLMs',
    'startups': 'Startups e Investimentos Tech',
    'development': 'Desenvolvimento e Programação',
    # Adicione suas próprias categorias:
    'hardware': 'Hardware e Chips',
    'security': 'Segurança da Informação'
}
```

## 📊 Dashboard Interativo

O dashboard gerado inclui:

- **Estatísticas gerais**: Total de notícias, categorias, relevância média
- **Filtros por categoria**: Visualize apenas a área de interesse
- **Busca em tempo real**: Encontre notícias específicas
- **Cards informativos** com:
  - Título e fonte
  - Data de publicação
  - Score de relevância (1-10)
  - Resumo executivo
  - Pontos-chave para discussão em vídeo
  - Link para fonte original

### Exemplo de visualização:

```
🚀 Tech News Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Estatísticas
├─ 45 Notícias
├─ 3 Categorias
└─ 7.8 Relevância Média

🔍 Filtros
[Todas] [IA & LLMs] [Startups] [Desenvolvimento]
[Buscar notícias...]

📰 IA Generativa e LLMs
┌─────────────────────────────────┐
│ Nova versão do GPT-5 anunciada  │
│ ⭐ 9/10 | 📅 07/02/2026         │
│                                 │
│ OpenAI anuncia GPT-5 com...    │
│                                 │
│ 🎬 Pontos para o vídeo:        │
│ ▹ Principais melhorias         │
│ ▹ Comparação com versão 4      │
│ ▹ Impacto no mercado           │
│                                 │
│ [Ler mais →]                   │
└─────────────────────────────────┘
```

## 🔄 Automação (Agendamento)

### Linux/Mac (cron)

Para executar semanalmente toda segunda às 8h:

1. Abra o crontab:
```bash
crontab -e
```

2. Adicione a linha:
```bash
0 8 * * 1 cd /caminho/para/projeto && /usr/bin/python3 tech_news_agent.py
```

### Windows (Task Scheduler)

1. Abra o Agendador de Tarefas
2. Criar Tarefa Básica
3. Configure para executar semanalmente
4. Ação: Iniciar programa
5. Programa: `python`
6. Argumentos: `tech_news_agent.py`
7. Diretório inicial: caminho do projeto

### Python (agendamento em código)

```python
import schedule
import time
from tech_news_agent import TechNewsAgent

def job():
    agent = TechNewsAgent()
    agent.run_weekly_collection()

# Executar toda segunda às 8h
schedule.every().monday.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Verifica a cada hora
```

## 🎬 Fluxo de Trabalho para Criadores de Conteúdo

1. **Segunda-feira**: Agente busca notícias automaticamente
2. **Terça-feira**: Revise o dashboard e selecione tópicos
3. **Quarta-feira**: Use os pontos-chave para criar roteiro
4. **Quinta-feira**: Grave os vídeos
5. **Sexta-feira**: Publique o conteúdo

### Dicas para criação de conteúdo:

- Use o **score de relevância** para priorizar assuntos
- Os **pontos-chave** já vêm prontos para discussão
- Acesse as **fontes originais** para detalhes adicionais
- Combine **múltiplas notícias** relacionadas em um vídeo

## 🔧 Solução de Problemas

### Erro de API Key
```
ValueError: API key não encontrada
```
**Solução**: Verifique se o arquivo `.env` está configurado corretamente.

### Poucas notícias retornadas
**Possíveis causas**:
- Período de busca muito curto
- Categorias muito específicas
- Limite de tokens da API atingido

**Solução**: Ajuste o parâmetro `days_back` para um período maior.

### Dashboard não abre no navegador
**Solução**: Abra manualmente o arquivo `tech_news_dashboard.html` em qualquer navegador.

## 📝 Estrutura do Projeto

```
tech-news-agent/
├── tech_news_agent.py      # Script principal
├── requirements.txt         # Dependências Python
├── .env.example            # Exemplo de configuração
├── .env                    # Sua configuração (não commitado)
├── README.md               # Este arquivo
└── tech_news_dashboard.html # Dashboard gerado (criado após execução)
```

## 🆚 Comparação com outras ferramentas

| Recurso | Tech News Agent | Feedly | Manus | Google Alerts |
|---------|----------------|--------|-------|---------------|
| Análise por IA | ✅ | ❌ | ✅ | ❌ |
| Pontos para vídeo | ✅ | ❌ | ❌ | ❌ |
| Dashboard visual | ✅ | ✅ | ✅ | ❌ |
| Gratuito | ✅ | Limitado | ❌ | ✅ |
| Personalizável | ✅ | Limitado | Limitado | Básico |
| Score de relevância | ✅ | ❌ | ❌ | ❌ |

## 🔐 Segurança e Privacidade

- ✅ Suas chaves de API ficam apenas no seu computador
- ✅ Nenhum dado é armazenado em servidores externos
- ✅ O código é open source e auditável
- ✅ Você controla quais notícias são coletadas

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Algumas ideias:

- [ ] Exportar para Notion/Trello
- [ ] Integração com calendário
- [ ] Notificações por email
- [ ] Análise de tendências
- [ ] Geração automática de roteiros

## 📄 Licença

Este projeto é fornecido "como está" para uso pessoal e comercial.

## 🆘 Suporte

Para questões ou problemas:
1. Verifique a seção de Solução de Problemas
2. Revise a documentação da API Anthropic
3. Abra uma issue descrevendo o problema

## 🎉 Próximos Passos

Após executar o agente pela primeira vez:

1. ✅ Abra o `tech_news_dashboard.html` no navegador
2. ✅ Explore as diferentes categorias
3. ✅ Use os filtros e busca
4. ✅ Leia os pontos-chave para seus vídeos
5. ✅ Configure o agendamento semanal
6. ✅ Personalize as categorias conforme necessário

---

**Desenvolvido para criadores de conteúdo que querem se manter atualizados sem perder tempo 🚀**
