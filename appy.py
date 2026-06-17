import streamlit as st  

# Configura a página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Gestor de orçamentos", 
    page_icon="📚", 
    layout="wide"  
)

# Estilo visual para deixar tudo mais redondo e bonito
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título do sistema
st.title("📂 Gestor de Orçamentos Super Fácil")
st.caption("Descubra o fornecedor mais barato sem fazer nenhuma conta de cabeça!")
st.write("---")

# Memória do programa para os dados não sumirem
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
# MENU LATERAL (SÓ PARA CRIAR AS PASTAS MAIORES)
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Comece por Aqui")
    
    # Caixa 1: Criar Projeto
    with st.container(border=True):
        st.markdown("### 📁 1º Passo: Criar Projeto")
        novo_projeto = st.text_input("Digite o nome do Projeto:", placeholder="Ex: Meu Quarto Novo")
        if st.button("🟩 SALVAR PROJETO", use_container_width=True):  
            if novo_projeto and novo_projeto not in st.session_state.projetos:
                st.session_state.projetos[novo_projeto] = {}  
                st.success("projeto cirado com sucesso!")  
                st.rerun()  

    st.write("") 

    # Caixa 2: Escolher Projeto e Criar Fornecedor
    lista_projetos = list(st.session_state.projetos.keys())
    if lista_projetos:
        with st.container(border=True):
            st.markdown("### 🏢 2º Passo: Adicionar Lojas")
            projeto_atual = st.selectbox("Qual projeto você quer mexer?", lista_projetos)
            
            st.divider()
            
            novo_fornecedor = st.text_input("Nome da Loja / Fornecedor:", placeholder="Ex: Loja do Zé")
            if st.button("🟩 SALVAR LOJA", use_container_width=True):
                if novo_fornecedor and novo_fornecedor not in st.session_state.projetos[projeto_atual]:
                    st.session_state.projetos[projeto_atual][novo_fornecedor] = {}  
                    st.success("Fornecedor adicionado com sucesso!")  
                    st.rerun()
    else:
        st.sidebar.warning("⚠️ Crie um projeto acima para começar.")  
        st.stop()  


# ==============================================================================
# PAINEL CENTRAL (ONDE TUDO ACONTECE)
# ==============================================================================

# Barra azul indicando onde o usuário está trabalhando no momento
st.info(f"O projeto que você está mexendo agora é o: {projeto_atual}")

# Cria as três abas principais, incluindo a nova tela de tutorial
aba_tutorial, aba_cadastro, aba_visao = st.tabs([
    "📖 Guia de Uso (Passo a Passo)", 
    "📝 Colocar Preços (Cadastro)", 
    "📊 Ver Quem Ganhou (Resultados)"
])

# --- ABA 0: TELA INICIAL INTERATIVA (GUIA PASSO A PASSO) ---
with aba_tutorial:
    st.markdown("## ⚡ Como usar o sistema em 3 passos simples:")
    
    col_t1, col_t2, col_t3 = st.columns(3, gap="medium")
    
    with col_t1:
        with st.container(border=True):
            st.markdown("### 1️⃣ Esquerda da Tela")
            st.write("Escreva o nome do seu **Projeto** e clique no botão verde. Depois, crie as **Lojas** (fornecedores) que você pesquisou.")
            
    with col_t2:
        with st.container(border=True):
            st.markdown("### 2️⃣ Aba 'Colocar Preços'")
            st.write("Vá na segunda aba aqui em cima, crie uma opção de orçamento (Ex: À vista) e digite todos os produtos com os seus preços.")
            
    with col_t3:
        with st.container(border=True):
            st.markdown("### 3️⃣ Aba 'Ver Quem Ganhou'")
            st.write("Abra a terceira aba e veja a mágica acontecer! O sistema mostra na hora um **Card Verde** com a opção mais barata para você economizar.")

    st.write("")
    st.success("💡 **Dica de Ouro:** Já deixamos alguns dados de teste salvos para você ver como funciona. Clique nas abas acima para testar!")


# --- ABA 1: COLOCAR PREÇOS (CADASTROS) ---
with aba_cadastro:
    lista_fornecedores = list(st.session_state.projetos[projeto_atual].keys())
    
    if lista_fornecedores:
        st.markdown("### 🏢 Seleção de Loja")
        fornecedor_atual = st.selectbox("Escolha em qual Loja você quer mexer agora:", lista_fornecedores)
        
        col_bloco_a, col_bloco_b = st.columns(2, gap="large")
        
        # Criar a pasta do orçamento
        with col_bloco_a:
            with st.container(border=True):
                st.markdown("### ✏️ A) Criar Grupo de Orçamento")
                st.caption("Exemplo: Opção Parcelada, Opção à Vista, Tipo Econômico...")
                
                novo_nome_orcamento = st.text_input("Escreva o nome do orçamento:", placeholder="Ex: À Vista com Desconto", key="nome_orc_input")
                if st.button("📦 CRIAR GRUPO", use_container_width=True):
                    if novo_nome_orcamento and novo_nome_orcamento not in st.session_state.projetos[projeto_atual][fornecedor_atual]:
                        st.session_state.projetos[projeto_atual][fornecedor_atual][novo_nome_orcamento] = []  
                        st.success(f"Orçamento '{novo_nome_orcamento}' criado com sucesso!")
                        st.rerun()
        
        # Adicionar as coisas e preços
        with col_bloco_b:
            with st.container(border=True):
                st.markdown("### 🛒 B) Colocar os Produtos Dentro")
                st.caption(f"Os itens abaixo vão entrar na loja: **{fornecedor_atual}**")
                
                lista_orcamentos = list(st.session_state.projetos[projeto_atual][fornecedor_atual].keys())
                if lista_orcamentos:
                    orcamento_atual = st.selectbox("Escolha o orçamento de destino:", lista_orcamentos)
                    
                    prod_nome = st.text_input("Nome do produto:", placeholder="Ex: Cadeira Amarela")
                    prod_preco = st.number_input("Preço dele (R$):", min_value=0.0, step=10.0, format="%.2f")
                    
                    if st.button("🛒 ADICIONAR PRODUTO", use_container_width=True):
                        if prod_nome:  
                            st.session_state.projetos[projeto_atual][fornecedor_atual][orcamento_atual].append({
                                "nome": prod_nome,
                                "preco": prod_preco
                            })
                            st.success(f" O {prod_nome} custando {prod_preco:.2f} reais foi adicionando com êxito!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Você esqueceu de digitar o nome do produto!")
                else:
                    st.warning("⚠️ Crie primeiro um Grupo de Orçamento no lado esquerdo antes de colocar os produtos.")
    else:
        st.info("💡 Cadastre uma Loja/Fornecedor no menu do lado esquerdo para liberar os botões de colocar preço.")


# --- ABA 2: VER QUEM GANHOU (VISUALIZAÇÃO E RESULTADOS) ---
with aba_visao:
    estrutura_projeto = st.session_state.projetos[projeto_atual]
    dados_ranking = []  
    
    # 1. Faz a soma invisível dos preços primeiro
    if estrutura_projeto:
        for forn, orcamentos in estrutura_projeto.items():
            if orcamentos:
                for nome_orc, produtos in orcamentos.items():
                    if produtos:
                        total_orc = sum(p["preco"] for p in produtos)
                        dados_ranking.append({"fornecedor": forn, "orcamento": nome_orc, "total": total_orc})

        # 2. Caixa do Campeão da Economia
        if dados_ranking:
            st.markdown("## 🏆 Quem Ficou Mais Barato?")
            
            melhor_opcao = min(dados_ranking, key=lambda x: x["total"])
            
            texto_vencedor = (
                f"🥇 A melhor combinação custo-benefício para o projeto '{projeto_atual}' é o {melhor_opcao['orcamento']} "
                f"do fornecedor {melhor_opcao['fornecedor']}, "
                f"com o custo total de R$ {melhor_opcao['total']:.2f}."
            )
            
            st.markdown(
                f"""
                <div style="background-color: #1e4620; padding: 22px; border-radius: 8px; border-left: 6px solid #2e7d32; color: #e8f5e9; font-size: 18px; font-weight: bold; margin-bottom: 30px;">
                    {texto_vencedor}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.info("💡 Coloque produtos e valores na aba anterior para eu calcular quem ganhou.")
            
        st.write("### 📋 Lista com Todos os Preços que Você Cadastrou")
        st.write("")

        # 3. Mostrar as tabelas de preços separadas por Loja
        for forn, orcamentos in estrutura_projeto.items():
            st.markdown(f"#### 🏢 Loja / Fornecedor: **{forn}**")
            
            if orcamentos:
                cols = st.columns(len(orcamentos))
                
                for idx, (nome_orc, produtos) in enumerate(orcamentos.items()):
                    with cols[idx]:
                        with st.container(border=True):
                            st.markdown(f"📄 **{nome_orc}**")
                            st.write("---")
                            total_orc = 0
                            
                            if produtos:
                                for p in produtos:
                                    st.write(f"• {p['nome']}: R$ {p['preco']:.2f}")
                                    total_orc += p["preco"]  
                                
                                st.write("---")
                                st.metric(label="Total Desse Orçamento", value=f"R$ {total_orc:.2f}")
                            else:
                                st.caption("Nenhum item adicionado aqui ainda.")
            else:
                st.caption("Nenhum orçamento gerado para esta loja.")
            st.write("")
            st.divider()
    else:
        st.info("💡 Coloque dados na aba de cadastro para gerar os relatórios.")
