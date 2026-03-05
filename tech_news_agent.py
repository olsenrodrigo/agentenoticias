#!/usr/bin/env python3
"""
Tech News Agent - Busca e organiza notícias de tecnologia e IA
Desenvolvido para criadores de conteúdo em vídeo
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import anthropic

class TechNewsAgent:
    def __init__(self, api_key=None):
        """
        Inicializa o agente de notícias
        
        Args:
            api_key: Chave da API Anthropic (opcional, usa variável de ambiente se não fornecida)
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key não encontrada. Configure ANTHROPIC_API_KEY ou passe como parâmetro.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.search_model = "claude-haiku-4-5-20251001"  # Rápido e com rate limits altos para buscas
        self.analysis_model = "claude-sonnet-4-5-20250929"  # Mais capaz para análise
        self.max_retries = 5
        self.categories = {
            'ai_llms': 'IA Generativa e LLMs',
            'startups': 'Startups e Investimentos Tech',
            'development': 'Desenvolvimento e Programação'
        }
        
    def _api_call_with_retry(self, **kwargs):
        """Faz chamada à API com retry automático para rate limit (429)"""
        for attempt in range(self.max_retries):
            try:
                return self.client.messages.create(**kwargs)
            except anthropic.RateLimitError as e:
                wait_time = 60 * (attempt + 1)  # 60s, 120s, 180s
                print(f"   ⏳ Rate limit atingido, aguardando {wait_time}s (tentativa {attempt + 1}/{self.max_retries})...")
                time.sleep(wait_time)
                if attempt == self.max_retries - 1:
                    raise
        return None

    def search_news(self, category, days_back=7):
        """
        Busca notícias para uma categoria específica
        
        Args:
            category: Categoria de notícias
            days_back: Quantos dias atrás buscar
            
        Returns:
            Lista de notícias encontradas
        """
        # Fontes brasileiras prioritárias
        self.brazilian_sources = [
            'canaltech.com.br',
            'olhardigital.com.br',
            'tecmundo.com.br',
            'itforum.com.br',
            'techtudo.com.br'
        ]

        search_queries = {
            'ai_llms': [
                # Fontes BR específicas
                'inteligência artificial site:canaltech.com.br OR site:olhardigital.com.br OR site:tecmundo.com.br',
                'IA generativa LLM site:techtudo.com.br OR site:itforum.com.br',
                # Internacional
                'latest AI LLM news OpenAI Anthropic Google'
            ],
            'startups': [
                # Fontes BR específicas
                'startups investimento site:canaltech.com.br OR site:olhardigital.com.br OR site:itforum.com.br',
                'venture capital tecnologia Brasil',
                # Internacional
                'tech startup funding Series A B C'
            ],
            'development': [
                # Fontes BR específicas
                'programação desenvolvimento site:canaltech.com.br OR site:tecmundo.com.br OR site:olhardigital.com.br',
                'ferramentas programação novidades',
                # Internacional
                'developer tools programming languages release'
            ]
        }
        
        queries = search_queries.get(category, [])
        all_news = []
        
        for i, query in enumerate(queries):
            # Delay entre requisições para respeitar rate limit (30k tokens/min)
            if i > 0:
                time.sleep(30)
            try:
                message = self._api_call_with_retry(
                    model=self.search_model,
                    max_tokens=4096,
                    tools=[{
                        "type": "web_search_20250305",
                        "name": "web_search"
                    }],
                    messages=[{
                        "role": "user",
                        "content": f"Search for: {query}. Focus on news from the last {days_back} days. Prioritize Brazilian and Portuguese-language sources when available. Return the top 5 most relevant and recent articles with titles, URLs, and brief summaries."
                    }]
                )
                
                # Processar resposta
                for block in message.content:
                    if block.type == "text":
                        all_news.append({
                            'query': query,
                            'content': block.text,
                            'timestamp': datetime.now().isoformat()
                        })
                        
            except Exception as e:
                print(f"Erro ao buscar '{query}': {e}")
                continue
                
        return all_news
    
    def analyze_and_structure_news(self, raw_news, category):
        """
        Analisa e estrutura as notícias brutas em formato organizado
        
        Args:
            raw_news: Notícias brutas da busca
            category: Categoria das notícias
            
        Returns:
            Lista estruturada de notícias
        """
        combined_content = "\n\n".join([item['content'] for item in raw_news])

        # Truncar conteúdo para caber no rate limit de 30k tokens/min
        max_chars = 40000  # ~10k tokens
        if len(combined_content) > max_chars:
            combined_content = combined_content[:max_chars] + "\n\n[... conteúdo truncado por limite de tamanho ...]"

        # Delay antes de processar para respeitar rate limit
        time.sleep(60)

        try:
            message = self._api_call_with_retry(
                model=self.analysis_model,
                max_tokens=8192,
                messages=[{
                    "role": "user",
                    "content": f"""Analise as seguintes notícias sobre {self.categories[category]} e retorne um JSON array com as notícias mais relevantes e recentes.

IMPORTANTE: Todo o conteúdo DEVE estar em português brasileiro. Se a notícia original estiver em inglês ou outro idioma, traduza o título, resumo e pontos-chave para português.

Para cada notícia, inclua:
- title: título da notícia (em português)
- url: link para a fonte (se disponível)
- summary: resumo em 2-3 frases (em português)
- key_points: array com 3-4 pontos-chave para discussão em vídeo (em português)
- relevance_score: 1-10 (quão relevante/importante é a notícia)
- date: data estimada da notícia
- source: nome da fonte
- region: "br" se for de fonte brasileira (canaltech, olhardigital, tecmundo, itforum, techtudo, tecnoblog, etc.) ou "world" se for fonte internacional
- original_language: idioma original da notícia (pt, en, etc.)

Fontes brasileiras conhecidas: Canaltech, Olhar Digital, TecMundo, IT Forum, TechTudo, Tecnoblog, Exame, InfoMoney, Valor Econômico, Folha, Estadão, G1.

Priorize notícias de fontes brasileiras. Se não houver notícias suficientes em português, inclua as melhores notícias internacionais traduzidas.

Retorne APENAS o JSON array, sem markdown ou explicações adicionais.

Conteúdo das buscas:
{combined_content}"""
                }]
            )
            
            # Extrair JSON da resposta
            response_text = message.content[0].text.strip()
            # Remover possíveis markdown
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            
            structured_news = json.loads(response_text)
            return structured_news
            
        except Exception as e:
            print(f"Erro ao estruturar notícias: {e}")
            return []
    
    def generate_dashboard(self, all_news, output_path='tech_news_dashboard.html'):
        """
        Gera dashboard HTML interativo
        
        Args:
            all_news: Dicionário com todas as notícias por categoria
            output_path: Caminho do arquivo HTML de saída
        """
        now = datetime.now()
        week_start = (now - timedelta(days=7)).strftime('%d/%m/%Y')
        week_end = now.strftime('%d/%m/%Y')
        
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech News Dashboard - {week_start} a {week_end}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .period {{
            color: #666;
            font-size: 1.1em;
        }}
        
        .filters {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        .filter-btn:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}
        
        .filter-btn.active {{
            background: #667eea;
            color: white;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 300px;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1em;
            transition: border-color 0.3s;
        }}
        
        .search-box:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .category-section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .category-title {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}
        
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .news-card {{
            border: 2px solid #f0f0f0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
            background: #fafafa;
        }}
        
        .news-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
            border-color: #667eea;
        }}
        
        .news-title {{
            font-size: 1.3em;
            color: #333;
            margin-bottom: 10px;
            font-weight: 600;
            line-height: 1.3;
        }}
        
        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            color: #888;
            font-size: 0.9em;
        }}
        
        .relevance-badge {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85em;
        }}
        
        .news-summary {{
            color: #555;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        
        .key-points {{
            background: #f8f9ff;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        
        .key-points-title {{
            font-weight: 600;
            color: #667eea;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .key-points ul {{
            list-style: none;
            margin-left: 0;
        }}
        
        .key-points li {{
            padding: 5px 0;
            color: #444;
            position: relative;
            padding-left: 20px;
        }}
        
        .key-points li:before {{
            content: "▹";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
        }}
        
        .news-link {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s;
            font-weight: 500;
        }}
        
        .news-link:hover {{
            background: #764ba2;
            transform: translateX(5px);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .hidden {{
            display: none;
        }}

        .filter-group {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .filter-label {{
            font-weight: 600;
            color: #667eea;
        }}

        .region-br {{
            border-left: 4px solid #009c3b;
        }}

        .region-world {{
            border-left: 4px solid #667eea;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 50px;
            padding: 20px;
        }}
        
        @media (max-width: 768px) {{
            .news-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .filters {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Tech News Dashboard</h1>
            <p class="period">Período: {week_start} - {week_end}</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="totalNews">0</div>
                <div class="stat-label">Total Notícias</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="brNews">0</div>
                <div class="stat-label">🇧🇷 Brasil</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="worldNews">0</div>
                <div class="stat-label">🌎 Mundo</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avgRelevance">0</div>
                <div class="stat-label">Relevância Média</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <span class="filter-label">Categoria:</span>
                <button class="filter-btn active" data-category="all">Todas</button>
                <button class="filter-btn" data-category="ai_llms">IA & LLMs</button>
                <button class="filter-btn" data-category="startups">Startups</button>
                <button class="filter-btn" data-category="development">Desenvolvimento</button>
            </div>
            <div class="filter-group">
                <span class="filter-label">Região:</span>
                <button class="filter-btn region-filter active" data-region="all">Todas</button>
                <button class="filter-btn region-filter" data-region="br">🇧🇷 Brasil</button>
                <button class="filter-btn region-filter" data-region="world">🌎 Mundo</button>
            </div>
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Buscar notícias...">
        </div>
        
        <div id="newsContainer">
"""
        
        # Adicionar notícias por categoria
        for category, news_list in all_news.items():
            if not news_list:
                continue
                
            category_name = self.categories[category]
            html_content += f"""
            <div class="category-section" data-category="{category}">
                <h2 class="category-title">{category_name}</h2>
                <div class="news-grid">
"""
            
            for news in sorted(news_list, key=lambda x: x.get('relevance_score', 0), reverse=True):
                title = news.get('title', 'Sem título')
                summary = news.get('summary', '')
                url = news.get('url', '#')
                source = news.get('source', 'Fonte desconhecida')
                date = news.get('date', 'Data não disponível')
                relevance = news.get('relevance_score', 0)
                key_points = news.get('key_points', [])
                original_language = news.get('original_language', 'pt')
                translated_badge = ' 🌐 Traduzido' if original_language != 'pt' else ''
                region = news.get('region', 'world')
                region_badge = '🇧🇷' if region == 'br' else '🌎'
                region_class = 'region-br' if region == 'br' else 'region-world'
                
                key_points_html = ""
                if key_points:
                    key_points_items = "".join([f"<li>{point}</li>" for point in key_points])
                    key_points_html = f"""
                    <div class="key-points">
                        <div class="key-points-title">🎬 Pontos para o vídeo:</div>
                        <ul>{key_points_items}</ul>
                    </div>
"""
                
                html_content += f"""
                    <div class="news-card {region_class}" data-category="{category}" data-region="{region}" data-title="{title.lower()}" data-summary="{summary.lower()}">
                        <h3 class="news-title">{region_badge} {title}</h3>
                        <div class="news-meta">
                            <span>📅 {date} | 📰 {source}{translated_badge}</span>
                            <span class="relevance-badge">⭐ {relevance}/10</span>
                        </div>
                        <p class="news-summary">{summary}</p>
                        {key_points_html}
                        <a href="{url}" class="news-link" target="_blank">Ler mais →</a>
                    </div>
"""
            
            html_content += """
                </div>
            </div>
"""
        
        html_content += """
        </div>
        
        <footer>
            <p>Dashboard gerado automaticamente pelo Tech News Agent 🤖</p>
            <p>Última atualização: """ + now.strftime('%d/%m/%Y às %H:%M') + """</p>
        </footer>
    </div>
    
    <script>
        // Filtros de categoria e região
        const categoryBtns = document.querySelectorAll('.filter-btn:not(.region-filter)');
        const regionBtns = document.querySelectorAll('.filter-btn.region-filter');
        const newsCards = document.querySelectorAll('.news-card');
        const categorySections = document.querySelectorAll('.category-section');
        const searchBox = document.getElementById('searchBox');

        let activeCategory = 'all';
        let activeRegion = 'all';

        categoryBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                categoryBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeCategory = btn.dataset.category;
                applyFilters();
            });
        });

        regionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                regionBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeRegion = btn.dataset.region;
                applyFilters();
            });
        });

        searchBox.addEventListener('input', applyFilters);

        function applyFilters() {
            const searchTerm = searchBox.value.toLowerCase();

            categorySections.forEach(section => {
                const category = section.dataset.category;
                const cards = section.querySelectorAll('.news-card');
                let visibleCards = 0;

                cards.forEach(card => {
                    const matchesCategory = activeCategory === 'all' || card.dataset.category === activeCategory;
                    const matchesRegion = activeRegion === 'all' || card.dataset.region === activeRegion;
                    const matchesSearch = searchTerm === '' ||
                                        card.dataset.title.includes(searchTerm) ||
                                        card.dataset.summary.includes(searchTerm);

                    if (matchesCategory && matchesRegion && matchesSearch) {
                        card.classList.remove('hidden');
                        visibleCards++;
                    } else {
                        card.classList.add('hidden');
                    }
                });

                if (activeCategory === 'all' && visibleCards === 0) {
                    section.classList.add('hidden');
                } else if (activeCategory !== 'all' && category !== activeCategory) {
                    section.classList.add('hidden');
                } else if (visibleCards === 0) {
                    section.classList.add('hidden');
                } else {
                    section.classList.remove('hidden');
                }
            });
        }
        
        // Calcular estatísticas
        function calculateStats() {
            const allCards = document.querySelectorAll('.news-card');
            const totalNews = allCards.length;
            const brCards = document.querySelectorAll('.news-card[data-region="br"]').length;
            const worldCards = document.querySelectorAll('.news-card[data-region="world"]').length;

            let totalRelevance = 0;
            allCards.forEach(card => {
                const badge = card.querySelector('.relevance-badge');
                if (badge) {
                    const relevance = parseInt(badge.textContent.match(/\\d+/)[0]);
                    totalRelevance += relevance;
                }
            });

            const avgRelevance = totalNews > 0 ? (totalRelevance / totalNews).toFixed(1) : 0;

            document.getElementById('totalNews').textContent = totalNews;
            document.getElementById('brNews').textContent = brCards;
            document.getElementById('worldNews').textContent = worldCards;
            document.getElementById('avgRelevance').textContent = avgRelevance;
        }

        calculateStats();
    </script>
</body>
</html>
"""
        
        # Salvar arquivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard gerado: {output_path}")
        return output_path
    
    def _format_whatsapp_message(self, all_news, dashboard_path, days_back):
        """
        Formata a mensagem de resumo para WhatsApp

        Args:
            all_news: Dicionário com notícias por categoria
            dashboard_path: Caminho do dashboard gerado
            days_back: Dias cobertos pela coleta

        Returns:
            Mensagem formatada para WhatsApp
        """
        now = datetime.now()
        period_start = (now - timedelta(days=days_back)).strftime('%d/%m')
        period_end = now.strftime('%d/%m/%Y')

        # Totais por categoria
        category_counts = {}
        all_items = []
        for category, news_list in all_news.items():
            category_name = self.categories.get(category, category)
            category_counts[category_name] = len(news_list)
            all_items.extend(news_list)

        total = len(all_items)

        # Top 5 por relevância
        top_news = sorted(all_items, key=lambda x: x.get('relevance_score', 0), reverse=True)[:5]

        lines = [
            "*TECH NEWS AGENT*",
            "Relatório Semanal",
            "",
            f"Período: {period_start} - {period_end}",
            f"Total: {total} notícias coletadas",
            "",
            "*POR CATEGORIA:*",
        ]

        for cat_name, count in category_counts.items():
            lines.append(f"  {cat_name}: {count}")

        lines.append("")
        lines.append("*TOP NOTÍCIAS:*")

        for i, news in enumerate(top_news, 1):
            score = news.get('relevance_score', 0)
            title = news.get('title', 'Sem título')
            lines.append(f"{i}. [{score}/10] {title}")

        lines.append("")
        lines.append("Dashboard gerado com sucesso.")
        lines.append(f"Arquivo: {dashboard_path}")

        return "\n".join(lines)

    def _generate_pdf(self, html_path):
        """
        Gera PDF a partir do dashboard HTML

        Args:
            html_path: Caminho do arquivo HTML

        Returns:
            Caminho do PDF gerado, ou None se falhar
        """
        try:
            from weasyprint import HTML
        except ImportError:
            print("   ⚠️  Biblioteca 'weasyprint' não instalada. PDF não será gerado.")
            return None

        try:
            pdf_path = html_path.replace('.html', '.pdf')
            HTML(filename=html_path).write_pdf(pdf_path)
            print(f"   ✅ PDF gerado: {pdf_path}")
            return pdf_path
        except Exception as e:
            print(f"   ⚠️  Falha ao gerar PDF: {e}")
            return None

    def _send_whatsapp_document(self, file_path, caption, api_url, api_key, instance, phone):
        """
        Envia um documento via WhatsApp (Evolution API v1.x)

        Args:
            file_path: Caminho do arquivo a enviar
            caption: Legenda do documento
            api_url, api_key, instance, phone: Credenciais Evolution API

        Returns:
            True se enviou com sucesso, False caso contrário
        """
        import requests
        import base64

        try:
            with open(file_path, 'rb') as f:
                file_b64 = base64.b64encode(f.read()).decode('utf-8')

            file_name = os.path.basename(file_path)
            url = f"{api_url.rstrip('/')}/message/sendMedia/{instance}"
            headers = {
                "apikey": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "number": phone,
                "mediaMessage": {
                    "mediatype": "document",
                    "fileName": file_name,
                    "media": file_b64,
                    "caption": caption
                }
            }

            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            print(f"   ✅ Documento enviado: {file_name}")
            return True
        except Exception as e:
            print(f"   ⚠️  Falha ao enviar documento {file_path}: {e}")
            return False

    def _send_whatsapp_notification(self, all_news, dashboard_path, days_back):
        """
        Envia notificação WhatsApp via Evolution API

        Args:
            all_news: Dicionário com notícias por categoria
            dashboard_path: Caminho do dashboard gerado
            days_back: Dias cobertos pela coleta

        Returns:
            True se enviou com sucesso, False caso contrário
        """
        try:
            import requests
        except ImportError:
            print("   ⚠️  Biblioteca 'requests' não instalada. Execute: pip install requests")
            return False

        try:
            api_url = os.environ.get('EVOLUTION_API_URL', '').strip()
            api_key = os.environ.get('EVOLUTION_API_KEY', '').strip()
            instance = os.environ.get('EVOLUTION_INSTANCE', '').strip()
            phone = os.environ.get('WHATSAPP_PHONE', '').strip()

            if not api_url:
                print("   ℹ️  WhatsApp não configurado (EVOLUTION_API_URL vazia). Pulando notificação.")
                return False

            if not all([api_key, instance, phone]):
                print("   ⚠️  Configuração WhatsApp incompleta. Verifique EVOLUTION_API_KEY, EVOLUTION_INSTANCE e WHATSAPP_PHONE no .env")
                return False

            message = self._format_whatsapp_message(all_news, dashboard_path, days_back)

            url = f"{api_url.rstrip('/')}/message/sendText/{instance}"
            headers = {
                "apikey": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "number": phone,
                "textMessage": {"text": message}
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            print("   ✅ Resumo em texto enviado!")

            # Enviar HTML como documento
            self._send_whatsapp_document(
                dashboard_path, "Dashboard HTML - Tech News Agent",
                api_url, api_key, instance, phone
            )

            # Enviar PDF se existir
            pdf_path = dashboard_path.replace('.html', '.pdf')
            if os.path.exists(pdf_path):
                self._send_whatsapp_document(
                    pdf_path, "Dashboard PDF - Tech News Agent",
                    api_url, api_key, instance, phone
                )

            return True

        except Exception as e:
            print(f"   ⚠️  Falha ao enviar WhatsApp: {e}")
            return False

    def run_weekly_collection(self, days_back=7):
        """
        Executa a coleta semanal completa de notícias
        
        Args:
            days_back: Quantos dias atrás buscar notícias
            
        Returns:
            Caminho do dashboard gerado
        """
        print("🔍 Iniciando busca de notícias...")
        all_news = {}
        
        for category in self.categories.keys():
            print(f"\n📰 Buscando: {self.categories[category]}")
            raw_news = self.search_news(category, days_back)
            
            if raw_news:
                print(f"   ✓ {len(raw_news)} buscas realizadas")
                structured = self.analyze_and_structure_news(raw_news, category)
                all_news[category] = structured
                print(f"   ✓ {len(structured)} notícias estruturadas")
            else:
                print(f"   ✗ Nenhuma notícia encontrada")
                all_news[category] = []
        
        print("\n📊 Gerando dashboard...")
        dashboard_path = self.generate_dashboard(all_news)

        # Gerar PDF do dashboard
        print("\n📄 Gerando PDF...")
        self._generate_pdf(dashboard_path)

        # Enviar notificação WhatsApp
        print("\n📱 Enviando notificação WhatsApp...")
        self._send_whatsapp_notification(all_news, dashboard_path, days_back)

        return dashboard_path


def main():
    """Função principal para execução standalone"""
    print("=" * 60)
    print("🤖 Tech News Agent - Coletor de Notícias Tech & IA")
    print("=" * 60)
    
    try:
        agent = TechNewsAgent()
        dashboard_path = agent.run_weekly_collection(days_back=7)
        
        print("\n" + "=" * 60)
        print("✅ Processo concluído com sucesso!")
        print(f"📁 Dashboard disponível em: {dashboard_path}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
