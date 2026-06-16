import streamlit as st  

# Configura a página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Gestor de Orçamentos", 
    page_icon="📚", 
    layout="wide"  # Deixa a tela inteira mais larga
)

# ==============================================================================
# ESTILO VISUAL EXTRA (Melhora o espaçamento e os cards)
# ==============================================================================
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal do sistema com uma linha fina decorativa
st.title("📂 Sistema Avançado de Projetos e Fornecedores")
st.caption("Organize seus projetos, cadastre propostas de fornecedores e descubra o menor preço de forma automatizada.")
st.write("---")

# Cria a memória do programa para os dados não sumirem ao clicar nos botões
if "projetos" not in st.session_state:
    st.session_state.projetos = {
        "Reforma Escritório": {
            "Fornecedor Madeiras LTDA": {
                "Orçamento Clássico": [{"nome": "Mesa de MDF", "preco": 450.0}, {"nome": "Prateleira", "preco": 150.0}],
                "Orçamento Premium": [{"nome": "Mesa de Madeira Maciça", "preco": 1200.0}]
            },
            "Fornecedor Móveis S/A": {
                "Opção Padrão": [{"nome": "Mesa Industrial", "preco": 600.0}, {"nome": "Cadeira Ergonômica", "preco": 800.0}]
            }
        }
    }

# ==============================================================================
# MENU LATERAL (Isolado para configurações de estrutura)
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Configurações de Estrutura")
    
    # Seção para Criar Projeto
    with st.container(border=True):
        st.subheader("📁 Projetos")
        novo_projeto = st.text_input("Nome do Novo Projeto", placeholder="Ex: Construção da Copa")
        if st.button("➕ Salvar Projeto", use_container_width=True):  
            if novo_projeto and novo_projeto not in st.session_state.projetos:
                st.session_state.projetos[novo_projeto] = {}  # Inicia o projeto vazio
                st.success("projeto cirado com sucesso!")  
                st.rerun()  # Recarrega a página

    st.write("") # Espaçamento

    # Seção para Selecionar Projeto e Criar Fornecedor
    lista_projetos = list(st.session_state.projetos.keys())
    if lista_projetos:
        with st.container(border=True):
            st.subheader("🏢 Fornecedores")
            projeto_atual = st.selectbox("Selecione o Projeto Ativo", lista_projetos)
            
            st.divider()
            
            novo_fornecedor = st.text_input("Nome do Novo Fornecedor", placeholder="Ex: Madeireira Central")
            if st.button("➕ Salvar Fornecedor", use_container_width=True):
                if novo_fornecedor and novo_fornecedor not in st.session_state.projetos[projeto_atual]:
                    st.session_state.projetos[projeto_atual][novo_fornecedor] = {}  # Inicia fornecedor vazio
                    st.success("Fornecedor adicionado com sucesso!")  
                    st.rerun()
    else:
        st.sidebar.warning("⚠️ Crie um projeto para começar.")  
        st.stop()  # Para o programa aqui até o usuário criar algo


# ==============================================================================
# PAINEL CENTRAL (Fluxo de Trabalho Principal)
# ==============================================================================

# Alerta elegante no topo indicando qual contexto o usuário está trabalhando
st.info(f"📌 **Você está visualizando e editando o projeto:** `{projeto_atual}`")

# Divide a tela em duas abas bem claras
aba_cadastro, aba_visao = st.tabs(["📝 Alimentar Dados (Orçamentos e Itens)", "📊 Dashboard e Painel Comparativo"])

# --- ABA 1: CADASTROS ---
with aba_cadastro:
    lista_fornecedores = list(st.session_state.projetos[projeto_atual].keys())
    
    if lista_fornecedores:
        # Seletor de fornecedor com destaque visual
        fornecedor_atual = st.selectbox("👉 Escolha um Fornecedor cadastrado para trabalhar:", lista_fornecedores)
        
        col_bloco_a, col_bloco_b = st.columns(2, gap="large")
        
        # LADO ESQUERDO: Criação das pastas de orçamento
        with col_bloco_a:
            with st.container(border=True):
                st.markdown("### ✏️ 1. Criar Opção de Orçamento")
                st.caption("Crie subdivisões para o mesmo fornecedor (ex: Opção À Vista, Parcelado, Versão Completa)")
                
                novo_nome_orcamento = st.text_input("Nome da Opção", placeholder="Ex: Proposta Econômica", key="nome_orc_input")
                if st.button("📦 Criar Orçamento", use_container_width=True):
                    if novo_nome_orcamento and novo_nome_orcamento not in st.session_state.projetos[projeto_atual][fornecedor_atual]:
                        st.session_state.projetos[projeto_atual][fornecedor_atual][novo_nome_orcamento] = []  # Lista vazia de itens
                        st.success(f"Orçamento '{novo_nome_orcamento}' criado!")
                        st.rerun()
        
        # LADO DIREITO: Inserção dos itens e preços
        with col_bloco_b:
            with st.container(border=True):
                st.markdown("### 🛒 2. Adicionar Itens / Produtos")
                st.caption(f"Adicione os materiais e valores dentro de uma das opções de: **{fornecedor_atual}**")
                
                lista_orcamentos = list(st.session_state.projetos[projeto_atual][fornecedor_atual].keys())
                if lista_orcamentos:
                    orcamento_atual = st.selectbox("Selecionar Destino:", lista_orcamentos)
                    
                    prod_nome = st.text_input("Nome do Item / Produto", placeholder="Ex: Cadeira de Escritório")
                    prod_preco = st.number_input("Preço Unitário (R$)", min_value=0.0, step=10.0, format="%.2f")
                    
                    if st.button("🛒 Confirmar e Adicionar Item", use_container_width=True):
                        if prod_nome:  # Checa se o nome não está em branco
                            st.session_state.projetos[projeto_atual][fornecedor_atual][orcamento_atual].append({
                                "nome": prod_nome,
                                "preco": prod_preco
                            })
                            st.success(f" O {prod_nome} custando {prod_preco:.2f} reais foi adicionando com êxito!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Por favor, insira o nome do item.")
                else:
                    st.warning("⚠️ Crie primeiro uma Opção de Orçamento no bloco ao lado para poder adicionar produtos.")
    else:
        st.info("💡 Cadastre pelo menos um fornecedor no menu lateral esquerdo para liberar os formulários de orçamento.")


# --- ABA 2: VISUALIZAÇÃO E RESULTADOS ---
with aba_visao:
    estrutura_projeto = st.session_state.projetos[projeto_atual]
    dados_ranking = []  # Lista para guardar e comparar os totais
    
    # 1. FAZ A SOMA DE TUDO PRIMEIRO para descobrir o mais barato
    if estrutura_projeto:
        for forn, orcamentos in estrutura_projeto.items():
            if orcamentos:
                for nome_orc, produtos in orcamentos.items():
                    if produtos:
                        total_orc = sum(p["preco"] for p in produtos)
                        dados_ranking.append({"fornecedor": forn, "orcamento": nome_orc, "total": total_orc})

        # 2. MOSTRA O VENCEDOR NO TOPO (ECONOMIA INTELIGENTE)
        if dados_ranking:
            st.markdown("## 🏆 Tomada de Decisão Automatizada")
            
            # Encontra o menor valor da lista com base no preço total
            melhor_opcao = min(dados_ranking, key=lambda x: x["total"])
            
            texto_vencedor = (
                f"🥇 A melhor combinação custo-benefício para o projeto '{projeto_atual}' é o **{melhor_opcao['orcamento']}** "
                f"do fornecedor **{melhor_opcao['fornecedor']}**, "
                f"com o custo total de **R$ {melhor_opcao['total']:.2f}**."
            )
            
            # Caixa verde elegante de destaque
            st.markdown(
                f"""
                <div style="background-color: #1e4620; padding: 22px; border-radius: 8px; border-left: 6px solid #2e7d32; color: #e8f5e9; font-size: 18px; font-weight: 500; margin-bottom: 30px;">
                    {texto_vencedor}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.info("💡 Adicione produtos e valores na aba anterior para que o relatório calcule a melhor opção de compra.")
            
        st.write("### 📋 Relatório Detalhado de Propostas Cadastradas")
        st.write("")

        # 3. MOSTRA OS DADOS DETALHADOS DE CADA FORNECEDOR (Cards lado a lado)
        for forn, orcamentos in estrutura_projeto.items():
            st.markdown(f"#### 🏢 Fornecedor: **{forn}**")
            
            if orcamentos:
                # Coloca os orçamentos do fornecedor lado a lado em colunas
                cols = st.columns(len(orcamentos))
                
                for idx, (nome_orc, produtos) in enumerate(orcamentos.items()):
                    with cols[idx]:
                        # Cada orçamento fica guardado dentro de um card limpo
                        with st.container(border=True):
                            st.markdown(f"📄 **{nome_orc}**")
                            st.write("---")
                            total_orc = 0
                            
                            if produtos:
                                for p in produtos:
                                    st.write(f"• {p['nome']}: R$ {p['preco']:.2f}")
                                    total_orc += p["preco"]  # Soma o preço do item
                                
                                st.write("---")
                                # Mostra o total destacado com o componente oficial de métrica do Streamlit
                                st.metric(label="Total Consolidado", value=f"R$ {total_orc:.2f}")
                            else:
                                st.caption("Nenhum item cadastrado nesta opção.")
            else:
                st.caption("Nenhum orçamento gerado para este fornecedor.")
            st.write("")
            st.divider()
    else:
        st.info("💡 Adicione dados na primeira aba para gerar os relatórios comparativos.")
