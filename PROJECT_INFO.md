# 📊 Informações do Projeto Audiper

## 🎯 Objetivo

Criar um sistema de auditoria contábil automatizada que processa arquivos SPED ECD e identifica inconsistências contábeis, especialmente saldos invertidos.

## 🏗️ Arquitetura

### Camadas

```
┌─────────────────────────────────────┐
│   Interface (Streamlit)             │  app.py
│   - Upload de arquivo               │
│   - Visualização de dados           │
│   - Download de relatório           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│   Lógica de Negócio (Core)          │  core/
│   - Leitura SPED                    │
│   - Testes de auditoria             │
│   - Exportação de dados             │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│   Dados                             │  dados_demo/
│   - Processamento com Polars        │
│   - Geração de dados demo           │
└─────────────────────────────────────┘
```

## 📦 Dependências Principais

| Pacote | Versão | Função |
|--------|--------|--------|
| streamlit | 1.28+ | Framework web |
| polars | 0.20+ | Processamento de dados (ultra rápido) |
| xlsxwriter | 3.1+ | Geração de Excel |
| pandas | - | Suporte adicional |

## 🔄 Fluxo de Dados

1. **Upload** → Arquivo SPED (.txt)
2. **Parsing** → Extração de registros (I050, I155)
3. **Processamento** → Limpeza e transformação com Polars
4. **Testes** → Aplicação de regras de auditoria
5. **Visualização** → Exibição de achados
6. **Exportação** → Geração de relatório Excel

## 🧪 Testes Implementados

### ✅ Saldos Invertidos (PTA-01)

**Objetivo:** Identificar contas com natureza de saldo invertida

**Regras:**
- Ativo (começa com 1) + Saldo Credor (C) = ERRO 🔴
- Passivo (começa com 2) + Saldo Devedor (D) = ERRO 🔴
- PL (começa com 3) + Saldo Devedor (D) = AVISO 🟡

**Exceções (não são erros):**
- Depreciação Acumulada
- Provisão para Devedores Duvidosos
- Prejuízos Acumulados
- Amortização Acumulada
- Redução de Valor

## 📂 Estrutura de Diretórios

```
audiper-mvp/
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências
├── README.md                       # Documentação
├── DEPLOY_GUIDE.md                # Guia de deploy
├── INSTRUCOES_RAPIDAS.txt         # Instruções rápidas
├── PROJECT_INFO.md                # Este arquivo
│
├── core/                           # Lógica de negócio
│   ├── __init__.py
│   ├── leitor_sped.py             # Parser SPED
│   │   - carregar_arquivo_upload()
│   │   - processar_sped_ecd()
│   │
│   ├── testes_auditoria.py        # Testes
│   │   - teste_saldos_invertidos()
│   │   - gerar_resumo_balancete()
│   │   - get_emoji_severidade()
│   │
│   └── exportador.py              # Exportação
│       - exportar_relatorio_completo()
│
├── dados_demo/                     # Dados de demonstração
│   ├── __init__.py
│   └── demo_generator.py          # Gerador de dados fictícios
│       - gerar_dados_demonstracao()
│
├── .streamlit/                     # Configurações
│   └── config.toml                # Tema e visual
│
└── .git/                           # Repositório Git
```

## 🚀 Como Usar

### Localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar
streamlit run app.py

# 3. Acessar
# http://localhost:8501
```

### Na Nuvem (Streamlit Cloud)

```bash
# 1. Fazer push para GitHub
git push origin main

# 2. Conectar em share.streamlit.io
# (Redeploy automático)

# 3. Acessar
# https://audiper-mvp.streamlit.app
```

## 🔐 Segurança

- ✅ Sem armazenamento de dados (processamento em memória)
- ✅ Sem conexão com banco de dados
- ✅ Sem envio de dados para servidores externos
- ✅ Arquivos processados localmente
- ✅ Ideal para dados sensíveis

## 📈 Performance

- **Polars** em vez de Pandas: 10-100x mais rápido
- **Processamento em memória**: Sem I/O desnecessário
- **Filtros otimizados**: Apenas dados relevantes processados

## 🔄 Próximas Melhorias

- [ ] Teste: Caixa Estourado
- [ ] Teste: Variação Horizontal (Ano vs Ano)
- [ ] Teste: Cruzamento ECD x ECF
- [ ] Suporte a múltiplos períodos
- [ ] Gráficos de análise
- [ ] Exportação em PDF
- [ ] Autenticação de usuários
- [ ] Histórico de auditorias

## 👥 Equipe

- **Desenvolvedor:** Audiper Team
- **Versão:** 1.0
- **Data:** Dezembro 2025
- **Status:** MVP (Mínimo Produto Viável)

## 📞 Contato

Para dúvidas ou sugestões, abra uma Issue no GitHub ou contate a equipe de desenvolvimento.

---

**Desenvolvido com ❤️ para Audiper**
