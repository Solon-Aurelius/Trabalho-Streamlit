import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Gestor de Orçamentos", page_icon="📚", layout="wide")

st.title("📂 Sistema Avançado de Projetos e Fornecedores")

# 2. Inicializa a estrutura de dados na sessão se não existir
# Estrutura: { "Projeto": { "Fornecedor": { "Nome do Orçamento": [lista de produtos] } } }
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

# ==========================================
# BARRA LATERAL: Cadastro de Base (Projeto e Fornecedor)
# ==========================================
st.sidebar.header("📁 Estrutura Base")

# Seção de Projetos
novo_projeto = st.sidebar.text_input("➕ Criar Novo Projeto")
if st.sidebar.button("Salvar Projeto"):
    if novo_projeto and novo_projeto not in st.session_state.projetos:
        st.session_state.projetos[novo_projeto] = {}
        st.sidebar.success(f"Projeto '{novo_projeto}' criado!")
        st.rerun()

st.sidebar.divider()

# Seção de Fornecedores
lista_projetos = list(st.session_state.projetos.keys())
if lista_projetos:
    projeto_atual = st.sidebar.selectbox("Selecione o Projeto Ativo", lista_projetos)
    
    novo_fornecedor = st.sidebar.text_input(f"🏢 Novo Fornecedor para '{projeto_atual}'")
    if st.sidebar.button("Salvar Fornecedor"):
        if novo_fornecedor and novo_fornecedor not in st.session_state.projetos[projeto_atual]:
            st.session_state.projetos[projeto_atual][novo_fornecedor] = {}
            st.sidebar.success(f"Fornecedor adicionado!")
            st.rerun()
else:
    st.sidebar.warning("Crie um projeto para começar.")
    st.stop()


# ==========================================
# PAINEL PRINCIPAL: Orçamentos e Itens
# ==========================================

aba_cadastro, aba_visao = st.tabs(["📝 Criar Orçamentos e Itens", "📊 Painel Comparativo"])

# --- ABA 1: CADASTRO DE ORÇAMENTOS E PRODUTOS ---
with aba_cadastro:
    st.header(f"📍 Projeto: {projeto_atual}")
    
    lista_fornecedores = list(st.session_state.projetos[projeto_atual].keys())
    
    if lista_fornecedores:
        fornecedor_atual = st.selectbox("Selecione o Fornecedor:", lista_fornecedores)
        
        st.divider()
        
        # Bloco A: Criar um novo Orçamento para este fornecedor
        st.subheader(f"✏️ Novo Orçamento para {fornecedor_atual}")
        novo_nome_orcamento = st.text_input("Nome do Orçamento (Ex: Opção A, À Vista, Versão Econômica)")
        if st.button("Criar este Orçamento"):
            if novo_nome_orcamento and novo_nome_orcamento not in st.session_state.projetos[projeto_atual][fornecedor_atual]:
                st.session_state.projetos[projeto_atual][fornecedor_atual][novo_nome_orcamento] = []
                st.success(f"Orçamento '{novo_nome_orcamento}' criado!")
                st.rerun()
        
        st.divider()
        
        # Bloco B: Adicionar Produtos a um Orçamento existente
        lista_orcamentos = list(st.session_state.projetos[projeto_atual][fornecedor_atual].keys())
        if lista_orcamentos:
            orcamento_atual = st.selectbox("Escolha o Orçamento para adicionar os produtos:", lista_orcamentos)
            
            # Formulário de inserção de produto
            col_nome, col_preco = st.columns([3, 1])
            with col_nome:
                prod_nome = st.text_input("Item / Produto")
            with col_preco:
                prod_preco = st.number_input("Preço (R$)", min_value=0.0, step=10.0)
                
            if st.button("🛒 Adicionar Item ao Orçamento"):
                if prod_nome:
                    st.session_state.projetos[projeto_atual][fornecedor_atual][orcamento_atual].append({
                        "nome": prod_nome,
                        "preco": prod_preco
                    })
                    st.success("Item adicionado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Insira o nome do item.")
        else:
            st.info("Crie um Nome de Orçamento acima para poder vincular produtos a ele.")
    else:
        st.info("Cadastre um fornecedor na barra lateral para liberar as opções de orçamento.")


# --- ABA 2: PAINEL COMPARATIVO ---
with aba_visao:
    st.header(f"📋 Comparativo Geral do Projeto: {projeto_atual}")
    
    estrutura_projeto = st.session_state.projetos[projeto_atual]
    dados_ranking = []
    
    if estrutura_projeto:
        for forn, orcamentos in estrutura_projeto.items():
            st.write(f"## 🏢 Fornecedor: {forn}")
            
            if orcamentos:
                # Criar colunas para exibir os diferentes orçamentos do mesmo fornecedor lado a lado
                cols = st.columns(len(orcamentos))
                
                for idx, (nome_orc, produtos) in enumerate(orcamentos.items()):
                    with cols[idx]:
                        st.markdown(f"### 📄 {nome_orc}")
                        total_orc = 0
                        
                        if produtos:
                            for p in produtos:
                                st.write(f"• {p['nome']}: R$ {p['preco']:.2f}")
                                total_orc += p["preco"]
                            
                            st.metric("Total do Orçamento", f"R$ {total_orc:.2f}")
                            # Guardamos qual fornecedor e qual orçamento gerou este custo
                            dados_ranking.append({"fornecedor": forn, "orcamento": nome_orc, "total": total_orc})
                        else:
                            st.caption("Nenhum item neste orçamento.")
            else:
                st.caption("Nenhum orçamento gerado para este fornecedor.")
            st.divider()
            
        # --- CÁLCULO DA MELHOR OPÇÃO ---
        if dados_ranking:
            st.subheader("🏆 Economia Inteligente")
            melhor_opcao = min(dados_ranking, key=lambda x: x["total"])
            
            texto_vencedor = (
                f"🥇 A melhor combinação é o {melhor_opcao['orcamento']} "
                f"do fornecedor {melhor_opcao['fornecedor']}, "
                f"com o custo total de R$ {melhor_opcao['total']:.2f}."
            )
            
            st.markdown(
                f"""
                <div style="background-color: #2e7d32; padding: 20px; border-radius: 8px; color: white; font-size: 18px;">
                    {texto_vencedor}
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.info("Adicione dados na primeira aba para gerar os relatórios comparativos.")