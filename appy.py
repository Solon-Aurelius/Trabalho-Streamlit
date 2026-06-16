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
        st.sidebar.success("projeto cirado com sucesso!")  # Mensagem pedida por você
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
            st.sidebar.success("Fornecedor adicionado com sucesso!")  # Mensagem pedida por você
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
        for
