import streamlit as st  

# Configura a página (deve ser o primeiro comando)
st.set_page_config(
    page_title="Gestor de Orçamentos", 
    page_icon="📚", 
    layout="wide"  # Deixa a tela inteira mais larga
)

# Título do sistema
st.title("📂 Sistema Avançado de Projetos e Fornecedores")

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
# MENU LATERAL
# ==============================================================================
st.sidebar.header("📁 Estrutura de Projetos")

# Cria um novo projeto
novo_projeto = st.sidebar.text_input("➕ Criar Novo Projeto")
if st.sidebar.button("Salvar Projeto"):  
    if novo_projeto and novo_projeto not in st.session_state.projetos:
        st.session_state.projetos[novo_projeto] = {}  # Inicia o projeto vazio
        st.sidebar.success("projeto cirado com sucesso!")  # Mensagem pedida
        st.rerun()  # Recarrega a página

st.sidebar.divider()  

# Seleciona o projeto e adiciona fornecedores nele
lista_projetos = list(st.session_state.projetos.keys())
if lista_projetos:
    projeto_atual = st.sidebar.selectbox("Selecione o Projeto Ativo", lista_projetos)
    
    novo_fornecedor = st.sidebar.text_input(f"🏢 Novo Fornecedor para '{projeto_atual}'")
    if st.sidebar.button("Salvar Fornecedor"):
        if novo_fornecedor and novo_fornecedor not in st.session_state.projetos[projeto_atual]:
            st.session_state.projetos[projeto_atual][novo_fornecedor] = {}  # Inicia fornecedor vazio
            st.sidebar.success("Fornecedor adicionado com sucesso!")  # Mensagem pedida
            st.rerun()
else:
    st.sidebar.warning("Crie um projeto para começar.")  
    st.stop()  # Para o programa aqui até o usuário criar algo


# ==============================================================================
# PAINEL CENTRAL
# ==============================================================================

# Mostra no topo qual projeto está aberto
st.success(f"🚀 **Projeto Ativo Selecionado:** `{projeto_atual}`")

# Divide a tela em duas abas
aba_cadastro, aba_visao = st.tabs(["📝 Criar Orçamentos e Itens", "📊 Painel Comparativo"])

# --- ABA 1: CADASTROS ---
with aba_cadastro:
    st.header(f"📍 Área de Cadastro: {projeto_atual}")
    
    lista_fornecedores = list(st.session_state.projetos[projeto_atual].keys())
    
    if lista_fornecedores:
        fornecedor_atual = st.selectbox("Selecione o Fornecedor para trabalhar:", lista_fornecedores)
        st.info(f"🏢 Você está gerenciando os orçamentos de: **{fornecedor_atual}**")
        st.divider()
        
        # Cria uma pasta de orçamento dentro do fornecedor
        st.subheader(f"✏️ Novo Orçamento para {fornecedor_atual}")
        novo_nome_orcamento = st.text_input("Nome do Orçamento (Ex: À Vista, Parcelado)")
        if st.button("Criar este Orçamento"):
            if novo_nome_orcamento and novo_nome_orcamento not in st.session_state.projetos[projeto_atual][fornecedor_atual]:
                st.session_state.projetos[projeto_atual][fornecedor_atual][novo_nome_orcamento] = []  # Lista vazia de itens
                st.success(f"Orçamento '{novo_nome_orcamento}' criado com sucesso!")
                st.rerun()
        
        st.divider()
        
        # Coloca produtos dentro de um orçamento existente
        lista_orcamentos = list(st.session_state.projetos[projeto_atual][fornecedor_atual].keys())
        if lista_orcamentos:
            orcamento_atual = st.selectbox("Escolha o Orçamento para adicionar os produtos:", lista_orcamentos)
            st.info(f"🛒 Os produtos digitados abaixo serão adicionados em: `{fornecedor_atual}` ➡️ `{orcamento_atual}`")
            
            # Deixa os campos de texto e preço lado a lado
            col_nome, col_preco = st.columns([3, 1])
            with col_nome:
                prod_nome = st.text_input("Item / Produto")
            with col_preco:
                prod_preco = st.number_input("Preço Unitário (R$)", min_value=0.0, step=10.0)
                
            if st.button("🛒 Adicionar Item ao Orçamento"):
                if prod_nome:  # Checa se o nome não tá em branco
                    # Coloca o produto na lista do orçamento selecionado
                    st.session_state.projetos[projeto_atual][fornecedor_atual][orcamento_atual].append({
                        "nome": prod_nome,
                        "preco": prod_preco
                    })
                    # Mensagem personalizada exatamente como você pediu
                    st.success(f" O {prod_nome} custando {prod_preco:.2f} reais foi adicionando com êxito!")
                    st.rerun()
                else:
                    st.warning("Insira o nome do item.")
        else:
            st.info("Crie um Nome de Orçamento acima para poder vincular produtos a ele.")
    else:
        st.info("Cadastre um fornecedor na barra lateral para liberar as opções de orçamento.")


# --- ABA 2: VISUALIZAÇÃO E RESULTADOS ---
with aba_visao:
    st.header(f"📋 Comparativo Geral do Projeto: {projeto_atual}")
    
    estrutura_projeto = st.session_state.projetos[projeto_atual]
    dados_ranking = []  # Lista para guardar e comparar os totais
    
    # 1. FAZ A SOMA DE TUDO PRIMEIRO para descobrir o mais barato
    if estrutura_projeto:
        for forn, orcamentos in estrutura_projeto.items():
            if orcamentos:
                for nome_orc, presidential in orcamentos.items():
                    if presidential:
                        total_orc = sum(p["preco"] for p in presidential)
                        # Guarda os totais na lista
                        dados_ranking.append({"fornecedor": forn, "orcamento": nome_orc, "total": total_orc})

        # 2. MOSTRA O VENCEDOR NO TOPO
        if dados_ranking:
            st.subheader("🏆 Economia Inteligente (Análise de Menor Preço)")
            
            # Encontra o menor valor da lista com base no preço total
            melhor_opcao = min(dados_ranking, key=lambda x: x["total"])
            
            texto_vencedor = (
                f"🥇 A melhor combinação custo-benefício para o projeto '{projeto_atual}' é o **{melhor_opcao['orcamento']}** "
                f"do fornecedor **{melhor_opcao['fornecedor']}**, "
                f"com o custo total de **R$ {melhor_opcao['total']:.2f}**."
            )
            
            # Cria a caixinha verde bonita para o vencedor
            st.markdown(
                f"""
                <div style="background-color: #2e7d32; padding: 20px; border-radius: 8px; color: white; font-size: 18px; font-weight: bold; margin-bottom: 25px;">
                    {texto_vencedor}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.info("Adicione produtos nos orçamentos para calcular a melhor opção.")
            
        st.divider()

        # 3. MOSTRA OS DADOS DETALHADOS DE CADA FORNECEDOR (Abaixo do vencedor)
        for forn, orcamentos in estrutura_projeto.items():
            st.write(f"## 🏢 Fornecedor: {forn}")
            
            if orcamentos:
                # Coloca os orçamentos do fornecedor lado a lado em colunas
                cols = st.columns(len(orcamentos))
                
                for idx, (nome_orc, presidential) in enumerate(orcamentos.items()):
                    with cols[idx]:
                        st.markdown(f"### 📄 {nome_orc}")
                        total_orc = 0
                        
                        if presidential:
                            for p in presidential:
                                st.write(f"• {p['nome']}: R$ {p['preco']:.2f}")
                                total_orc += p["preco"]  # Soma o preço do item
                            
                            # Mostra o total destacado
                            st.metric("Total do Orçamento", f"R$ {total_orc:.2f}")
                        else:
                            st.caption("Nenhum item neste orçamento.")
            else:
                st.caption("Nenhum orçamento gerado para este fornecedor.")
            st.divider()
    else:
        st.info("Adicione dados na primeira aba para gerar os relatórios comparativos.")
