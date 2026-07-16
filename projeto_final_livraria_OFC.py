import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk

ARQUIVO_DADOS = "livros.json"

#dados
def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {"livros": [], "emprestimos": []}
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            conteudo = json.load(f)
            # Garante compatibilidade caso o arquivo antigo só tivesse a lista de livros
            if isinstance(conteudo, list):
                return {"livros": conteudo, "emprestimos": []}
            if "livros" not in conteudo: conteudo["livros"] = []
            if "emprestimos" not in conteudo: conteudo["emprestimos"] = []
            return conteudo
    except Exception:
        return {"livros": [], "emprestimos": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

#logica da aba 1 : de listagem de livros
def atualizar_tabela_livros():
    for linha in tabela_livros.get_children():
        tabela_livros.delete(linha)
    for livro in dados["livros"]:
        tabela_livros.insert("", "end", values=(livro["id"], livro["titulo"], livro["autor"], livro["quantidade"]))

def preencher_campos_livros(event):
    item_selecionado = tabela_livros.selection()
    if item_selecionado:
        valores = tabela_livros.item(item_selecionado, "values")
        txt_titulo.delete(0, tk.END)
        txt_titulo.insert(0, valores[1])
        txt_autor.delete(0, tk.END)
        txt_autor.insert(0, valores[2])
        txt_quantidade.delete(0, tk.END)
        txt_quantidade.insert(0, valores[3])

def adicionar_livro():
    titulo = txt_titulo.get().strip()
    autor = txt_autor.get().strip()
    qtd_str = txt_quantidade.get().strip()
    
    if not titulo or not autor or not qtd_str:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
        return
    try:
        quantidade = int(qtd_str)
        if quantidade < 0: raise ValueError
    except ValueError:
        messagebox.showerror("Erro de Digitação", "A quantidade deve ser um número inteiro positivo!")
        return
    
    id_livro = max([l['id'] for l in dados["livros"]], default=0) + 1
    novo_livro = {"id": id_livro, "titulo": titulo, "autor": autor, "quantidade": quantidade}
    dados["livros"].append(novo_livro)
    salvar_dados(dados)
    atualizar_tabela_livros()
    
    txt_titulo.delete(0, tk.END)
    txt_autor.delete(0, tk.END)
    txt_quantidade.delete(0, tk.END)
    
    if quantidade == 0:
        messagebox.showwarning("Alerta de Estoque", f"O livro '{titulo}' foi adicionado com estoque ZERADO!")
    else:
        messagebox.showinfo("Sucesso", f"'{titulo}' adicionado!")

def atualizar_livro():
    item_selecionado = tabela_livros.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um livro para editar.")
        return
    valores = tabela_livros.item(item_selecionado, "values")
    id_busca = int(valores[0])
    
    titulo = txt_titulo.get().strip()
    autor = txt_autor.get().strip()
    qtd_str = txt_quantidade.get().strip()
    
    if not titulo or not autor or not qtd_str:
        messagebox.showwarning("Aviso", "Os campos não podem ficar vazios!")
        return
    try:
        quantidade = int(qtd_str)
        if quantidade < 0: raise ValueError
    except ValueError:
        messagebox.showerror("Erro de Digitação", "Quantidade inválida!")
        return
        
    for livro in dados["livros"]:
        if livro["id"] == id_busca:
            livro["titulo"] = titulo
            livro["autor"] = autor
            livro["quantidade"] = quantidade
            salvar_dados(dados)
            atualizar_tabela_livros()
            
            txt_titulo.delete(0, tk.END)
            txt_autor.delete(0, tk.END)
            txt_quantidade.delete(0, tk.END)
            
            if quantidade == 0:
                messagebox.showwarning("Alerta de Estoque", f"Estoque de '{titulo}' zerado!")
            else:
                messagebox.showinfo("Sucesso", "Livro atualizado!")
            return

def deletar_livro():
    item_selecionado = tabela_livros.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um livro para excluir.")
        return
    valores = tabela_livros.item(item_selecionado, "values")
    id_busca = int(valores[0])
    
    for livro in dados["livros"]:
        if livro["id"] == id_busca:
            dados["livros"].remove(livro)
            salvar_dados(dados)
            atualizar_tabela_livros()
            return

#logica da aba 2 : emprestimos de livro
def atualizar_tabela_emprestimos():
    for linha in tabela_emp.get_children():
        tabela_emp.delete(linha)
    
    hoje = datetime.now().date()
    
    for emp in dados["emprestimos"]:
        data_emp = datetime.strptime(emp["data_emprestimo"], "%Y-%m-%d").date()
        prazo_final = data_emp + timedelta(days=7)
        dias_restantes = (prazo_final - hoje).days
        
        if dias_restantes < 0:
            status_prazo = "EXPIRADO"
        else:
            status_prazo = f"{dias_restantes} dias"
            
        tabela_emp.insert("", "end", values=(emp["id"], emp["titulo_livro"], emp["nome_pessoa"], emp["cpf"], emp["data_emprestimo"], status_prazo))

def realizar_emprestimo():
    item_selecionado = tabela_livros.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Vá na aba 'Livros' e selecione o livro que deseja emprestar!")
        return
    
    valores_livro = tabela_livros.item(item_selecionado, "values")
    id_livro = int(valores_livro[0])
    titulo_livro = valores_livro[1]
    qtd_livro = int(valores_livro[3])
    
    nome = txt_nome_emp.get().strip()
    cpf = txt_cpf_emp.get().strip()
    
    if not nome or not cpf:
        messagebox.showwarning("Aviso", "Preencha o Nome e o CPF de quem está pegando o livro!")
        return
        
    if qtd_livro <= 0:
        messagebox.showerror("Erro", "Não é possível emprestar! Este livro está com estoque zerado.")
        return

    #subtrair 1 do estoque do livro
    for livro in dados["livros"]:
        if livro["id"] == id_livro:
            livro["quantidade"] -= 1
            break
            
    id_emp = max([e['id'] for e in dados["emprestimos"]], default=0) + 1
    data_atual = datetime.now().strftime("%Y-%m-%d")
    
    novo_emprestimo = {
        "id": id_emp,
        "id_livro": id_livro,
        "titulo_livro": titulo_livro,
        "nome_pessoa": nome,
        "cpf": cpf,
        "data_emprestimo": data_atual
    }
    
    dados["emprestimos"].append(novo_emprestimo)
    salvar_dados(dados)
    
    atualizar_tabela_livros()
    atualizar_tabela_emprestimos()
    
    txt_nome_emp.delete(0, tk.END)
    txt_cpf_emp.delete(0, tk.END)
    messagebox.showinfo("Sucesso", f"Empréstimo registrado! Prazo de devolução: 7 dias.")

def devolver_livro_emp():
    item_selecionado = tabela_emp.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione um registro na tabela de empréstimos para devolver.")
        return
        
    valores_emp = tabela_emp.item(item_selecionado, "values")
    id_emp = int(valores_emp[0])
    
    for emp in dados["emprestimos"]:
        if emp["id"] == id_emp:
            # Devolve +1 para o estoque do livro original
            for livro in dados["livros"]:
                if livro["id"] == emp["id_livro"]:
                    livro["quantidade"] += 1
                    break
            dados["emprestimos"].remove(emp)
            break
            
    salvar_dados(dados)
    atualizar_tabela_livros()
    atualizar_tabela_emprestimos()
    messagebox.showinfo("Sucesso", "Livro devolvido e estoque atualizado!")

#parte visual
dados = carregar_dados()

janela = tk.Tk()
janela.title("Papiro - Gerenciamento de Livraria") 
janela.geometry("720x620")
janela.configure(bg="#f4f6f9")
janela.resizable(False, False)

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"), background="#2c3e50", foreground="white")
estilo.configure("Treeview", font=("Comic Sans MS", 10), rowheight=25)
estilo.map("Treeview", background=[("selected", "#3498db")])

#criação do sistema de Abas (Tabs)
abas_controle = ttk.Notebook(janela)
aba_livros = tk.Frame(abas_controle, bg="#f4f6f9")
aba_emprestimos = tk.Frame(abas_controle, bg="#f4f6f9")
abas_controle.add(aba_livros, text=" 📚 Cadastro de Livros ")
abas_controle.add(aba_emprestimos, text=" 🤝 Empréstimos ")
abas_controle.pack(expand=1, fill="both")

#aba do gerenciamento de livros
frame_inputs = tk.Frame(aba_livros, bg="#f4f6f9")
frame_inputs.pack(pady=20)

tk.Label(frame_inputs, text="Título do Livro:", font=("Comic Sans MS", 10, "bold"), bg="#f4f6f9", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=6, sticky="e")
txt_titulo = tk.Entry(frame_inputs, width=35, font=("Comic Sans MS", 11), relief="solid", bd=1)
txt_titulo.grid(row=0, column=1, padx=10, pady=6)

tk.Label(frame_inputs, text="Autor / Escritor:", font=("Comic Sans MS", 10, "bold"), bg="#f4f6f9", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=6, sticky="e")
txt_autor = tk.Entry(frame_inputs, width=35, font=("Comic Sans MS", 11), relief="solid", bd=1)
txt_autor.grid(row=1, column=1, padx=10, pady=6)

tk.Label(frame_inputs, text="Qtd. em Estoque:", font=("Comic Sans MS", 10, "bold"), bg="#f4f6f9", fg="#2c3e50").grid(row=2, column=0, padx=10, pady=6, sticky="e")
txt_quantidade = tk.Entry(frame_inputs, width=35, font=("Comic Sans MS", 11), relief="solid", bd=1)
txt_quantidade.grid(row=2, column=1, padx=10, pady=6)

frame_botoes = tk.Frame(aba_livros, bg="#f4f6f9")
frame_botoes.pack(pady=5)

btn_adicionar = tk.Button(frame_botoes, text="➕ Adicionar", bg="#2ecc71", fg="white", font=("Comic Sans MS", 10, "bold"), relief="flat", padx=12, pady=6, command=adicionar_livro)
btn_adicionar.grid(row=0, column=0, padx=8)

btn_atualizar = tk.Button(frame_botoes, text="✏️ Atualizar Livro", bg="#3498db", fg="white", font=("Comic Sans MS", 10, "bold"), relief="flat", padx=12, pady=6, command=atualizar_livro)
btn_atualizar.grid(row=0, column=1, padx=8)

btn_deletar = tk.Button(frame_botoes, text="❌ Excluir", bg="#e74c3c", fg="white", font=("Comic Sans MS", 10, "bold"), relief="flat", padx=12, pady=6, command=deletar_livro)
btn_deletar.grid(row=0, column=2, padx=8)

colunas_l = ("ID", "Título", "Autor", "Quantidade")
tabela_livros = ttk.Treeview(aba_livros, columns=colunas_l, show="headings", height=10)
tabela_livros.heading("ID", text="ID")
tabela_livros.heading("Título", text="Título")
tabela_livros.heading("Autor", text="Autor")
tabela_livros.heading("Quantidade", text="Qtd. Estoque")
tabela_livros.column("ID", width=50, anchor="center")
tabela_livros.column("Título", width=250)
tabela_livros.column("Autor", width=220)
tabela_livros.column("Quantidade", width=100, anchor="center")
tabela_livros.pack(pady=15, padx=25)
tabela_livros.bind("<<TreeviewSelect>>", preencher_campos_livros)

#aba de emprestimos
frame_inputs_emp = tk.Frame(aba_emprestimos, bg="#f4f6f9")
frame_inputs_emp.pack(pady=20)

tk.Label(frame_inputs_emp, text="Nome do Cliente:", font=("Comic Sans MS", 10, "bold"), bg="#f4f6f9", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=6, sticky="e")
txt_nome_emp = tk.Entry(frame_inputs_emp, width=35, font=("Comic Sans MS", 11), relief="solid", bd=1)
txt_nome_emp.grid(row=0, column=1, padx=10, pady=6)

tk.Label(frame_inputs_emp, text="CPF do Cliente:", font=("Comic Sans MS", 10, "bold"), bg="#f4f6f9", fg="#2c3e50").grid(row=1, column=0, padx=10, pady=6, sticky="e")
txt_cpf_emp = tk.Entry(frame_inputs_emp, width=35, font=("Comic Sans MS", 11), relief="solid", bd=1)
txt_cpf_emp.grid(row=1, column=1, padx=10, pady=6)

frame_botoes_emp = tk.Frame(aba_emprestimos, bg="#f4f6f9")
frame_botoes_emp.pack(pady=5)

btn_emprestar = tk.Button(frame_botoes_emp, text="🤝 Conceder Empréstimo", bg="#9b59b6", fg="white", font=("Comic Sans MS", 10, "bold"), relief="flat", padx=15, pady=6, command=realizar_emprestimo)
btn_emprestar.grid(row=0, column=0, padx=10)

btn_devolver = tk.Button(frame_botoes_emp, text="🔄 Registrar Devolução", bg="#f39c12", fg="white", font=("Comic Sans MS", 10, "bold"), relief="flat", padx=15, pady=6, command=devolver_livro_emp)
btn_devolver.grid(row=0, column=1, padx=10)

colunas_e = ("ID", "Livro", "Cliente", "CPF", "Data Retirada", "Prazo")
tabela_emp = ttk.Treeview(aba_emprestimos, columns=colunas_e, show="headings", height=10)
tabela_emp.heading("ID", text="ID")
tabela_emp.heading("Livro", text="Livro")
tabela_emp.heading("Cliente", text="Cliente")
tabela_emp.heading("CPF", text="CPF")
tabela_emp.heading("Data Retirada", text="Data Retirada")
tabela_emp.heading("Prazo", text="Prazo")
tabela_emp.column("ID", width=40, anchor="center")
tabela_emp.column("Livro", width=180)
tabela_emp.column("Cliente", width=150)
tabela_emp.column("CPF", width=110, anchor="center")
tabela_emp.column("Data Retirada", width=100, anchor="center")
tabela_emp.column("Prazo", width=100, anchor="center")
tabela_emp.pack(pady=15, padx=20)

# Inicialização geral
atualizar_tabela_livros()
atualizar_tabela_emprestimos()
janela.mainloop()