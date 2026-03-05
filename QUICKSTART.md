# ⚡ Guia Rápido - Tech News Agent

## 🚀 Comece em 5 minutos

### 1️⃣ Instalação (1 minuto)

```bash
# Instale as dependências
pip install anthropic python-dotenv

# Ou use o arquivo requirements
pip install -r requirements.txt
```

### 2️⃣ Configuração (2 minutos)

**Obtenha sua API key:**
1. Acesse: https://console.anthropic.com/
2. Faça login ou crie uma conta
3. Vá em "API Keys"
4. Clique em "Create Key"
5. Copie a chave (começa com `sk-ant-`)

**Configure no projeto:**

Opção A - Criar arquivo .env (recomendado):
```bash
# Crie o arquivo .env
echo "ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui" > .env
```

Opção B - Exportar no terminal:
```bash
export ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
```

### 3️⃣ Execute (2 minutos)

**Teste rápido:**
```bash
python test_agent.py
```

**Execução completa:**
```bash
python tech_news_agent.py
```

**Resultado:**
- Um arquivo `tech_news_dashboard.html` será criado
- Abra no seu navegador
- Explore as notícias! 🎉

---

## 📱 Uso Diário

### Toda semana:
```bash
python tech_news_agent.py
```

### Resultado:
- Dashboard HTML atualizado
- Notícias dos últimos 7 dias
- Organizadas por categoria
- Com pontos-chave para vídeos

---

## 🎬 Fluxo para YouTubers/Criadores

```
Segunda → Execute o agente
   ↓
Terça → Revise o dashboard
   ↓
Quarta → Escolha os tópicos
   ↓
Quinta → Use os pontos-chave para roteiro
   ↓
Sexta → Grave e publique!
```

---

## 🔧 Personalizações Comuns

### Alterar período de busca:
```python
# No arquivo tech_news_agent.py, linha ~250
agent.run_weekly_collection(days_back=3)  # 3 dias ao invés de 7
```

### Mudar categorias:
```python
# No arquivo tech_news_agent.py, linhas ~25-29
self.categories = {
    'ai_llms': 'IA Generativa e LLMs',
    'hardware': 'Hardware e Chips',  # Nova categoria
    'security': 'Cibersegurança'     # Nova categoria
}
```

### Ajustar queries de busca:
```python
# No arquivo tech_news_agent.py, linhas ~42-58
search_queries = {
    'ai_llms': [
        'latest GPT news',           # Sua query personalizada
        'new AI models 2026',        # Sua query personalizada
    ]
}
```

---

## 🤖 Automação

### Linux/Mac:
```bash
# Edite o cron
crontab -e

# Adicione (executa toda segunda às 8h):
0 8 * * 1 cd /caminho/projeto && python3 tech_news_agent.py
```

### Windows:
1. Agendador de Tarefas
2. Criar Tarefa Básica
3. Semanal → Segunda-feira → 08:00
4. Programa: `python`
5. Argumentos: `tech_news_agent.py`

---

## ❓ Problemas Comuns

### "API key não encontrada"
✅ Verifique se o arquivo `.env` existe e está correto

### "Poucas notícias"
✅ Aumente `days_back` para 14 ou 30 dias

### "Dashboard não abre"
✅ Clique com botão direito → Abrir com → Navegador

### "Erro de importação"
✅ Execute: `pip install -r requirements.txt`

---

## 💰 Custos

- **Claude API**: ~$0.01 a $0.05 por execução
- **Mensal** (semanal): ~$0.20/mês
- Muito mais barato que ferramentas pagas! 💪

---

## 🎯 Próximos Passos

- [ ] Execute o `test_agent.py`
- [ ] Revise seu primeiro dashboard
- [ ] Ajuste as categorias se necessário
- [ ] Configure automação semanal
- [ ] Crie seu primeiro vídeo! 🎬

---

**Dúvidas? Leia o README.md completo!**
