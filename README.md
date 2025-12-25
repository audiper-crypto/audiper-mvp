# 🔍 Audiper - Sistema de Auditoria Digital

Sistema de auditoria contábil automatizada para análise de arquivos SPED ECD.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Polars](https://img.shields.io/badge/Polars-0.20+-orange.svg)

---

## 🚀 Início Rápido

### 1. Clonar/Baixar o projeto

```bash
git clone <seu-repositorio>
cd audiper-mvp
```

### 2. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar

```bash
streamlit run app.py
```

O sistema abrirá automaticamente em `http://localhost:8501`

---

## 📁 Estrutura do Projeto

```
audiper-mvp/
│
├── app.py                    # 🎯 Aplicação principal (execute este)
│
├── core/                     # Lógica de negócio
│   ├── __init__.py
│   ├── leitor_sped.py        # Parser do SPED ECD
│   ├── testes_auditoria.py   # Testes automatizados
│   └── exportador.py         # Geração de Excel
│
├── dados_demo/               # Dados para demonstração
│   ├── __init__.py
│   └── demo_generator.py     # Gera dados fictícios
│
├── .streamlit/
│   └── config.toml           # Configurações visuais
│
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

---

## 🧪 Testes Disponíveis

### ✅ Implementado: Saldos Invertidos

Identifica contas com natureza de saldo invertida:

| Natureza | Saldo Normal | Anomalia |
|----------|--------------|----------|
| ATIVO | Devedor (D) | Credor → 🔴 Crítico |
| PASSIVO | Credor (C) | Devedor → 🔴 Crítico |
| PL | Credor (C) | Devedor → 🟡 Atenção |

**Exceções conhecidas (não são erros):**
- Depreciação Acumulada
- Provisão para Devedores Duvidosos
- Prejuízos Acumulados

### 🔜 Em desenvolvimento

- Caixa Estourado (Caixa com saldo credor)
- Variação Horizontal (Ano vs Ano Anterior)
- Cruzamento ECD x ECF

---

## ☁️ Deploy no Streamlit Cloud (Grátis)

### Passo 1: Subir para GitHub

```bash
git init
git add .
git commit -m "Audiper MVP"
git remote add origin https://github.com/seu-usuario/audiper-mvp.git
git push -u origin main
```

### Passo 2: Conectar ao Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione seu repositório
5. Branch: `main`
6. Main file: `app.py`
7. Clique em "Deploy!"

Pronto! Sua URL será algo como: `https://audiper.streamlit.app`

---

## 📊 Formatos Suportados

### Entrada
- **SPED ECD** (.txt) - Escrituração Contábil Digital
  - Registro 0000: Dados da empresa
  - Registro I050: Plano de Contas
  - Registro I155: Saldos Periódicos

### Saída
- **Excel** (.xlsx) - Relatório formatado com múltiplas abas

---

## ⚙️ Configurações

Edite `.streamlit/config.toml` para personalizar:

```toml
[theme]
primaryColor = "#667eea"      # Cor principal
backgroundColor = "#ffffff"   # Fundo
textColor = "#1a1a2e"         # Texto

[server]
maxUploadSize = 200           # Tamanho máximo upload (MB)
```

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/novo-teste`)
3. Commit suas mudanças (`git commit -m 'Adiciona teste X'`)
4. Push para a branch (`git push origin feature/novo-teste`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é de uso interno da Audiper.

---

## 📞 Suporte

Em caso de dúvidas ou problemas:
- Abra uma Issue no GitHub
- Contate a equipe de desenvolvimento

---

**Desenvolvido com ❤️ para Audiper**
