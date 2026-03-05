#!/usr/bin/env python3
"""
Script de exemplo/teste do Tech News Agent
Execute este arquivo para testar rapidamente o agente
"""

from dotenv import load_dotenv
load_dotenv()

from tech_news_agent import TechNewsAgent
import os

def test_agent():
    """Testa o agente com uma busca simples"""
    
    print("=" * 70)
    print("🧪 TESTE DO TECH NEWS AGENT")
    print("=" * 70)
    print()
    
    # Verificar API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ERRO: API key não encontrada!")
        print()
        print("Configure sua chave da Anthropic:")
        print("1. Crie um arquivo .env na raiz do projeto")
        print("2. Adicione: ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui")
        print()
        print("Ou exporte diretamente no terminal:")
        print("export ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui")
        return
    
    print("✅ API key encontrada")
    print()
    
    try:
        # Inicializar agente
        print("🤖 Inicializando agente...")
        agent = TechNewsAgent()
        print("✅ Agente inicializado com sucesso!")
        print()
        
        # Opção 1: Teste rápido - buscar apenas uma categoria
        print("📰 Opção de teste:")
        print("1. Teste rápido (apenas IA & LLMs - ~2 min)")
        print("2. Teste completo (todas categorias - ~5 min)")
        print()
        
        choice = input("Escolha (1 ou 2): ").strip()
        print()
        
        if choice == "1":
            # Teste rápido
            print("🔍 Buscando notícias sobre IA e LLMs...")
            raw_news = agent.search_news('ai_llms', days_back=7)
            
            if raw_news:
                print(f"✅ {len(raw_news)} buscas realizadas")
                print()
                print("🧠 Analisando e estruturando notícias...")
                structured = agent.analyze_and_structure_news(raw_news, 'ai_llms')
                print(f"✅ {len(structured)} notícias estruturadas")
                print()
                
                # Mostrar exemplo
                if structured:
                    print("📋 Exemplo de notícia encontrada:")
                    print("-" * 70)
                    news = structured[0]
                    print(f"Título: {news.get('title', 'N/A')}")
                    print(f"Relevância: {news.get('relevance_score', 0)}/10")
                    print(f"Resumo: {news.get('summary', 'N/A')[:150]}...")
                    print("-" * 70)
                    print()
                
                # Gerar mini dashboard
                print("📊 Gerando dashboard...")
                all_news = {'ai_llms': structured}
                dashboard_path = agent.generate_dashboard(all_news, 'test_dashboard.html')
                print()
                print("=" * 70)
                print("✅ TESTE CONCLUÍDO COM SUCESSO!")
                print(f"📁 Dashboard de teste: {dashboard_path}")
                print("=" * 70)
            else:
                print("❌ Nenhuma notícia encontrada. Tente aumentar o período.")
        
        elif choice == "2":
            # Teste completo
            print("🔍 Executando coleta completa...")
            print("⏱️  Isso pode levar alguns minutos...")
            print()
            
            dashboard_path = agent.run_weekly_collection(days_back=7)
            
            print()
            print("=" * 70)
            print("✅ TESTE COMPLETO CONCLUÍDO!")
            print(f"📁 Dashboard completo: {dashboard_path}")
            print("=" * 70)
        
        else:
            print("❌ Opção inválida. Execute novamente e escolha 1 ou 2.")
    
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERRO DURANTE O TESTE")
        print("=" * 70)
        print(f"Mensagem: {e}")
        print()
        print("Possíveis soluções:")
        print("- Verifique sua conexão com a internet")
        print("- Verifique se a API key está correta")
        print("- Verifique se você tem créditos na conta Anthropic")


if __name__ == "__main__":
    test_agent()
