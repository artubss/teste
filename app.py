import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
import datetime
import uuid
from PIL import Image

# Configuração inicial
st.set_page_config(
    page_title="Nosso Closet RN - Sistema de Gestão",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF69B4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FF69B4;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
        margin-bottom: 1rem;
    }
    .pink-box {
        background-color: #FFE6F2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #FF69B4;
        margin-bottom: 1rem;
    }
    .task-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .task-pending {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
    }
    .task-progress {
        background-color: #D1ECF1;
        border-left: 5px solid #17A2B8;
    }
    .task-completed {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
    }
    .task-late {
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
    }
    .menu-option {
        background-color: #FFE6F2;
        padding: 0.8rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #FF69B4;
        cursor: pointer;
    }
    .menu-option:hover {
        background-color: #FFD1E6;
    }
    .menu-number {
        font-weight: bold;
        color: #FF69B4;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização de dados
if 'first_run' not in st.session_state:
    st.session_state.first_run = True
    
    # Dados de exemplo
    st.session_state.fornecedores = [
        {"id": "1", "nome": "Fornecedor A", "contato": "11 99999-9999", "taxa": 0.15},
        {"id": "2", "nome": "Fornecedor B", "contato": "11 88888-8888", "taxa": 0.20},
        {"id": "3", "nome": "Fornecedor C", "contato": "11 77777-7777", "taxa": 0.18}
    ]
    
    st.session_state.clientes = [
        {"id": "1", "nome": "Maria Silva", "telefone": "84 99999-9999", "endereco": "Rua A, 123"},
        {"id": "2", "nome": "João Santos", "telefone": "84 88888-8888", "endereco": "Av B, 456"},
        {"id": "3", "nome": "Ana Oliveira", "telefone": "84 77777-7777", "endereco": "Praça C, 789"}
    ]
    
    st.session_state.produtos = [
        {"id": "1", "nome": "Vestido Floral", "tamanho": "M", "cor": "Azul", "preco": 89.90, "fornecedor_id": "1", "imagem": None},
        {"id": "2", "nome": "Calça Jeans", "tamanho": "38", "cor": "Preto", "preco": 129.90, "fornecedor_id": "2", "imagem": None},
        {"id": "3", "nome": "Blusa Manga Longa", "tamanho": "P", "cor": "Branco", "preco": 59.90, "fornecedor_id": "1", "imagem": None},
    ]
    
    st.session_state.pedidos = [
        {"id": "1", "cliente_id": "1", "data": "2025-03-25", "produtos": [{"produto_id": "1", "quantidade": 1}], "valor_total": 89.90, "status": "Aguardando Pagamento"},
        {"id": "2", "cliente_id": "2", "data": "2025-03-26", "produtos": [{"produto_id": "2", "quantidade": 1}, {"produto_id": "3", "quantidade": 2}], "valor_total": 249.70, "status": "Pago"},
        {"id": "3", "cliente_id": "3", "data": "2025-03-27", "produtos": [{"produto_id": "3", "quantidade": 1}], "valor_total": 59.90, "status": "Entregue"}
    ]
    
    st.session_state.tarefas = [
        {"id": "1", "titulo": "Postar catálogo", "fornecedor_id": "1", "responsavel": "Vendedor 1", "prazo": "2025-04-05", "status": "Pendente", "descricao": "Postar catálogo nas redes sociais"},
        {"id": "2", "titulo": "Fechar pedido", "fornecedor_id": "1", "responsavel": "Gerente", "prazo": "2025-04-03", "status": "Em Andamento", "descricao": "Fechar pedido mensal com fornecedor"},
        {"id": "3", "titulo": "Cobrar clientes", "fornecedor_id": "2", "responsavel": "Financeiro", "prazo": "2025-04-02", "status": "Concluído", "descricao": "Cobrar clientes com pagamento pendente"},
        {"id": "4", "titulo": "Planilhar pedidos", "fornecedor_id": "3", "responsavel": "Assistente", "prazo": "2025-03-30", "status": "Atrasado", "descricao": "Organizar planilha de pedidos"}
    ]
    
    st.session_state.financeiro = {
        "receitas": [
            {"id": "1", "descricao": "Vendas Março", "valor": 5890.50, "data": "2025-03-31", "categoria": "Vendas"},
            {"id": "2", "descricao": "Consultoria de Moda", "valor": 350.00, "data": "2025-03-28", "categoria": "Serviços"}
        ],
        "despesas": [
            {"id": "1", "descricao": "Aluguel", "valor": 1200.00, "data": "2025-03-05", "categoria": "Fixas"},
            {"id": "2", "descricao": "Fornecedor A", "valor": 2500.00, "data": "2025-03-15", "categoria": "Estoque"},
            {"id": "3", "descricao": "Salários", "valor": 1800.00, "data": "2025-03-30", "categoria": "Pessoal"}
        ]
    }
    
    # Inicializar página atual
    st.session_state.pagina_atual = "Dashboard"
    
    # Inicializar variáveis de estado
    st.session_state.cliente_para_editar = None
    st.session_state.produto_para_editar = None
    st.session_state.fornecedor_para_editar = None
    st.session_state.tarefa_detalhes = None
    st.session_state.itens_pedido = []

# Funções auxiliares
def get_cliente_by_id(cliente_id):
    for cliente in st.session_state.clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None

def get_produto_by_id(produto_id):
    for produto in st.session_state.produtos:
        if produto["id"] == produto_id:
            return produto
    return None

def get_fornecedor_by_id(fornecedor_id):
    for fornecedor in st.session_state.fornecedores:
        if fornecedor["id"] == fornecedor_id:
            return fornecedor
    return None

def gerar_id():
    return str(uuid.uuid4())[:8]

def salvar_imagem(imagem_upload):
    if imagem_upload is not None:
        img = Image.open(imagem_upload)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

def mostrar_imagem(imagem_base64):
    if imagem_base64:
        st.image(f"data:image/png;base64,{imagem_base64}")
    else:
        st.write("Sem imagem disponível")

# Simulação de envio de mensagem WhatsApp
def simular_envio_whatsapp(numero, mensagem):
    st.success(f"Simulação: Mensagem enviada para {numero}: {mensagem}")
    return True

# Módulos do sistema
def mostrar_dashboard():
    st.markdown('<h2 class="sub-header">Dashboard</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Resumo Financeiro</h3>', unsafe_allow_html=True)
        
        total_receitas = sum(item["valor"] for item in st.session_state.financeiro["receitas"])
        total_despesas = sum(item["valor"] for item in st.session_state.financeiro["despesas"])
        lucro = total_receitas - total_despesas
        
        col_a, col_b = st.columns(2)
        col_a.metric("Receitas", f"R$ {total_receitas:.2f}")
        col_b.metric("Despesas", f"R$ {total_despesas:.2f}")
        st.metric("Lucro", f"R$ {lucro:.2f}", delta=f"{(lucro/total_receitas*100 if total_receitas > 0 else 0):.1f}%")
        
        # Gráfico de receitas x despesas
        fig, ax = plt.subplots(figsize=(8, 4))
        categorias = ['Receitas', 'Despesas', 'Lucro']
        valores = [total_receitas, total_despesas, lucro]
        cores = ['#4CAF50', '#F44336', '#2196F3']
        ax.bar(categorias, valores, color=cores)
        ax.set_ylabel('Valor (R$)')
        ax.set_title('Resumo Financeiro')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Status de Tarefas</h3>', unsafe_allow_html=True)
        
        status_counts = {"Pendente": 0, "Em Andamento": 0, "Concluído": 0, "Atrasado": 0}
        for tarefa in st.session_state.tarefas:
            status_counts[tarefa["status"]] += 1
        
        fig, ax = plt.subplots(figsize=(8, 4))
        cores = ['#FFC107', '#17A2B8', '#28A745', '#DC3545']
        ax.pie(
            status_counts.values(), 
            labels=status_counts.keys(), 
            autopct='%1.1f%%',
            colors=cores
        )
        ax.set_title('Distribuição de Tarefas por Status')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Pedidos recentes
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3>Pedidos Recentes</h3>', unsafe_allow_html=True)
    
    if st.session_state.pedidos:
        pedidos_df = []
        for pedido in st.session_state.pedidos:
            cliente = get_cliente_by_id(pedido["cliente_id"])
            pedidos_df.append({
                "ID": pedido["id"],
                "Cliente": cliente["nome"] if cliente else "Cliente não encontrado",
                "Data": pedido["data"],
                "Valor Total": f"R$ {pedido['valor_total']:.2f}",
                "Status": pedido["status"]
            })
        
        st.dataframe(pd.DataFrame(pedidos_df), use_container_width=True)
    else:
        st.info("Não há pedidos registrados.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tarefas pendentes
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3>Tarefas Pendentes</h3>', unsafe_allow_html=True)
    
    tarefas_pendentes = [t for t in st.session_state.tarefas if t["status"] in ["Pendente", "Atrasado"]]
    if tarefas_pendentes:
        for tarefa in tarefas_pendentes:
            fornecedor = get_fornecedor_by_id(tarefa["fornecedor_id"])
            status_class = "task-late" if tarefa["status"] == "Atrasado" else "task-pending"
            st.markdown(f"""
            <div class="task-box {status_class}">
                <strong>{tarefa["titulo"]}</strong> - {fornecedor["nome"] if fornecedor else "Fornecedor não encontrado"}<br>
                Responsável: {tarefa["responsavel"]} | Prazo: {tarefa["prazo"]} | Status: {tarefa["status"]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Não há tarefas pendentes.")
    st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_clientes():
    st.markdown('<h2 class="sub-header">Gerenciamento de Clientes</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Lista de Clientes", "Cadastrar Cliente"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Clientes Cadastrados")
        
        # Barra de pesquisa
        termo_busca = st.text_input("Buscar cliente por nome ou telefone:")
        
        if st.session_state.clientes:
            clientes_filtrados = st.session_state.clientes
            if termo_busca:
                clientes_filtrados = [c for c in st.session_state.clientes if 
                                     termo_busca.lower() in c["nome"].lower() or 
                                     termo_busca in c["telefone"]]
            
            if clientes_filtrados:
                for cliente in clientes_filtrados:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**Nome:** {cliente['nome']}")
                        st.write(f"**Telefone:** {cliente['telefone']}")
                    with col2:
                        st.write(f"**Endereço:** {cliente['endereco']}")
                    with col3:
                        if st.button("Editar", key=f"edit_{cliente['id']}"):
                            st.session_state.cliente_para_editar = cliente
                            st.rerun()
                        if st.button("Excluir", key=f"del_{cliente['id']}"):
                            st.session_state.clientes = [c for c in st.session_state.clientes if c["id"] != cliente["id"]]
                            st.success("Cliente excluído com sucesso!")
                            st.rerun()
                    st.divider()
            else:
                st.info("Nenhum cliente encontrado com os termos de busca.")
        else:
            st.info("Não há clientes cadastrados.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Cadastrar Novo Cliente")
        
        # Verifica se está em modo de edição
        cliente_editar = st.session_state.get("cliente_para_editar", None)
        
        with st.form("form_cliente"):
            nome = st.text_input("Nome completo:", value=cliente_editar["nome"] if cliente_editar else "")
            telefone = st.text_input("Telefone (com DDD):", value=cliente_editar["telefone"] if cliente_editar else "")
            endereco = st.text_input("Endereço completo:", value=cliente_editar["endereco"] if cliente_editar else "")
            
            submitted = st.form_submit_button("Salvar Cliente")
            
            if submitted:
                if cliente_editar:
                    # Modo edição
                    for i, cliente in enumerate(st.session_state.clientes):
                        if cliente["id"] == cliente_editar["id"]:
                            st.session_state.clientes[i] = {
                                "id": cliente_editar["id"],
                                "nome": nome,
                                "telefone": telefone,
                                "endereco": endereco
                            }
                    st.success("Cliente atualizado com sucesso!")
                    st.session_state.cliente_para_editar = None
                else:
                    # Novo cliente
                    novo_cliente = {
                        "id": gerar_id(),
                        "nome": nome,
                        "telefone": telefone,
                        "endereco": endereco
                    }
                    st.session_state.clientes.append(novo_cliente)
                    st.success("Cliente cadastrado com sucesso!")
                
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_produtos():
    st.markdown('<h2 class="sub-header">Gerenciamento de Produtos</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Lista de Produtos", "Cadastrar Produto"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Produtos Cadastrados")
        
        # Barra de pesquisa
        termo_busca = st.text_input("Buscar produto por nome, tamanho ou cor:")
        
        if st.session_state.produtos:
            produtos_filtrados = st.session_state.produtos
            if termo_busca:
                produtos_filtrados = [p for p in st.session_state.produtos if 
                                     termo_busca.lower() in p["nome"].lower() or 
                                     termo_busca.lower() in p["tamanho"].lower() or
                                     termo_busca.lower() in p["cor"].lower()]
            
            if produtos_filtrados:
                for produto in produtos_filtrados:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"**Nome:** {produto['nome']}")
                        st.write(f"**Tamanho:** {produto['tamanho']} | **Cor:** {produto['cor']}")
                    with col2:
                        fornecedor = get_fornecedor_by_id(produto["fornecedor_id"])
                        st.write(f"**Preço:** R$ {produto['preco']:.2f}")
                        st.write(f"**Fornecedor:** {fornecedor['nome'] if fornecedor else 'Não especificado'}")
                    with col3:
                        if produto["imagem"]:
                            mostrar_imagem(produto["imagem"])
                        
                        if st.button("Editar", key=f"edit_prod_{produto['id']}"):
                            st.session_state.produto_para_editar = produto
                            st.rerun()
                        if st.button("Excluir", key=f"del_prod_{produto['id']}"):
                            st.session_state.produtos = [p for p in st.session_state.produtos if p["id"] != produto["id"]]
                            st.success("Produto excluído com sucesso!")
                            st.rerun()
                    st.divider()
            else:
                st.info("Nenhum produto encontrado com os termos de busca.")
        else:
            st.info("Não há produtos cadastrados.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Cadastrar Novo Produto")
        
        # Verifica se está em modo de edição
        produto_editar = st.session_state.get("produto_para_editar", None)
        
        with st.form("form_produto"):
            nome = st.text_input("Nome do produto:", value=produto_editar["nome"] if produto_editar else "")
            
            col1, col2 = st.columns(2)
            with col1:
                tamanho = st.text_input("Tamanho:", value=produto_editar["tamanho"] if produto_editar else "")
            with col2:
                cor = st.text_input("Cor:", value=produto_editar["cor"] if produto_editar else "")
            
            preco = st.number_input("Preço (R$):", min_value=0.0, value=float(produto_editar["preco"]) if produto_editar else 0.0, step=0.01)
            
            fornecedor_options = ["Selecione..."] + [f["nome"] for f in st.session_state.fornecedores]
            fornecedor_index = 0
            
            if produto_editar and produto_editar["fornecedor_id"]:
                for i, f in enumerate(st.session_state.fornecedores):
                    if f["id"] == produto_editar["fornecedor_id"]:
                        fornecedor_index = i + 1  # +1 porque temos "Selecione..." na posição 0
                        break
            
            fornecedor_selecionado = st.selectbox(
                "Fornecedor:",
                options=fornecedor_options,
                index=fornecedor_index
            )
            
            imagem_upload = st.file_uploader("Imagem do produto:", type=["jpg", "jpeg", "png"])
            
            if produto_editar and produto_editar["imagem"] and not imagem_upload:
                st.write("Imagem atual:")
                mostrar_imagem(produto_editar["imagem"])
            
            submitted = st.form_submit_button("Salvar Produto")
            
            if submitted:
                # Processar imagem
                imagem_base64 = None
                if imagem_upload:
                    imagem_base64 = salvar_imagem(imagem_upload)
                elif produto_editar and produto_editar["imagem"]:
                    imagem_base64 = produto_editar["imagem"]
                
                # Obter ID do fornecedor
                fornecedor_id = None
                if fornecedor_selecionado != "Selecione...":
                    for f in st.session_state.fornecedores:
                        if f["nome"] == fornecedor_selecionado:
                            fornecedor_id = f["id"]
                            break
                
                if produto_editar:
                    # Modo edição
                    for i, produto in enumerate(st.session_state.produtos):
                        if produto["id"] == produto_editar["id"]:
                            st.session_state.produtos[i] = {
                                "id": produto_editar["id"],
                                "nome": nome,
                                "tamanho": tamanho,
                                "cor": cor,
                                "preco": preco,
                                "fornecedor_id": fornecedor_id,
                                "imagem": imagem_base64
                            }
                    st.success("Produto atualizado com sucesso!")
                    st.session_state.produto_para_editar = None
                else:
                    # Novo produto
                    novo_produto = {
                        "id": gerar_id(),
                        "nome": nome,
                        "tamanho": tamanho,
                        "cor": cor,
                        "preco": preco,
                        "fornecedor_id": fornecedor_id,
                        "imagem": imagem_base64
                    }
                    st.session_state.produtos.append(novo_produto)
                    st.success("Produto cadastrado com sucesso!")
                
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_pedidos():
    st.markdown('<h2 class="sub-header">Gerenciamento de Pedidos</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Lista de Pedidos", "Novo Pedido"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Pedidos Registrados")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_status = st.multiselect(
                "Filtrar por status:",
                options=["Todos", "Aguardando Pagamento", "Pago", "Em Preparação", "Pronto para Retirada", "Entregue"],
                default=["Todos"]
            )
        with col2:
            filtro_cliente = st.selectbox(
                "Filtrar por cliente:",
                options=["Todos"] + [c["nome"] for c in st.session_state.clientes]
            )
        
        if st.session_state.pedidos:
            pedidos_filtrados = st.session_state.pedidos
            
            # Aplicar filtros
            if "Todos" not in filtro_status:
                pedidos_filtrados = [p for p in pedidos_filtrados if p["status"] in filtro_status]
            
            if filtro_cliente != "Todos":
                cliente_id = next((c["id"] for c in st.session_state.clientes if c["nome"] == filtro_cliente), None)
                if cliente_id:
                    pedidos_filtrados = [p for p in pedidos_filtrados if p["cliente_id"] == cliente_id]
            
            if pedidos_filtrados:
                for pedido in pedidos_filtrados:
                    cliente = get_cliente_by_id(pedido["cliente_id"])
                    
                    st.markdown(f"""
                    <div class="pink-box">
                        <strong>Pedido #{pedido['id']}</strong> - {pedido['data']} - {pedido['status']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Cliente:** {cliente['nome'] if cliente else 'Cliente não encontrado'}")
                        st.write(f"**Telefone:** {cliente['telefone'] if cliente else 'N/A'}")
                    
                    with col2:
                        st.write("**Produtos:**")
                        for item in pedido["produtos"]:
                            produto = get_produto_by_id(item["produto_id"])
                            if produto:
                                st.write(f"- {produto['nome']} ({produto['tamanho']}, {produto['cor']}) x{item['quantidade']}")
                    
                    with col3:
                        st.write(f"**Total:** R$ {pedido['valor_total']:.2f}")
                        
                        # Opções de atualização de status
                        novo_status = st.selectbox(
                            "Atualizar status:",
                            options=["Aguardando Pagamento", "Pago", "Em Preparação", "Pronto para Retirada", "Entregue"],
                            index=["Aguardando Pagamento", "Pago", "Em Preparação", "Pronto para Retirada", "Entregue"].index(pedido["status"]),
                            key=f"status_{pedido['id']}"
                        )
                        
                        if st.button("Atualizar", key=f"update_{pedido['id']}"):
                            # Atualizar status do pedido
                            for i, p in enumerate(st.session_state.pedidos):
                                if p["id"] == pedido["id"]:
                                    st.session_state.pedidos[i]["status"] = novo_status
                                    
                                    # Se status for "Pronto para Retirada", enviar notificação
                                    if novo_status == "Pronto para Retirada" and cliente:
                                        mensagem = f"Olá {cliente['nome'].split()[0]}! Seu pedido #{pedido['id']} está pronto para retirada na Nosso Closet RN. Aguardamos sua visita!"
                                        simular_envio_whatsapp(cliente["telefone"], mensagem)
                                    
                                    # Se status mudar para "Aguardando Pagamento", enviar lembrete
                                    if novo_status == "Aguardando Pagamento" and cliente:
                                        mensagem = f"Olá {cliente['nome'].split()[0]}! Lembramos que seu pedido #{pedido['id']} no valor de R$ {pedido['valor_total']:.2f} está aguardando pagamento. Para mais informações, entre em contato conosco."
                                        simular_envio_whatsapp(cliente["telefone"], mensagem)
                            
                            st.success(f"Status do pedido atualizado para: {novo_status}")
                            st.rerun()
                    
                    st.divider()
            else:
                st.info("Nenhum pedido encontrado com os filtros selecionados.")
        else:
            st.info("Não há pedidos registrados.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Registrar Novo Pedido")
        
        # Selecionar cliente
        cliente_options = ["Selecione..."] + [c["nome"] for c in st.session_state.clientes]
        cliente_selecionado = st.selectbox("Cliente:", options=cliente_options)
        
        if cliente_selecionado != "Selecione...":
            cliente_id = next((c["id"] for c in st.session_state.clientes if c["nome"] == cliente_selecionado), None)
            
            # Inicializar lista de itens se não existir
            if "itens_pedido" not in st.session_state:
                st.session_state.itens_pedido = []
            
            # Adicionar produtos ao pedido
            st.subheader("Adicionar Produtos")
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                produto_options = ["Selecione..."] + [p["nome"] + f" ({p['tamanho']}, {p['cor']})" for p in st.session_state.produtos]
                produto_selecionado = st.selectbox("Produto:", options=produto_options)
            
            with col2:
                quantidade = st.number_input("Quantidade:", min_value=1, value=1)
            
            with col3:
                st.write("")
                st.write("")
                if st.button("Adicionar ao Pedido") and produto_selecionado != "Selecione...":
                    # Encontrar o produto selecionado
                    produto_nome = produto_selecionado.split(" (")[0]
                    produto_id = next((p["id"] for p in st.session_state.produtos if p["nome"] == produto_nome), None)
                    
                    if produto_id:
                        produto = get_produto_by_id(produto_id)
                        
                        # Verificar se o produto já está no pedido
                        item_existente = False
                        for i, item in enumerate(st.session_state.itens_pedido):
                            if item["produto_id"] == produto_id:
                                st.session_state.itens_pedido[i]["quantidade"] += quantidade
                                item_existente = True
                                break
                        
                        if not item_existente:
                            st.session_state.itens_pedido.append({
                                "produto_id": produto_id,
                                "quantidade": quantidade
                            })
                        
                        st.success(f"Produto adicionado ao pedido: {produto_nome}")
                        st.rerun()
            
            # Mostrar itens do pedido
            if st.session_state.itens_pedido:
                st.subheader("Itens do Pedido")
                
                valor_total = 0
                
                for i, item in enumerate(st.session_state.itens_pedido):
                    produto = get_produto_by_id(item["produto_id"])
                    if produto:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        
                        with col1:
                            st.write(f"{produto['nome']} ({produto['tamanho']}, {produto['cor']})")
                        
                        with col2:
                            st.write(f"Qtd: {item['quantidade']}")
                        
                        with col3:
                            subtotal = produto["preco"] * item["quantidade"]
                            valor_total += subtotal
                            st.write(f"R$ {subtotal:.2f}")
                        
                        with col4:
                            if st.button("Remover", key=f"remove_{i}"):
                                st.session_state.itens_pedido.pop(i)
                                st.rerun()
                
                st.markdown(f"**Valor Total: R$ {valor_total:.2f}**")
                
                # Finalizar pedido
                data_pedido = st.date_input("Data do pedido:", datetime.datetime.now())
                status_inicial = st.selectbox("Status inicial:", options=["Aguardando Pagamento", "Pago", "Em Preparação"])
                
                if st.button("Finalizar Pedido"):
                    if st.session_state.itens_pedido:
                        # Calcular valor total novamente
                        valor_total = 0
                        for item in st.session_state.itens_pedido:
                            produto = get_produto_by_id(item["produto_id"])
                            if produto:
                                valor_total += produto["preco"] * item["quantidade"]
                        
                        # Criar novo pedido
                        novo_pedido = {
                            "id": gerar_id(),
                            "cliente_id": cliente_id,
                            "data": data_pedido.strftime("%Y-%m-%d"),
                            "produtos": st.session_state.itens_pedido.copy(),
                            "valor_total": valor_total,
                            "status": status_inicial
                        }
                        
                        st.session_state.pedidos.append(novo_pedido)
                        
                        # Enviar notificação de pedido criado
                        cliente = get_cliente_by_id(cliente_id)
                        if cliente:
                            mensagem = f"Olá {cliente['nome'].split()[0]}! Seu pedido #{novo_pedido['id']} no valor de R$ {valor_total:.2f} foi registrado com sucesso. Agradecemos a preferência!"
                            simular_envio_whatsapp(cliente["telefone"], mensagem)
                            
                            # Se for aguardando pagamento, enviar dados para pagamento
                            if status_inicial == "Aguardando Pagamento":
                                mensagem_pagamento = f"Para finalizar seu pedido, realize o pagamento via PIX para a chave: contato@nossocloset.com.br"
                                simular_envio_whatsapp(cliente["telefone"], mensagem_pagamento)
                        
                        # Limpar itens do pedido
                        st.session_state.itens_pedido = []
                        
                        st.success("Pedido registrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Adicione pelo menos um produto ao pedido.")
            else:
                st.info("Nenhum produto adicionado ao pedido ainda.")
        else:
            st.info("Selecione um cliente para continuar.")
        st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_tarefas():
    st.markdown('<h2 class="sub-header">Gerenciamento de Tarefas</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Filtros")
        
        filtro_fornecedor = st.selectbox(
            "Fornecedor:",
            options=["Todos"] + [f["nome"] for f in st.session_state.fornecedores]
        )
        
        filtro_status = st.multiselect(
            "Status:",
            options=["Todos", "Pendente", "Em Andamento", "Concluído", "Atrasado"],
            default=["Todos"]
        )
        
        filtro_responsavel = st.text_input("Responsável:")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Seção para adicionar nova tarefa
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Nova Tarefa")
        
        with st.form("form_tarefa"):
            titulo = st.text_input("Título da tarefa:")
            descricao = st.text_area("Descrição:")
            
            fornecedor_options = ["Selecione..."] + [f["nome"] for f in st.session_state.fornecedores]
            fornecedor_selecionado = st.selectbox("Fornecedor:", options=fornecedor_options)
            
            responsavel = st.text_input("Responsável:")
            prazo = st.date_input("Prazo:", datetime.datetime.now() + datetime.timedelta(days=7))
            status = st.selectbox("Status inicial:", options=["Pendente", "Em Andamento"])
            
            submitted = st.form_submit_button("Adicionar Tarefa")
            
            if submitted:
                if titulo and fornecedor_selecionado != "Selecione...":
                    # Obter ID do fornecedor
                    fornecedor_id = next((f["id"] for f in st.session_state.fornecedores if f["nome"] == fornecedor_selecionado), None)
                    
                    if fornecedor_id:
                        nova_tarefa = {
                            "id": gerar_id(),
                            "titulo": titulo,
                            "descricao": descricao,
                            "fornecedor_id": fornecedor_id,
                            "responsavel": responsavel,
                            "prazo": prazo.strftime("%Y-%m-%d"),
                            "status": status
                        }
                        
                        st.session_state.tarefas.append(nova_tarefa)
                        st.success("Tarefa adicionada com sucesso!")
                        st.rerun()
                else:
                    st.error("Preencha o título e selecione um fornecedor.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Tarefas")
        
        # Aplicar filtros
        tarefas_filtradas = st.session_state.tarefas
        
        if filtro_fornecedor != "Todos":
            fornecedor_id = next((f["id"] for f in st.session_state.fornecedores if f["nome"] == filtro_fornecedor), None)
            if fornecedor_id:
                tarefas_filtradas = [t for t in tarefas_filtradas if t["fornecedor_id"] == fornecedor_id]
        
        if "Todos" not in filtro_status:
            tarefas_filtradas = [t for t in tarefas_filtradas if t["status"] in filtro_status]
        
        if filtro_responsavel:
            tarefas_filtradas = [t for t in tarefas_filtradas if filtro_responsavel.lower() in t["responsavel"].lower()]
        
        # Agrupar por status
        tarefas_por_status = {
            "Pendente": [],
            "Em Andamento": [],
            "Concluído": [],
            "Atrasado": []
        }
        
        for tarefa in tarefas_filtradas:
            tarefas_por_status[tarefa["status"]].append(tarefa)
        
        # Mostrar tarefas em colunas por status
        status_cols = st.columns(4)
        
        for i, (status, tarefas) in enumerate(tarefas_por_status.items()):
            with status_cols[i]:
                st.markdown(f"<h4>{status} ({len(tarefas)})</h4>", unsafe_allow_html=True)
                
                status_class = {
                    "Pendente": "task-pending",
                    "Em Andamento": "task-progress",
                    "Concluído": "task-completed",
                    "Atrasado": "task-late"
                }[status]
                
                for tarefa in tarefas:
                    fornecedor = get_fornecedor_by_id(tarefa["fornecedor_id"])
                    
                    st.markdown(f"""
                    <div class="task-box {status_class}">
                        <strong>{tarefa["titulo"]}</strong><br>
                        Fornecedor: {fornecedor["nome"] if fornecedor else "Não especificado"}<br>
                        Responsável: {tarefa["responsavel"]}<br>
                        Prazo: {tarefa["prazo"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Detalhes", key=f"details_{tarefa['id']}"):
                            st.session_state.tarefa_detalhes = tarefa
                            st.rerun()
                    
                    with col2:
                        if status != "Concluído" and st.button("Concluir", key=f"complete_{tarefa['id']}"):
                            for i, t in enumerate(st.session_state.tarefas):
                                if t["id"] == tarefa["id"]:
                                    st.session_state.tarefas[i]["status"] = "Concluído"
                            st.success("Tarefa marcada como concluída!")
                            st.rerun()
        
        # Modal de detalhes da tarefa
        if "tarefa_detalhes" in st.session_state and st.session_state.tarefa_detalhes:
            tarefa = st.session_state.tarefa_detalhes
            fornecedor = get_fornecedor_by_id(tarefa["fornecedor_id"])
            
            st.divider()
            st.subheader(f"Detalhes da Tarefa: {tarefa['titulo']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Fornecedor:** {fornecedor['nome'] if fornecedor else 'Não especificado'}")
                st.write(f"**Responsável:** {tarefa['responsavel']}")
                st.write(f"**Prazo:** {tarefa['prazo']}")
                st.write(f"**Status:** {tarefa['status']}")
            
            with col2:
                st.write("**Descrição:**")
                st.write(tarefa["descricao"])
            
            # Opções de atualização
            col1, col2, col3 = st.columns(3)
            
            with col1:
                novo_status = st.selectbox(
                    "Atualizar status:",
                    options=["Pendente", "Em Andamento", "Concluído", "Atrasado"],
                    index=["Pendente", "Em Andamento", "Concluído", "Atrasado"].index(tarefa["status"])
                )
            
            with col2:
                novo_responsavel = st.text_input("Atualizar responsável:", value=tarefa["responsavel"])
            
            with col3:
                novo_prazo = st.date_input("Atualizar prazo:", datetime.datetime.strptime(tarefa["prazo"], "%Y-%m-%d"))
            
            if st.button("Salvar Alterações"):
                for i, t in enumerate(st.session_state.tarefas):
                    if t["id"] == tarefa["id"]:
                        st.session_state.tarefas[i]["status"] = novo_status
                        st.session_state.tarefas[i]["responsavel"] = novo_responsavel
                        st.session_state.tarefas[i]["prazo"] = novo_prazo.strftime("%Y-%m-%d")
                
                st.success("Tarefa atualizada com sucesso!")
                st.session_state.tarefa_detalhes = None
                st.rerun()
            
            if st.button("Fechar"):
                st.session_state.tarefa_detalhes = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_fornecedores():
    st.markdown('<h2 class="sub-header">Gerenciamento de Fornecedores</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Lista de Fornecedores", "Cadastrar Fornecedor"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Fornecedores Cadastrados")
        
        if st.session_state.fornecedores:
            for fornecedor in st.session_state.fornecedores:
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Nome:** {fornecedor['nome']}")
                
                with col2:
                    st.write(f"**Contato:** {fornecedor['contato']}")
                    st.write(f"**Taxa:** {fornecedor['taxa']*100:.1f}%")
                
                with col3:
                    if st.button("Editar", key=f"edit_forn_{fornecedor['id']}"):
                        st.session_state.fornecedor_para_editar = fornecedor
                        st.rerun()
                    
                    if st.button("Excluir", key=f"del_forn_{fornecedor['id']}"):
                        # Verificar se há produtos associados
                        produtos_associados = [p for p in st.session_state.produtos if p["fornecedor_id"] == fornecedor["id"]]
                        if produtos_associados:
                            st.error(f"Não é possível excluir. Existem {len(produtos_associados)} produtos associados a este fornecedor.")
                        else:
                            st.session_state.fornecedores = [f for f in st.session_state.fornecedores if f["id"] != fornecedor["id"]]
                            st.success("Fornecedor excluído com sucesso!")
                            st.rerun()
                
                # Lista de tarefas do fornecedor
                tarefas_fornecedor = [t for t in st.session_state.tarefas if t["fornecedor_id"] == fornecedor["id"]]
                if tarefas_fornecedor:
                    with st.expander(f"Tarefas ({len(tarefas_fornecedor)})"):
                        for tarefa in tarefas_fornecedor:
                            status_class = {
                                "Pendente": "task-pending",
                                "Em Andamento": "task-progress",
                                "Concluído": "task-completed",
                                "Atrasado": "task-late"
                            }[tarefa["status"]]
                            
                            st.markdown(f"""
                            <div class="task-box {status_class}">
                                <strong>{tarefa["titulo"]}</strong> - {tarefa["status"]}<br>
                                Responsável: {tarefa["responsavel"]} | Prazo: {tarefa["prazo"]}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Lista de produtos do fornecedor
                produtos_fornecedor = [p for p in st.session_state.produtos if p["fornecedor_id"] == fornecedor["id"]]
                if produtos_fornecedor:
                    with st.expander(f"Produtos ({len(produtos_fornecedor)})"):
                        for produto in produtos_fornecedor:
                            st.write(f"- {produto['nome']} ({produto['tamanho']}, {produto['cor']}) - R$ {produto['preco']:.2f}")
                
                st.divider()
        else:
            st.info("Não há fornecedores cadastrados.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Cadastrar Novo Fornecedor")
        
        # Verifica se está em modo de edição
        fornecedor_editar = st.session_state.get("fornecedor_para_editar", None)
        
        with st.form("form_fornecedor"):
            nome = st.text_input("Nome do fornecedor:", value=fornecedor_editar["nome"] if fornecedor_editar else "")
            contato = st.text_input("Contato (telefone/email):", value=fornecedor_editar["contato"] if fornecedor_editar else "")
            
            taxa_percent = st.slider(
                "Taxa por peça (%):",
                min_value=0.0,
                max_value=50.0,
                value=fornecedor_editar["taxa"]*100 if fornecedor_editar else 15.0,
                step=0.5
            )
            taxa = taxa_percent / 100
            
            submitted = st.form_submit_button("Salvar Fornecedor")
            
            if submitted:
                if fornecedor_editar:
                    # Modo edição
                    for i, fornecedor in enumerate(st.session_state.fornecedores):
                        if fornecedor["id"] == fornecedor_editar["id"]:
                            st.session_state.fornecedores[i] = {
                                "id": fornecedor_editar["id"],
                                "nome": nome,
                                "contato": contato,
                                "taxa": taxa
                            }
                    st.success("Fornecedor atualizado com sucesso!")
                    st.session_state.fornecedor_para_editar = None
                else:
                    # Novo fornecedor
                    novo_fornecedor = {
                        "id": gerar_id(),
                        "nome": nome,
                        "contato": contato,
                        "taxa": taxa
                    }
                    st.session_state.fornecedores.append(novo_fornecedor)
                    st.success("Fornecedor cadastrado com sucesso!")
                
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_financeiro():
    st.markdown('<h2 class="sub-header">Gerenciamento Financeiro</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Visão Geral", "Receitas", "Despesas"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Resumo Financeiro")
        
        # Cálculos financeiros
        total_receitas = sum(item["valor"] for item in st.session_state.financeiro["receitas"])
        total_despesas = sum(item["valor"] for item in st.session_state.financeiro["despesas"])
        lucro = total_receitas - total_despesas
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Receitas Totais", f"R$ {total_receitas:.2f}")
        
        with col2:
            st.metric("Despesas Totais", f"R$ {total_despesas:.2f}")
        
        with col3:
            st.metric("Lucro", f"R$ {lucro:.2f}", delta=f"{(lucro/total_receitas*100 if total_receitas > 0 else 0):.1f}%")
        
        # Gráfico de barras
        st.subheader("Receitas x Despesas")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        categorias = ['Receitas', 'Despesas', 'Lucro']
        valores = [total_receitas, total_despesas, lucro]
        cores = ['#4CAF50', '#F44336', '#2196F3']
        ax.bar(categorias, valores, color=cores)
        ax.set_ylabel('Valor (R$)')
        ax.set_title('Resumo Financeiro')
        
        for i, v in enumerate(valores):
            ax.text(i, v + 50, f"R$ {v:.2f}", ha='center')
        
        st.pyplot(fig)
        
        # Gráfico de pizza para despesas por categoria
        st.subheader("Despesas por Categoria")
        
        despesas_por_categoria = {}
        for despesa in st.session_state.financeiro["despesas"]:
            categoria = despesa["categoria"]
            if categoria not in despesas_por_categoria:
                despesas_por_categoria[categoria] = 0
            despesas_por_categoria[categoria] += despesa["valor"]
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            despesas_por_categoria.values(),
            labels=despesas_por_categoria.keys(),
            autopct='%1.1f%%',
            startangle=90
        )
        ax.axis('equal')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Gerenciar Receitas")
        
        # Formulário para adicionar receita
        with st.form("form_receita"):
            st.write("Nova Receita")
            
            descricao = st.text_input("Descrição:")
            valor = st.number_input("Valor (R$):", min_value=0.01, step=0.01)
            data = st.date_input("Data:", datetime.datetime.now())
            categoria = st.selectbox("Categoria:", options=["Vendas", "Serviços", "Outros"])
            
            submitted = st.form_submit_button("Adicionar Receita")
            
            if submitted:
                nova_receita = {
                    "id": gerar_id(),
                    "descricao": descricao,
                    "valor": valor,
                    "data": data.strftime("%Y-%m-%d"),
                    "categoria": categoria
                }
                
                st.session_state.financeiro["receitas"].append(nova_receita)
                st.success("Receita adicionada com sucesso!")
                st.rerun()
        
        # Lista de receitas
        st.subheader("Receitas Registradas")
        
        if st.session_state.financeiro["receitas"]:
            receitas_df = []
            for receita in st.session_state.financeiro["receitas"]:
                receitas_df.append({
                    "ID": receita["id"],
                    "Descrição": receita["descricao"],
                    "Valor": f"R$ {receita['valor']:.2f}",
                    "Data": receita["data"],
                    "Categoria": receita["categoria"]
                })
            
            st.dataframe(pd.DataFrame(receitas_df), use_container_width=True)
            
            # Opção para excluir receita
            receita_para_excluir = st.selectbox(
                "Selecione uma receita para excluir:",
                options=["Selecione..."] + [f"{r['descricao']} - R$ {r['valor']:.2f} ({r['data']})" for r in st.session_state.financeiro["receitas"]]
            )
            
            if receita_para_excluir != "Selecione..." and st.button("Excluir Receita"):
                descricao_valor = receita_para_excluir.split(" - ")[0]
                for i, receita in enumerate(st.session_state.financeiro["receitas"]):
                    if receita["descricao"] == descricao_valor:
                        st.session_state.financeiro["receitas"].pop(i)
                        st.success("Receita excluída com sucesso!")
                        st.rerun()
                        break
        else:
            st.info("Não há receitas registradas.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Gerenciar Despesas")
        
        # Formulário para adicionar despesa
        with st.form("form_despesa"):
            st.write("Nova Despesa")
            
            descricao = st.text_input("Descrição:")
            valor = st.number_input("Valor (R$):", min_value=0.01, step=0.01)
            data = st.date_input("Data:", datetime.datetime.now())
            categoria = st.selectbox("Categoria:", options=["Fixas", "Estoque", "Pessoal", "Marketing", "Outros"])
            
            submitted = st.form_submit_button("Adicionar Despesa")
            
            if submitted:
                nova_despesa = {
                    "id": gerar_id(),
                    "descricao": descricao,
                    "valor": valor,
                    "data": data.strftime("%Y-%m-%d"),
                    "categoria": categoria
                }
                
                st.session_state.financeiro["despesas"].append(nova_despesa)
                st.success("Despesa adicionada com sucesso!")
                st.rerun()
        
        # Lista de despesas
        st.subheader("Despesas Registradas")
        
        if st.session_state.financeiro["despesas"]:
            despesas_df = []
            for despesa in st.session_state.financeiro["despesas"]:
                despesas_df.append({
                    "ID": despesa["id"],
                    "Descrição": despesa["descricao"],
                    "Valor": f"R$ {despesa['valor']:.2f}",
                    "Data": despesa["data"],
                    "Categoria": despesa["categoria"]
                })
            
            st.dataframe(pd.DataFrame(despesas_df), use_container_width=True)
            
            # Opção para excluir despesa
            despesa_para_excluir = st.selectbox(
                "Selecione uma despesa para excluir:",
                options=["Selecione..."] + [f"{d['descricao']} - R$ {d['valor']:.2f} ({d['data']})" for d in st.session_state.financeiro["despesas"]]
            )
            
            if despesa_para_excluir != "Selecione..." and st.button("Excluir Despesa"):
                descricao_valor = despesa_para_excluir.split(" - ")[0]
                for i, despesa in enumerate(st.session_state.financeiro["despesas"]):
                    if despesa["descricao"] == descricao_valor:
                        st.session_state.financeiro["despesas"].pop(i)
                        st.success("Despesa excluída com sucesso!")
                        st.rerun()
                        break
        else:
            st.info("Não há despesas registradas.")
        st.markdown('</div>', unsafe_allow_html=True)

def gerenciar_notificacoes():
    st.markdown('<h2 class="sub-header">Sistema de Notificações</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Enviar Notificações", "Automações"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Enviar Notificação Manual")
        
        # Selecionar cliente
        cliente_options = ["Selecione..."] + [c["nome"] for c in st.session_state.clientes]
        cliente_selecionado = st.selectbox("Cliente:", options=cliente_options)
        
        if cliente_selecionado != "Selecione...":
            cliente = next((c for c in st.session_state.clientes if c["nome"] == cliente_selecionado), None)
            
            if cliente:
                st.write(f"Telefone: {cliente['telefone']}")
                
                # Modelos de mensagem
                modelo_mensagem = st.selectbox(
                    "Modelo de mensagem:",
                    options=[
                        "Personalizada",
                        "Lembrete de Pagamento",
                        "Produto Disponível para Retirada",
                        "Promoção",
                        "Novos Produtos",
                        "Agradecimento"
                    ]
                )
                
                if modelo_mensagem == "Personalizada":
                    mensagem = st.text_area("Digite sua mensagem:", value=f"Olá {cliente['nome'].split()[0]}, ")
                elif modelo_mensagem == "Lembrete de Pagamento":
                    # Buscar pedidos pendentes do cliente
                    pedidos_pendentes = [p for p in st.session_state.pedidos if p["cliente_id"] == cliente["id"] and p["status"] == "Aguardando Pagamento"]
                    
                    if pedidos_pendentes:
                        pedido_select = st.selectbox(
                            "Selecione o pedido:",
                            options=[f"Pedido #{p['id']} - R$ {p['valor_total']:.2f} ({p['data']})" for p in pedidos_pendentes]
                        )
                        
                        pedido_id = pedido_select.split(" - ")[0].replace("Pedido #", "")
                        pedido = next((p for p in pedidos_pendentes if p["id"] == pedido_id), None)
                        
                        if pedido:
                            mensagem = f"Olá {cliente['nome'].split()[0]}! Gostaríamos de lembrar sobre o pagamento pendente do seu Pedido #{pedido['id']} no valor de R$ {pedido['valor_total']:.2f}. Para mais informações, entre em contato conosco."
                    else:
                        st.warning("Este cliente não possui pedidos com pagamento pendente.")
                        mensagem = ""
                elif modelo_mensagem == "Produto Disponível para Retirada":
                    # Buscar pedidos pagos do cliente
                    pedidos_pagos = [p for p in st.session_state.pedidos if p["cliente_id"] == cliente["id"] and p["status"] == "Pago"]
                    
                    if pedidos_pagos:
                        pedido_select = st.selectbox(
                            "Selecione o pedido:",
                            options=[f"Pedido #{p['id']} - R$ {p['valor_total']:.2f} ({p['data']})" for p in pedidos_pagos]
                        )
                        
                        pedido_id = pedido_select.split(" - ")[0].replace("Pedido #", "")
                        pedido = next((p for p in pedidos_pagos if p["id"] == pedido_id), None)
                        
                        if pedido:
                            mensagem = f"Olá {cliente['nome'].split()[0]}! Seu pedido #{pedido['id']} já está disponível para retirada na Nosso Closet RN. Aguardamos sua visita!"
                    else:
                        st.warning("Este cliente não possui pedidos pagos.")
                        mensagem = ""
                elif modelo_mensagem == "Promoção":
                    mensagem = f"Olá {cliente['nome'].split()[0]}! A Nosso Closet RN está com uma promoção especial esta semana. Aproveite descontos de até 30% em peças selecionadas. Venha conferir!"
                elif modelo_mensagem == "Novos Produtos":
                    mensagem = f"Olá {cliente['nome'].split()[0]}! Acabamos de receber novos produtos na Nosso Closet RN. Venha conferir as novidades e garanta as melhores peças!"
                elif modelo_mensagem == "Agradecimento":
                    mensagem = f"Olá {cliente['nome'].split()[0]}! Gostaríamos de agradecer por sua preferência. É sempre um prazer atendê-lo(a) na Nosso Closet RN. Volte sempre!"
                
                if mensagem:
                    st.text_area("Mensagem a ser enviada:", value=mensagem, height=150, disabled=True)
                    
                    if st.button("Enviar Notificação"):
                        sucesso = simular_envio_whatsapp(cliente["telefone"], mensagem)
                        if sucesso:
                            st.success("Notificação enviada com sucesso!")
                        else:
                            st.error("Erro ao enviar notificação. Verifique o número de telefone.")
        else:
            st.info("Selecione um cliente para enviar uma notificação.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Envio em massa
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Envio em Massa")
        
        tipo_selecao = st.radio("Selecionar clientes por:", options=["Todos os Clientes", "Clientes com Pedidos Pendentes", "Clientes Inativos"])
        
        clientes_selecionados = []
        
        if tipo_selecao == "Todos os Clientes":
            clientes_selecionados = st.session_state.clientes
        elif tipo_selecao == "Clientes com Pedidos Pendentes":
            # Clientes com pedidos aguardando pagamento
            clientes_com_pendencia = set()
            for pedido in st.session_state.pedidos:
                if pedido["status"] == "Aguardando Pagamento":
                    clientes_com_pendencia.add(pedido["cliente_id"])
            
            clientes_selecionados = [c for c in st.session_state.clientes if c["id"] in clientes_com_pendencia]
        elif tipo_selecao == "Clientes Inativos":
            # Simulando clientes inativos (sem pedidos nos últimos 30 dias)
            hoje = datetime.datetime.now()
            clientes_ativos = set()
            
            for pedido in st.session_state.pedidos:
                data_pedido = datetime.datetime.strptime(pedido["data"], "%Y-%m-%d")
                if (hoje - data_pedido).days <= 30:
                    clientes_ativos.add(pedido["cliente_id"])
            
            clientes_selecionados = [c for c in st.session_state.clientes if c["id"] not in clientes_ativos]
        
        st.write(f"Clientes selecionados: {len(clientes_selecionados)}")
        
        if clientes_selecionados:
            # Lista dos clientes selecionados
            with st.expander("Ver clientes selecionados"):
                for cliente in clientes_selecionados:
                    st.write(f"- {cliente['nome']} ({cliente['telefone']})")
            
            # Mensagem para envio em massa
            mensagem_massa = st.text_area(
                "Mensagem para envio em massa:",
                value="Olá! A Nosso Closet RN tem uma mensagem especial para você: "
            )
            
            if st.button("Enviar para Todos Selecionados"):
                progresso = st.progress(0)
                for i, cliente in enumerate(clientes_selecionados):
                    # Personalizar mensagem com nome do cliente
                    mensagem_personalizada = mensagem_massa.replace("Olá!", f"Olá {cliente['nome'].split()[0]}!")
                    
                    # Simular envio
                    simular_envio_whatsapp(cliente["telefone"], mensagem_personalizada)
                    
                    # Atualizar barra de progresso
                    progresso.progress((i + 1) / len(clientes_selecionados))
                
                st.success(f"Mensagens enviadas com sucesso para {len(clientes_selecionados)} clientes!")
        else:
            st.info("Nenhum cliente encontrado com os critérios selecionados.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Configurar Automações")
        
        st.write("Configure notificações automáticas para seus clientes")
        
        # Automação de lembrete de pagamento
        st.subheader("Lembrete de Pagamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            lembrete_pagamento_ativo = st.checkbox("Ativar lembretes de pagamento", value=True)
        
        with col2:
            dias_lembrete = st.number_input("Enviar lembrete após (dias):", min_value=1, value=3)
        
        mensagem_lembrete = st.text_area(
            "Mensagem de lembrete:",
            value="Olá {nome}! Gostaríamos de lembrar que seu pedido #{pedido} no valor de R$ {valor} está pendente de pagamento. Agradecemos sua atenção!"
        )
        
        # Automação de produto disponível
        st.subheader("Produto Disponível para Retirada")
        
        col1, col2 = st.columns(2)
        
        with col1:
            notif_disponivel_ativo = st.checkbox("Ativar notificação de produto disponível", value=True)
        
        with col2:
            dias_disponivel = st.number_input("Notificar após (dias da compra):", min_value=1, value=7)
        
        mensagem_disponivel = st.text_area(
            "Mensagem de produto disponível:",
            value="Olá {nome}! Seu pedido #{pedido} já está disponível para retirada na Nosso Closet RN. Aguardamos sua visita!"
        )
        
        # Automação de promoções
        st.subheader("Promoções e Novidades")
        
        col1, col2 = st.columns(2)
        
        with col1:
            promocoes_ativo = st.checkbox("Ativar notificações de promoções", value=True)
        
        with col2:
            frequencia_promocoes = st.selectbox(
                "Frequência de envio:",
                options=["Semanal", "Quinzenal", "Mensal"]
            )
        
        mensagem_promocao = st.text_area(
            "Mensagem de promoção:",
            value="Olá {nome}! A Nosso Closet RN está com promoções especiais esta semana. Venha conferir e aproveite!"
        )
        
        # Salvar configurações
        if st.button("Salvar Configurações de Automação"):
            # Em um sistema real, essas configurações seriam salvas em um banco de dados
            # Aqui apenas simulamos o salvamento
            st.session_state.automacoes = {
                "lembrete_pagamento": {
                    "ativo": lembrete_pagamento_ativo,
                    "dias": dias_lembrete,
                    "mensagem": mensagem_lembrete
                },
                "produto_disponivel": {
                    "ativo": notif_disponivel_ativo,
                    "dias": dias_disponivel,
                    "mensagem": mensagem_disponivel
                },
                "promocoes": {
                    "ativo": promocoes_ativo,
                    "frequencia": frequencia_promocoes,
                    "mensagem": mensagem_promocao
                }
            }
            
            st.success("Configurações de automação salvas com sucesso!")
        st.markdown('</div>', unsafe_allow_html=True)

# Navegação numérica
def exibir_menu_navegacao():
    st.sidebar.markdown('<h3>Menu de Navegação</h3>', unsafe_allow_html=True)
    
    opcoes_menu = [
        {"numero": 1, "nome": "Dashboard", "funcao": mostrar_dashboard},
        {"numero": 2, "nome": "Clientes", "funcao": gerenciar_clientes},
        {"numero": 3, "nome": "Produtos", "funcao": gerenciar_produtos},
        {"numero": 4, "nome": "Pedidos", "funcao": gerenciar_pedidos},
        {"numero": 5, "nome": "Tarefas", "funcao": gerenciar_tarefas},
        {"numero": 6, "nome": "Fornecedores", "funcao": gerenciar_fornecedores},
        {"numero": 7, "nome": "Financeiro", "funcao": gerenciar_financeiro},
        {"numero": 8, "nome": "Notificações", "funcao": gerenciar_notificacoes}
    ]
    
    # Exibir opções de menu com números
    for opcao in opcoes_menu:
        st.sidebar.markdown(
            f"""<div class="menu-option" onclick="this.style.backgroundColor='#FFD1E6'">
                <span class="menu-number">{opcao['numero']}</span> {opcao['nome']}
            </div>""", 
            unsafe_allow_html=True
        )
    
    # Campo para navegação por número
    st.sidebar.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
    numero_pagina = st.sidebar.number_input("Digite o número da página:", min_value=1, max_value=8, value=1)
    
    # Mapear número para página
    pagina_selecionada = opcoes_menu[numero_pagina-1]["nome"]
    
    # Atualizar página atual
    if pagina_selecionada != st.session_state.pagina_atual:
        st.session_state.pagina_atual = pagina_selecionada
        st.rerun()
    
    # Exibir página atual
    st.sidebar.markdown(f"<p>Página atual: <strong>{st.session_state.pagina_atual}</strong></p>", unsafe_allow_html=True)
    
    return pagina_selecionada

# Função principal
def main():
    st.markdown('<h1 class="main-header">Nosso Closet RN - Sistema de Gestão</h1>', unsafe_allow_html=True)
    
    # Exibir menu de navegação e obter página selecionada
    pagina_selecionada = exibir_menu_navegacao()
    
    # Exibir conteúdo da página
    if pagina_selecionada == "Dashboard":
        mostrar_dashboard()
    elif pagina_selecionada == "Clientes":
        gerenciar_clientes()
    elif pagina_selecionada == "Produtos":
        gerenciar_produtos()
    elif pagina_selecionada == "Pedidos":
        gerenciar_pedidos()
    elif pagina_selecionada == "Tarefas":
        gerenciar_tarefas()
    elif pagina_selecionada == "Fornecedores":
        gerenciar_fornecedores()
    elif pagina_selecionada == "Financeiro":
        gerenciar_financeiro()
    elif pagina_selecionada == "Notificações":
        gerenciar_notificacoes()

# Executar o aplicativo
if __name__ == "__main__":
    main()
