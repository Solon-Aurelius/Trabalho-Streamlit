import streamlit as st  # Importa a biblioteca principal de interface web

# 1. Configuração de metadados da página (Deve ser o primeiro comando)
st.set_page_config(
    page_title="Gestor de Orçamentos", 
    page_icon="📚", 
    layout="wide"  # Define o layout em modo amplo para melhor aproveitamento da tela
)

# Título principal do sistema
st.title("📂 Sistema Avançado de Projetos e Fornecedores")

# 2. Inicialização da Estrutura de Dados Dinâmica (Dicionários Aninhados)
# Usamos st.session_state para que os dados inseridos não sumam ao clicar em botões
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
# PAINEL LATERAL (SIDEBAR): Gerenciamento da estrutura base do sistema
# ==============================================================================
st.sidebar.header("📁 Estrutura de Projetos")

# Input para capturar e validar a criação de um novo projeto
novo_projeto = st.sidebar.text_input("➕ Criar Novo Projeto")
if st.sidebar.button("Salvar Projeto"):  # Botão de ação
    if novo_projeto and novo_projeto not in st.session_state.projetos:
        st.session_state.projetos[novo_projeto] = {}  # Inicia projeto vazio
        st.sidebar.success(f"Projeto '{novo_projeto}' criado!")  # Feedback de sucesso
        st.rerun()  # Atualiza a tela imediatamente

st.sidebar.divider()  # Divisor visual

# Menu de seleção para definir qual projeto está ativo no momento
lista_projetos = list(st.session_state.projetos.keys())
if lista_projetos:
    projeto_atual = st.sidebar.selectbox("Selecione o Projeto Ativo", lista_projetos)
    
    # Input para adicionar fornecedores vinculados estritamente ao projeto ativo
    novo_fornecedor = st.sidebar.text_input(f"🏢 Novo Fornecedor para '{projeto_atual}'")
    if st.sidebar.button("Salvar Fornecedor"):
        if novo_fornecedor and novo_fornecedor not in st.session_state.projetos[projeto_atual]:
            st.session_state.projetos[projeto_atual][novo_fornecedor] = {}  # Inicia fornecedor vazio
            st.sidebar.success(f"Fornecedor adicionado!")
            st.rerun()
else:
    st.sidebar.warning("Crie um projeto para começar.")  # Mensagem de atenção
    st.stop()  # Interrompe a execução do script de forma segura até a ação do usuário


# ==============================================================================
# PAINEL CENTRAL: Organizado por Abas para melhor experiência visual
# ==============================================================================

# --- AVISO VISUAL DE SELEÇÃO ATIVA ---
# Esse bloco no topo serve para guiar o usuário sobre o que está selecionado globalmente
st.success(f"🚀 **Projeto Ativo Selecionado:** `{projeto_atual}`")

aba_cadastro, aba_visao = st.tabs(["📝 Criar Orçamentos e Itens", "📊 Painel Comparativo"])

# --- ABA 1: GERENCIAMENTO DE ORÇAMENTOS E ITENS ---
with aba_cadastro:
    st.header(f"📍 Área de Cadastro: {projeto_atual}")
    
    # Extrai os fornecedores cadastrados para o projeto selecionado
    lista_fornecedores = list(st.session_state.projetos[projeto_atual].keys())
    
    if lista_fornecedores:
        fornecedor_atual = st.selectbox("Selecione o Fornecedor para trabalhar:", lista_fornecedores)
        
        # Aviso visual informando qual fornecedor está ativo nesta aba
        st.info(f"🏢 Você está gerenciando os orçamentos de: **{fornecedor_atual}**")
        st.divider()
        
        # Sub-bloco A: Criação de uma pasta de orçamento específica para o fornecedor
        st.subheader(f"✏️ Novo Orçamento para {fornecedor_atual}")
        novo_nome_orcamento = st.text_input("Nome do Orçamento (Ex: À Vista, Parcelado, Versão Econômica)")
        if st.button("Criar este Orçamento"):
            if novo_nome_orcamento and novo_nome_orcamento not in st.session_state.projetos[projeto_atual][fornecedor_atual]:
                st.session_state.projetos[projeto_atual][fornecedor_atual][novo_nome_orcamento] = []  # Lista de itens vazia
                st.success(f"Orçamento '{novo_nome_orcamento}' criado com sucesso!")
                st.rerun()
        
        st.divider()
        
        # Sub-bloco B: Alimentação de itens/produtos dentro de um orçamento existente
        lista_orcamentos = list(st.session_state.projetos[projeto_atual][fornecedor_atual].keys())
        if lista_orcamentos:
            orcamento_atual = st.selectbox("Escolha o Orçamento para adicionar os produtos:", lista_orcamentos)
            
            # Mais um aviso visual mostrando onde o produto vai cair exatamente
            st.info(f"🛒 Os produtos digitados abaixo serão adicionados em: `{fornecedor_atual}` ➡️ `{orcamento_atual}`")
            
            # Divide os inputs na mesma linha usando colunas (Layout Responsivo)
            col_nome, col_preco = st.columns([3, 1])
            with col_nome:
                prod_nome = st.text_input("Item / Produto")
            with col_preco:
                prod_preco = st.number_input("Preço Unitário (R$)", min_value=0.0, step=10.0)
                
            if st.button("🛒 Adicionar Item ao Orçamento"):
                if prod_nome:  # Validação de dados contra campos em branco
                    st.session_state.projetos[projeto_atual][fornecedor_atual][orcamento_atual].append({
                        "nome": prod_nome,
                        "preco": prod_preco
                    })
                    st.success(f"✅ Produto '{prod_nome}' adicionado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Insira o nome do item.")
        else:
            st.info("Crie um Nome de Orçamento acima para poder vincular produtos a ele.")
    else:
        st.info("Cadastre um fornecedor na barra lateral para liberar as opções de orçamento.")


# --- ABA 2: PAINEL VISUAL E COMPARATIVO DE CUSTOS ---
with aba_visao:
    st.header(f"📋 Comparativo Geral do Projeto: {projeto_atual}")
    
    estrutura_projeto = st.session_state.projetos[projeto_atual]
    dados_ranking = []  # Lista auxiliar para calcular dinamicamente a melhor proposta econômica
    
    # --- PASSO 1: CALCULAR OS TOTAIS PRIMEIRO (Para poder colocar o resultado no topo) ---
    if estrutura_projeto:
        for forn, orcamentos in estrutura_projeto.items():
            if orcamentos:
                for nome_orc, produtos in orcamentos.items():
                    if produtos:
                        total_orc = sum(p["preco"] for p in produtos)
                        dados_ranking.append({"fornecedor": forn, "orcamento": nome_orc, "total": total_orc})

        # --- ALGORITMO DE INTELIGÊNCIA DE SELEÇÃO NO TOPO ---
        if dados_ranking:
            st.subheader("🏆 Economia Inteligente (Análise de Menor Preço)")
            
            # Função nativa 'min' avalia a chave "total" e retorna a menor entidade matemática da lista
            melhor_opcao = min(dados_ranking, key=lambda x: x["total"])
            
            texto_vencedor = (
                f"🥇 A melhor combinação custo-benefício para o projeto '{projeto_atual}' é o **{melhor_opcao['orcamento']}** "
                f"do fornecedor **{melhor_opcao['fornecedor']}**, "
                f"com o custo total consolidado de **R$ {melhor_opcao['total']:.2f}**."
            )
            
            # Injeção controlada de HTML/CSS para destaque visual no topo
            st.markdown(
                f"""
                <div style="background-color: #2e7d32; padding: 20px; border-radius: 8px; color: white; font-size: 18px; font-weight: bold; margin-bottom: 25px;">
                    {texto_vencedor}
                </div>
                """, 
                unsafe_allow_html=True
            )
        else:
            st.info("Adicione produtos nos orçamentos para que o sistema calcule a melhor opção econômica.")
            
        st.divider()

        # --- PASSO 2: DETALHAMENTO DOS FORNECEDORES (Abaixo do Card) ---
        for forn, orcamentos in estrutura_projeto.items():
            st.write(f"## 🏢 Fornecedor: {forn}")
            
            if orcamentos:
                # Cria colunas dinâmicas para exibir os orçamentos lado a lado na interface
                cols = st.columns(len(orcamentos))
                
                for idx, (nome_orc, produtos) in enumerate(orcamentos.items()):
                    with cols[idx]:
                        st.markdown(f"### 📄 {nome_orc}")
                        total_orc = 0
                        
                        if produtos:
                            for p in produtos:
                                st.write(f"• {p['nome']}: R$ {p['preco']:.2f}")
                                total_orc += p["preco"]  # Acumulador de valor
                            
                            # Exibe o valor final processado através de um componente de métrica
                            st.metric("Total do Orçamento", f"R$ {total_orc:.2f}")
                        else:
                            st.caption("Nenhum item neste orçamento.")
            else:
                st.caption("Nenhum orçamento gerado para este fornecedor.")
            st.divider()
    else:
        st.info("Adicione dados na primeira aba para gerar os relatórios comparativos.")
