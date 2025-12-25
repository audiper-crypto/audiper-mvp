"""
Audiper - Sistema de Auditoria Digital
Interface Streamlit

Execute com: streamlit run app.py
"""

import streamlit as st
import polars as pl
from datetime import datetime

# Importar módulos do core
from core.leitor_sped import processar_sped_ecd, carregar_arquivo_upload
from core.testes_auditoria import (
    teste_saldos_invertidos, 
    gerar_resumo_balancete,
    get_emoji_severidade,
)
from core.exportador import exportar_relatorio_completo
from dados_demo.demo_generator import gerar_dados_demonstracao


# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Audiper - Auditoria Digital",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado
st.markdown("""
<style>
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-card-red {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .metric-card-yellow {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #666;
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    /* Tabela de achados */
    .achado-critico {
        background-color: #fee2e2 !important;
        border-left: 4px solid #dc2626 !important;
    }
    
    .achado-atencao {
        background-color: #fef3c7 !important;
        border-left: 4px solid #f59e0b !important;
    }
    
    /* Esconder o menu hamburger e footer do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================
# ESTADO DA SESSÃO
# ============================================
if "dados_carregados" not in st.session_state:
    st.session_state.dados_carregados = False
    st.session_state.empresa = None
    st.session_state.df_plano = None
    st.session_state.df_saldos = None
    st.session_state.achados = []
    st.session_state.stats = {}


# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/audit.png", width=80)
    st.markdown("## 🔍 Audiper")
    st.markdown("*Sistema de Auditoria Digital*")
    st.divider()
    
    st.markdown("### 📁 Carregar Dados")
    
    # Opção 1: Upload de arquivo
    arquivo_upload = st.file_uploader(
        "Arquivo SPED ECD (.txt)",
        type=["txt"],
        help="Selecione o arquivo SPED ECD exportado do sistema contábil"
    )
    
    st.markdown("**ou**")
    
    # Opção 2: Dados de demonstração
    if st.button("🎭 Usar Dados Demo", use_container_width=True, type="secondary"):
        with st.spinner("Gerando dados de demonstração..."):
            empresa, df_plano, df_saldos = gerar_dados_demonstracao()
            
            st.session_state.empresa = empresa
            st.session_state.df_plano = df_plano
            st.session_state.df_saldos = df_saldos
            st.session_state.dados_carregados = True
            
            # Executar teste
            achados, stats = teste_saldos_invertidos(df_saldos)
            st.session_state.achados = achados
            st.session_state.stats = stats
            
        st.success("✅ Dados demo carregados!")
        st.rerun()
    
    # Processar arquivo se upload
    if arquivo_upload is not None:
        if st.button("⚡ Processar Arquivo", use_container_width=True, type="primary"):
            with st.spinner("Processando arquivo SPED..."):
                conteudo = carregar_arquivo_upload(arquivo_upload)
                empresa, df_plano, df_saldos, status = processar_sped_ecd(conteudo)
                
                if "✅" in status:
                    st.session_state.empresa = empresa
                    st.session_state.df_plano = df_plano
                    st.session_state.df_saldos = df_saldos
                    st.session_state.dados_carregados = True
                    
                    # Executar teste
                    achados, stats = teste_saldos_invertidos(df_saldos)
                    st.session_state.achados = achados
                    st.session_state.stats = stats
                    
                    st.success(status)
                    st.rerun()
                else:
                    st.error(status)
    
    st.divider()
    
    # Informações
    st.markdown("### ℹ️ Sobre")
    st.markdown("""
    **Versão:** MVP 1.0  
    **Testes disponíveis:**
    - ✅ Saldos Invertidos
    - 🔜 Caixa Estourado
    - 🔜 Variação Horizontal
    """)


# ============================================
# CONTEÚDO PRINCIPAL
# ============================================

# Header
st.markdown('<p class="main-header">🔍 Audiper</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema de Auditoria Digital - SPED ECD</p>', unsafe_allow_html=True)
st.divider()

# Se não há dados carregados
if not st.session_state.dados_carregados:
    st.markdown("## 👋 Bem-vindo!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Como usar:
        
        1. **Faça upload** do arquivo SPED ECD (.txt) na barra lateral
        2. Clique em **Processar Arquivo**
        3. Visualize os **achados de auditoria**
        4. **Exporte** o relatório em Excel
        
        ---
        
        💡 **Dica:** Use o botão "Dados Demo" para testar o sistema sem um arquivo real.
        """)
    
    with col2:
        st.markdown("""
        ### Testes Automatizados:
        
        | Teste | Descrição |
        |-------|-----------|
        | 🔴 **Saldos Invertidos** | Identifica Ativo com saldo credor e Passivo com saldo devedor |
        | 🔜 Caixa Estourado | Verifica se Caixa ficou negativo |
        | 🔜 Variação Horizontal | Compara ano atual vs anterior |
        """)
    
    st.stop()


# ============================================
# DASHBOARD (quando há dados)
# ============================================

# Informações da Empresa
empresa = st.session_state.empresa
if empresa:
    st.markdown(f"### 🏢 {empresa.nome}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("CNPJ", empresa.cnpj)
    col2.metric("UF", empresa.uf)
    col3.metric("Início", empresa.data_inicio)
    col4.metric("Fim", empresa.data_fim)
    
    st.divider()


# Métricas dos Achados
st.markdown("### 📊 Resumo da Auditoria")

stats = st.session_state.stats
achados = st.session_state.achados

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total de Achados",
        value=stats.get("total", 0),
        delta=None
    )

with col2:
    criticos = stats.get("criticos", 0)
    st.metric(
        label="🔴 Críticos",
        value=criticos,
        delta=f"{criticos} requerem ação" if criticos > 0 else None,
        delta_color="inverse"
    )

with col3:
    atencao = stats.get("atencao", 0)
    st.metric(
        label="🟡 Atenção",
        value=atencao,
    )

with col4:
    info = stats.get("info", 0)
    st.metric(
        label="🔵 Informativos",
        value=info,
    )

st.divider()


# Tabela de Achados
st.markdown("### 🔍 Detalhamento dos Achados")

if not achados:
    st.success("✅ Nenhuma exceção encontrada! Todas as contas estão com saldos coerentes.")
else:
    # Filtros
    col1, col2 = st.columns([1, 3])
    
    with col1:
        filtro_severidade = st.selectbox(
            "Filtrar por Severidade",
            options=["Todos", "CRÍTICO", "ATENÇÃO", "INFO"],
            index=0
        )
    
    # Aplicar filtro
    achados_filtrados = achados
    if filtro_severidade != "Todos":
        achados_filtrados = [a for a in achados if a["severidade"] == filtro_severidade]
    
    # Exibir como cards
    for achado in achados_filtrados:
        severidade = achado["severidade"]
        emoji = achado["emoji"]
        cor = achado["cor"]
        
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                st.markdown(f"**{emoji} {achado['cod_conta']}**")
                st.caption(achado["descricao"])
            
            with col2:
                st.markdown(f"**{achado['achado']}**")
                st.caption(f"Esperado: {achado['saldo_esperado']} | Encontrado: {achado['saldo_encontrado']}")
                
            with col3:
                st.markdown(f"### {achado['valor_formatado']}")
            
            with st.expander("💡 Ver recomendação"):
                st.info(achado["recomendacao"])
            
            st.divider()
    
    # Tabela alternativa (dados brutos)
    with st.expander("📋 Ver tabela completa"):
        df_achados = pl.DataFrame(achados_filtrados).select([
            "cod_conta", "descricao", "natureza", 
            "saldo_esperado", "saldo_encontrado", 
            "valor_formatado", "severidade", "achado"
        ])
        st.dataframe(
            df_achados.to_pandas(),
            use_container_width=True,
            hide_index=True
        )


# Botão de Export
st.divider()
st.markdown("### 📥 Exportar Relatório")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("📊 Gerar Excel Completo", type="primary", use_container_width=True):
        with st.spinner("Gerando relatório..."):
            excel_buffer = exportar_relatorio_completo(
                achados=achados,
                df_saldos=st.session_state.df_saldos,
                empresa_nome=empresa.nome if empresa else "N/A",
                periodo=f"{empresa.data_inicio} a {empresa.data_fim}" if empresa else "N/A"
            )
            
            st.download_button(
                label="⬇️ Baixar Relatório Excel",
                data=excel_buffer,
                file_name=f"auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

with col2:
    st.caption("""
    O relatório Excel contém:
    - **Resumo:** Dados da empresa e estatísticas
    - **Achados:** Lista completa de exceções encontradas  
    - **Balancete:** Todos os saldos processados
    """)


# Footer
st.divider()
st.caption(f"Audiper MVP v1.0 | Processado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | Desenvolvido para auditoria contábil digital")
