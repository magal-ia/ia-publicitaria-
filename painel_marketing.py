import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
import time

# Configuração inicial
st.set_page_config(
    page_title="Marketing Analytics Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dados de exemplo melhorados
def criar_dados_exemplo():
    return pd.DataFrame({
        "Campanha": ["Verão 2023", "Black Friday", "Natal", "Ano Novo", "Dia das Mães"],
        "Investimento": [5000, 15000, 10000, 8000, 7000],
        "Cliques": [1200, 3500, 2800, 2100, 1900],
        "Impressões": [50000, 150000, 120000, 90000, 85000],
        "Conversões": [120, 350, 210, 180, 160],
        "CTR": [2.4, 2.3, 2.1, 2.6, 2.2],
        "CPA": [41.67, 42.86, 47.62, 44.44, 43.75],
        "ROAS": [3.2, 4.1, 3.8, 3.5, 3.7],
        "Status": ["Ativa", "Concluída", "Concluída", "Pausada", "Ativa"],
        "Plataforma": ["Google Ads", "Facebook Ads", "Google Ads", "Facebook Ads", "Instagram Ads"],
        "Canal": ["Search", "Feed", "Display", "Stories", "Reels"]
    })

# Função para exportar Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def main():
    st.title("📊 Painel de Marketing Avançado")
    
    # Inicializar dados
    if 'df' not in st.session_state:
        st.session_state.df = criar_dados_exemplo()
    
    # Barra lateral para conexões e upload
    with st.sidebar:
        st.header("🔌 Conexões")
        
        # Conexão com Google Ads
        with st.expander("🔵 Conectar Google Ads", expanded=False):
            google_client_id = st.text_input("ID do Cliente Google Ads", key="google_client_id")
            google_token = st.text_input("Token de Acesso", type="password", key="google_access_token")
            if st.button("Conectar Google Ads", key="connect_google"):
                with st.spinner("Conectando ao Google Ads..."):
                    time.sleep(2)
                    if google_client_id and google_token:
                        st.success("Conexão estabelecida com Google Ads!")
                    else:
                        st.error("Preencha todos os campos")
        
        # Conexão com Facebook Ads
        with st.expander("🔴 Conectar Meta Ads", expanded=False):
            meta_client_id = st.text_input("ID do Anúncio Facebook", key="meta_client_id")
            meta_token = st.text_input("Token de Acesso", type="password", key="meta_access_token")
            if st.button("Conectar Meta Ads", key="connect_meta"):
                with st.spinner("Conectando ao Meta Ads..."):
                    time.sleep(2)
                    if meta_client_id and meta_token:
                        st.success("Conexão estabelecida com Meta Ads!")
                    else:
                        st.error("Preencha todos os campos")
        
        # Upload de arquivo Excel
        st.header("📤 Upload de Dados")
        uploaded_file = st.file_uploader("Carregue sua planilha", 
                                       type=["xlsx", "csv"],
                                       key="file_uploader",
                                       help="Formatos suportados: Excel (.xlsx) ou CSV")
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.xlsx'):
                    df_uploaded = pd.read_excel(uploaded_file)
                else:
                    df_uploaded = pd.read_csv(uploaded_file)
                
                st.session_state.df = df_uploaded
                st.success("Dados carregados com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {str(e)}")
        
        # Botão para resetar dados
        if st.button("🔄 Restaurar Dados Originais", key="reset_data"):
            st.session_state.df = criar_dados_exemplo()
            st.success("Dados restaurados para o exemplo padrão!")

    # Abas principais
    tab1, tab2, tab3 = st.tabs(["📋 Planilha", "📈 Análise", "📊 Dashboard Interativo"])
    
    with tab1:
        st.header("Planilha de Campanhas")
        
        # Editor de dados
        edited_df = st.data_editor(
            st.session_state.df,
            num_rows="dynamic",
            column_config={
                "Investimento": st.column_config.NumberColumn(
                    format="R$ %.2f",
                    min_value=0,
                    help="Valor total investido na campanha"
                ),
                "CPA": st.column_config.NumberColumn(
                    format="R$ %.2f",
                    help="Custo por aquisição"
                ),
                "CTR": st.column_config.ProgressColumn(
                    format="%.2f%%", 
                    min_value=0, 
                    max_value=10,
                    help="Click-through rate"
                ),
                "ROAS": st.column_config.NumberColumn(
                    format="%.2f",
                    help="Retorno sobre investimento em publicidade"
                ),
                "Status": st.column_config.SelectboxColumn(
                    options=["Ativa", "Pausada", "Concluída", "Rascunho"],
                    help="Status atual da campanha"
                ),
                "Plataforma": st.column_config.SelectboxColumn(
                    options=["Google Ads", "Facebook Ads", "Instagram Ads", "TikTok Ads", "LinkedIn Ads"],
                    help="Plataforma de anúncios"
                ),
                "Canal": st.column_config.SelectboxColumn(
                    options=["Search", "Display", "Feed", "Stories", "Reels", "Vídeo"],
                    help="Canal de veiculação"
                )
            },
            use_container_width=True,
            key="data_editor"
        )
        
        # Atualizar dados na sessão se houve edição
        if not edited_df.equals(st.session_state.df):
            st.session_state.df = edited_df
            st.rerun()
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                "📥 Baixar Excel",
                data=to_excel(st.session_state.df),
                file_name="campanhas_marketing.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Exportar dados para Excel"
            )
        with col2:
            if st.button("🔄 Atualizar Métricas", key="update_metrics"):
                with st.spinner("Calculando métricas..."):
                    st.session_state.df["CTR"] = np.round((st.session_state.df["Cliques"] / st.session_state.df["Impressões"]) * 100, 2)
                    st.session_state.df["CPA"] = np.round(st.session_state.df["Investimento"] / st.session_state.df["Conversões"], 2)
                    st.session_state.df["ROAS"] = np.round((st.session_state.df["Conversões"] * 100) / st.session_state.df["Investimento"], 2)
                    st.success("Métricas atualizadas com sucesso!")
                    time.sleep(1)
                    st.rerun()
        with col3:
            if st.button("🧹 Limpar Dados", key="clear_data"):
                st.session_state.df = pd.DataFrame(columns=st.session_state.df.columns)
                st.warning("Dados limpos! Carregue um novo arquivo ou restaure os dados originais.")
    
    with tab2:
        st.header("Análise de Performance")
        
        # Filtros avançados
        with st.expander("🔍 Filtros Avançados", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.multiselect(
                    "Status",
                    options=st.session_state.df["Status"].unique(),
                    default=st.session_state.df["Status"].unique(),
                    key="status_filter"
                )
            with col2:
                platform_filter = st.multiselect(
                    "Plataforma",
                    options=st.session_state.df["Plataforma"].unique(),
                    default=st.session_state.df["Plataforma"].unique(),
                    key="platform_filter"
                )
            with col3:
                channel_filter = st.multiselect(
                    "Canal",
                    options=st.session_state.df["Canal"].unique(),
                    default=st.session_state.df["Canal"].unique(),
                    key="channel_filter"
                )
        
        # Dados filtrados
        df_filtrado = st.session_state.df[
            st.session_state.df["Status"].isin(status_filter) & 
            st.session_state.df["Plataforma"].isin(platform_filter) &
            st.session_state.df["Canal"].isin(channel_filter)
        ]
        
        if not df_filtrado.empty:
            # Métricas resumidas
            st.subheader("📌 Resumo de Performance")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Investido", f"R$ {df_filtrado['Investimento'].sum():,.2f}")
            with col2:
                st.metric("Conversões Totais", f"{df_filtrado['Conversões'].sum():,}")
            with col3:
                st.metric("CTR Médio", f"{df_filtrado['CTR'].mean():.2f}%")
            with col4:
                st.metric("ROAS Médio", f"{df_filtrado['ROAS'].mean():.2f}")
            
            # Gráficos
            st.subheader("📊 Visualizações")
            
            tab1, tab2, tab3 = st.tabs(["Engajamento", "Eficiência", "Distribuição"])
            
            with tab1:
                fig_engajamento = px.bar(
                    df_filtrado,
                    x="Campanha",
                    y=["Cliques", "Conversões"],
                    barmode="group",
                    title="Engajamento por Campanha",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig_engajamento, use_container_width=True)
                
            with tab2:
                fig_eficiencia = px.scatter(
                    df_filtrado,
                    x="Investimento",
                    y="Conversões",
                    size="ROAS",
                    color="Plataforma",
                    hover_name="Campanha",
                    title="Eficiência das Campanhas",
                    trendline="lowess"
                )
                st.plotly_chart(fig_eficiencia, use_container_width=True)
                
            with tab3:
                fig_distribuicao = px.pie(
                    df_filtrado,
                    names="Plataforma",
                    values="Investimento",
                    title="Distribuição de Investimento por Plataforma",
                    hole=0.3
                )
                st.plotly_chart(fig_distribuicao, use_container_width=True)
        else:
            st.warning("Nenhum dado encontrado com os filtros selecionados")
    
    with tab3:
        st.header("Dashboard Interativo")
        
        if not st.session_state.df.empty:
            # Verifica se existem colunas numéricas suficientes
            numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                # Controles interativos
                with st.expander("⚙️ Configurações do Gráfico", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        x_axis = st.selectbox(
                            "Eixo X", 
                            options=numeric_cols,
                            index=0,
                            key="x_axis"
                        )
                    with col2:
                        y_axis = st.selectbox(
                            "Eixo Y", 
                            options=numeric_cols,
                            index=1 if len(numeric_cols) > 1 else 0,
                            key="y_axis"
                        )
                    with col3:
                        color_options = ["Nenhum"] + st.session_state.df.select_dtypes(exclude=['number']).columns.tolist()
                        color_by = st.selectbox(
                            "Cor por", 
                            options=color_options,
                            index=0,
                            key="color_by"
                        )
                
                # Gráfico de dispersão interativo
                try:
                    fig = px.scatter(
                        st.session_state.df,
                        x=x_axis,
                        y=y_axis,
                        color=None if color_by == "Nenhum" else color_by,
                        hover_name="Campanha",
                        hover_data=st.session_state.df.columns,
                        title=f"Relação entre {x_axis} e {y_axis}",
                        template="plotly_white"
                    )
                    fig.update_traces(
                        marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao criar gráfico: {str(e)}")
                
                # Matriz de correlação
                st.subheader("🔗 Matriz de Correlação")
                try:
                    corr_matrix = st.session_state.df[numeric_cols].corr()
                    fig_corr = px.imshow(
                        corr_matrix,
                        text_auto=True,
                        aspect="auto",
                        color_continuous_scale='Blues',
                        title="Correlação entre Métricas Numéricas"
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao criar matriz de correlação: {str(e)}")
                
                # Estatísticas descritivas
                st.subheader("📝 Estatísticas Descritivas")
                try:
                    st.dataframe(
                        st.session_state.df[numeric_cols].describe().T.style.format("{:.2f}"),
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Erro ao exibir estatísticas: {str(e)}")
            else:
                st.warning("São necessárias pelo menos 2 colunas numéricas para a análise.")
        else:
            st.warning("Nenhum dado disponível para análise. Carregue dados ou restaure o exemplo.")

if __name__ == "__main__":
    main()