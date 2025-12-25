# 🚀 Guia Completo de Deploy - Audiper MVP

Este documento contém instruções passo a passo para colocar o Audiper no ar no Streamlit Cloud.

---

## 📋 Pré-requisitos

Antes de começar, você precisará de:

1. **Conta no GitHub** - [github.com](https://github.com)
2. **Conta no Streamlit Cloud** - [share.streamlit.io](https://share.streamlit.io)
3. **Git instalado** no seu computador (opcional, mas recomendado)

---

## 🔧 Opção 1: Deploy Rápido (Recomendado)

### Passo 1: Preparar o Repositório GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Crie um novo repositório chamado `audiper-mvp`
3. **Não** inicialize com README (deixe em branco)
4. Clique em "Create repository"

### Passo 2: Fazer Upload dos Arquivos

Na página do seu novo repositório, clique em "uploading an existing file" e faça upload de:

- `app.py`
- `requirements.txt`
- `README.md`
- Pasta `core/` (com todos os arquivos)
- Pasta `dados_demo/` (com todos os arquivos)
- Pasta `.streamlit/` (com `config.toml`)

### Passo 3: Conectar ao Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em "New app"
3. Faça login com sua conta GitHub (se solicitado)
4. Preencha os campos:
   - **Repository:** `seu-usuario/audiper-mvp`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Clique em "Deploy"

**Pronto!** Em 2-3 minutos, seu app estará online em:
```
https://audiper-mvp.streamlit.app
```

---

## 💻 Opção 2: Deploy via Git (Para Desenvolvedores)

### Passo 1: Clonar o Repositório Local

```bash
# Clone este repositório
git clone https://github.com/seu-usuario/audiper-mvp.git
cd audiper-mvp
```

### Passo 2: Fazer Alterações (Opcional)

Edite os arquivos conforme necessário.

### Passo 3: Fazer Commit e Push

```bash
# Adicionar todas as mudanças
git add .

# Fazer commit
git commit -m "Atualização do Audiper"

# Fazer push para GitHub
git push origin main
```

### Passo 4: Deploy Automático

O Streamlit Cloud detectará automaticamente as mudanças e fará o redeploy!

---

## 🧪 Testar Localmente Antes de Fazer Deploy

### Passo 1: Instalar Dependências

```bash
# Criar ambiente virtual (recomendado)
python3 -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

### Passo 3: Testar Funcionalidades

- ✅ Clique em "Usar Dados Demo" para testar com dados fictícios
- ✅ Verifique se os achados aparecem corretamente
- ✅ Teste o download do Excel
- ✅ Verifique a visualização de dados brutos

---

## 📁 Estrutura do Projeto

```
audiper-mvp/
├── app.py                      # Aplicação principal
├── requirements.txt            # Dependências Python
├── README.md                   # Documentação
├── DEPLOY_GUIDE.md            # Este arquivo
│
├── core/                       # Lógica de negócio
│   ├── __init__.py
│   ├── leitor_sped.py         # Parser do SPED ECD
│   ├── testes_auditoria.py    # Testes automatizados
│   └── exportador.py          # Geração de Excel
│
├── dados_demo/                # Dados para demonstração
│   ├── __init__.py
│   └── demo_generator.py      # Gera dados fictícios
│
└── .streamlit/                # Configurações Streamlit
    └── config.toml            # Tema e configurações visuais
```

---

## 🔐 Variáveis de Ambiente (Futuro)

Se precisar adicionar variáveis de ambiente (como chaves de API):

1. No Streamlit Cloud, vá para **Settings** do seu app
2. Clique em **Secrets**
3. Adicione suas variáveis no formato:
   ```
   API_KEY = "sua-chave-aqui"
   DATABASE_URL = "sua-url-aqui"
   ```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'core'"

**Solução:** Certifique-se de que a pasta `core/` contém um arquivo `__init__.py`

### Erro: "streamlit: command not found"

**Solução:** Instale o Streamlit:
```bash
pip install streamlit
```

### App não carrega no Streamlit Cloud

**Solução:** 
1. Verifique se `requirements.txt` está correto
2. Verifique os logs no Streamlit Cloud (aba "Logs")
3. Tente fazer um novo commit e push

### Upload de arquivo muito lento

**Solução:** O limite padrão é 200MB. Para aumentar, edite `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500  # em MB
```

---

## 📊 Monitorar Seu App

No Streamlit Cloud:

1. Acesse [share.streamlit.io/admin](https://share.streamlit.io/admin)
2. Clique no seu app
3. Visualize:
   - **Logs:** Erros e mensagens de execução
   - **Settings:** Configurações do app
   - **Secrets:** Variáveis de ambiente

---

## 🔄 Atualizar o App

Sempre que você fizer mudanças no código:

```bash
# 1. Fazer commit das mudanças
git add .
git commit -m "Descrição da mudança"

# 2. Fazer push para GitHub
git push origin main

# 3. Streamlit Cloud fará o redeploy automaticamente
# (pode levar 1-2 minutos)
```

---

## 📞 Suporte

Em caso de problemas:

1. Verifique os **Logs** no Streamlit Cloud
2. Consulte a [Documentação do Streamlit](https://docs.streamlit.io)
3. Abra uma Issue no GitHub do projeto

---

## ✅ Checklist Final

Antes de considerar o deploy completo:

- [ ] Repositório GitHub criado e com todos os arquivos
- [ ] Aplicação testada localmente com sucesso
- [ ] Dados demo funcionando corretamente
- [ ] Excel sendo gerado corretamente
- [ ] App deployed no Streamlit Cloud
- [ ] URL compartilhada com a equipe

---

**Desenvolvido com ❤️ para Audiper**

Versão: 1.0 | Data: Dezembro 2025
