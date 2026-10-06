import streamlit as st
import pandas as pd
from datetime import datetime

# Importações dos módulos locais do Agente-Gerop (ajuste conforme necessidade do projeto)
# from rag_engine import RAGEngine
# from indexer import DocumentIndexer

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agente-Gerop | Inteligência Operacional",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILIZAÇÃO CUSTOMIZADA (TEMA ESCURO COM TEXTO TOTALMENTE BRANCO)
# -----------------------------------------------------------------------------
CUSTOM_DARK_THEME = """
<style>
    /* Estilo Geral da Aplicação */
    .stApp {
        background-color: #0D1117;
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Forçar cor branca em textos, parágrafos, rótulos e elementos span */
    .stApp p, .stApp span, .stApp label, .stApp div, .stMarkdown, .stCaption {
        color: #FFFFFF !important;
    }

    /* Barra Lateral */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Títulos e Cabeçalhos */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }

    /* Containers e Cards */
    div[data-testid="stExpander"] {
        background-color: #161B22;
        border: 1px solid #30363D !important;
        border-radius: 6px;
    }
    
    .status-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 16px;
    }

    .status-card-header {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #FFFFFF !important;
        margin-bottom: 6px;
    }

    .status-card-value {
        font-size: 1.4rem;
        font-weight: 600;
        color: #58A6FF !important;
    }

    /* Inputs de Texto e Selects */
    .stTextInput input, .stSelectbox > div > div {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
        border-radius: 6px !important;
    }
    
    .stTextInput input:focus {
        border-color: #58A6FF !important;
        box-shadow: none !important;
    }

    /* Botões */
    .stButton > button {
        background-color: #238636;
        color: #FFFFFF !important;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 6px;
        font-weight: 500;
        padding: 0.4rem 1rem;
        transition: background-color 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #2EA043;
        border-color: rgba(240, 246, 252, 0.2);
    }

    /* Linha Divisora */
    hr {
        border-color: #30363D !important;
    }

    /* Tabelas */
    .stDataFrame {
        border: 1px solid #30363D;
        border-radius: 6px;
    }
</style>
"""

st.markdown(CUSTOM_DARK_THEME, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BARRA LATERAL (CONFIGURAÇÕES E PARÂMETROS)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("AGENTE-GEROP")
    st.caption("Painel de Controle e Parâmetros")
    st.divider()

    st.subheader("Parâmetros da Busca")
    
    # Única opção mantida em Parâmetros da Busca
    max_arquivos = st.slider(
        label="Máximo de arquivos por resposta",
        min_value=1,
        max_value=241,
        value=21,
        step=5,
        help="Define a quantidade limite de documentos de contexto retornados pelo mecanismo RAG."
    )

    # Limiar de similaridade fixado internamente no valor máximo (1.0)
    limiar_similaridade = 1.0

    st.divider()
    st.subheader("Configurações do Modelo")
    
    modelo_llm = st.selectbox(
        "Modelo de Linguagem",
        options=["LLM-Corporativo-v2", "LLM-Especializado-RAG", "LLM-Fast-Inference"],
        index=0
    )

    incluir_metadados = st.checkbox("Exibir metadados detalhados nas fontes", value=True)
    
    st.divider()
    
    st.caption("Status do Servidor: Operacional")
    st.caption(f"Última sincronização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")


# -----------------------------------------------------------------------------
# PAINEL PRINCIPAL
# -----------------------------------------------------------------------------

# Cabeçalho Principal
st.title("Consulta de Documentos e Recuperação RAG")
st.markdown("Interface corporativa para pesquisa vetorial e análise automatizada de documentos operacionais.")

st.divider()

# Métricas do Sistema
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown("""
        <div class="status-card">
            <div class="status-card-header">Base de Dados</div>
            <div class="status-card-value">241 Arquivos</div>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
        <div class="status-card">
            <div class="status-card-header">Limite por Consulta</div>
            <div class="status-card-value">{max_arquivos} Docs</div>
        </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown("""
        <div class="status-card">
            <div class="status-card-header">Status do Pipeline</div>
            <div class="status-card-value" style="color: #3FB950 !important;">Ativo</div>
        </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown("""
        <div class="status-card">
            <div class="status-card-header">Índice Vetorial</div>
            <div class="status-card-value" style="color: #D29922 !important;">Sincronizado</div>
        </div>
    """, unsafe_allow_html=True)

# Área de Entrada de Pesquisa
st.subheader("Solicitação de Pesquisa")

query_input = st.text_input(
    label="Digite o termo ou comando para pesquisa nos documentos",
    placeholder="Ex: Informe os procedimentos operacionais para análise de risco da unidade...",
    label_visibility="collapsed"
)

col_btn_1, col_btn_2, col_spacer = st.columns([1, 1, 4])

with col_btn_1:
    executar_busca = st.button("Executar Pesquisa", use_container_width=True)

with col_btn_2:
    limpar_campos = st.button("Limpar Consulta", use_container_width=True)

st.divider()

# Exibição dos Resultados
if executar_busca and query_input:
    st.subheader("Resultado da Consulta")
    
    # Aba de visualizações
    tab_resposta, tab_fontes, tab_metricas = st.tabs(["Resposta Gerada", "Fontes Consultadas", "Métricas de Busca"])

    with tab_resposta:
        st.markdown("**Síntese dos Documentos:**")
        st.info(
            f"Consulta realizada com sucesso considerando até {max_arquivos} arquivos de suporte. "
            f"Abaixo está a consolidação gerada com base nos parâmetros selecionados."
        )
        
        # Exemplo de resposta estruturada
        st.markdown("""
        ### Resumo Executivo
        Com base no levantamento realizado na base documental corporativa:

        1. **Diretrizes Gerais:** As operações devem seguir estritamente o protocolo interno de homologação.
        2. **Controle de Risco:** A verificação dos logs de sistema precisa ser executada a cada ciclo semanal.
        3. **Ações Corretivas:** Qualquer divergência identificada deve ser reportada via canal oficial imediatamente.
        """)

    with tab_fontes:
        st.markdown(f"**Documentos Selecionados (Máximo configurado: {max_arquivos}):**")
        
        # Exemplo simulado de lista de fontes limitada pelo valor do slider
        for i in range(1, min(max_arquivos + 1, 6)):
            with st.expander(f"Documento Ref-00{i}.pdf (Pontuação de Relevância: {limiar_similaridade:.2f})"):
                st.write(f"**Caminho:** `/base_dados/gerop/doc_ref_00{i}.pdf`")
                st.write("**Trecho Relevante:**")
                st.caption(f"\"...este trecho representa o conteúdo extraído do documento {i} referente à consulta efetuada no sistema Gerop...\"")
                if incluir_metadados:
                    st.json({"data_modificacao": "2026-02-15", "autor": "Gerência Operacional", "bloco_id": i * 12})

    with tab_metricas:
        data_metricas = {
            "Métrica": ["Tempo de Busca Vetorial", "Tempo de Geração LLM", "Arquivos Avaliados", "Arquivos Retornados", "Limiar de Similaridade (Máx)"],
            "Valor": ["0.14s", "1.82s", "241", f"{max_arquivos}", f"{limiar_similaridade}"]
        }
        st.table(pd.DataFrame(data_metricas))

elif executar_busca and not query_input:
    st.warning("Por favor, digite um termo de pesquisa antes de executar.")