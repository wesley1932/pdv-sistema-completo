import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, parent, auth_manager, success_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.success_callback = success_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal centralizado
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(expand=True)
        
        # Logo/Título
        title_label = ttk.Label(main_frame, text="🏪 SISTEMA PDV", 
                               font=('Arial', 24, 'bold'))
        title_label.pack(pady=30)
        
        subtitle_label = ttk.Label(main_frame, text="Ponto de Venda Completo", 
                                 font=('Arial', 12))
        subtitle_label.pack(pady=5)
        
        # Frame do formulário de login
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding=20)
        login_frame.pack(pady=30, padx=20, ipadx=20, ipady=20)
        
        # Campo usuário
        ttk.Label(login_frame, text="Usuário:", font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(login_frame, textvariable=self.username_var, 
                                       font=('Arial', 11), width=25)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Campo senha
        ttk.Label(login_frame, text="Senha:", font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(login_frame, textvariable=self.password_var, 
                                       show="*", font=('Arial', 11), width=25)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Botão login
        login_btn = ttk.Button(login_frame, text="Entrar", command=self.handle_login,
                              style='Accent.TButton')
        login_btn.grid(row=2, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Informações de login padrão
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(pady=20)
        
        ttk.Label(info_frame, text="Login Padrão:", font=('Arial', 10, 'bold')).pack()
        ttk.Label(info_frame, text="Usuário: admin", font=('Arial', 9)).pack()
        ttk.Label(info_frame, text="Senha: Esqs2018$", font=('Arial', 9)).pack()
        
        # Focar no campo usuário
        self.username_entry.focus()
        
        # Bind Enter key
        self.parent.bind('<Return>', lambda e: self.handle_login())
        
        # Preencher campos padrão para demonstração
        self.username_var.set("admin")
        self.password_var.set("Esqs2018$")
    
    def handle_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        if self.auth_manager.login(username, password):
            user = self.auth_manager.get_current_user()
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user['full_name']}!")
            self.success_callback()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            self.password_var.set("")
            self.password_entry.focus()