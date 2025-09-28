import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.login_ui import LoginWindow
from ui.sales_ui import SalesWindow
from ui.inventory_ui import InventoryWindow
from ui.users_ui import UsersWindow
from ui.reports_ui import ReportsWindow
from ui.settings_ui import SettingsWindow
from database.database_manager import DatabaseManager
from auth.auth_manager import AuthManager
from config.config_manager import ConfigManager

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema PDV Completo")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Maximizar janela
        
        # Configurar ícone (se existir)
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
        
        # Inicializar managers
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager(self.db_manager)
        self.config_manager = ConfigManager()
        
        # Aplicar tema
        self.apply_theme()
        
        # Variável para controlar janelas abertas
        self.current_window = None
        
        # Mostrar tela de login
        self.show_login()
    
    def apply_theme(self):
        theme = self.config_manager.get_theme()
        style = ttk.Style()
        
        # Configurar cores do tema
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       foreground=theme['text_color'])
        
        style.configure('Menu.TButton',
                       font=('Arial', 12),
                       padding=10)
    
    def show_login(self):
        """Mostrar janela de login"""
        if self.current_window:
            self.current_window.destroy()
        
        # Limpar a janela principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Criar frame de login
        login_frame = ttk.Frame(self.root)
        login_frame.pack(expand=True, fill='both')
        
        self.current_window = LoginWindow(login_frame, self.auth_manager, self.show_main_menu)
    
    def show_main_menu(self):
        """Mostrar menu principal após login"""
        # Limpar a janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Criar frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        company_name = self.config_manager.get('company.name', 'Sistema PDV')
        title_label = ttk.Label(main_frame, text=company_name, style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Informações do usuário logado
        user = self.auth_manager.get_current_user()
        user_info = f"Usuário: {user['full_name']} ({user['role'].upper()})"
        user_label = ttk.Label(main_frame, text=user_info)
        user_label.pack(pady=5)
        
        # Frame para botões do menu
        menu_frame = ttk.Frame(main_frame)
        menu_frame.pack(expand=True, pady=20)
        
        # Configurar grid
        menu_frame.grid_columnconfigure(0, weight=1)
        menu_frame.grid_columnconfigure(1, weight=1)
        menu_frame.grid_columnconfigure(2, weight=1)
        
        # Botões do menu
        buttons = [
            ("💰 Vendas", self.show_sales, 0, 0),
            ("📦 Estoque", self.show_inventory, 0, 1),
            ("📊 Relatórios", self.show_reports, 0, 2),
            ("👥 Usuários", self.show_users, 1, 0),
            ("⚙️ Configurações", self.show_settings, 1, 1),
            ("🚺 Sair", self.logout, 1, 2)
        ]
        
        for text, command, row, col in buttons:
            # Verificar permissões
            if text == "👥 Usuários" and not self.auth_manager.is_admin():
                continue
            
            btn = ttk.Button(menu_frame, text=text, command=command, 
                           style='Menu.TButton', width=20)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        
        # Alertas de estoque baixo
        self.check_low_stock_alerts(main_frame)
        
        # Frame inferior com botões de ação rápida
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side='bottom', fill='x', pady=10)
        
        ttk.Button(bottom_frame, text="Backup Manual", 
                  command=self.manual_backup).pack(side='left', padx=5)
    
    def check_low_stock_alerts(self, parent):
        """Verificar e mostrar alertas de estoque baixo"""
        from inventory.inventory_manager import InventoryManager
        
        inventory_manager = InventoryManager(self.db_manager)
        low_stock = inventory_manager.get_low_stock_products()
        
        if low_stock and self.config_manager.get('system.low_stock_alert', True):
            alert_frame = ttk.LabelFrame(parent, text="⚠️ ALERTAS DE ESTOQUE", padding=10)
            alert_frame.pack(fill='x', padx=20, pady=10)
            
            alert_text = f"🚨 {len(low_stock)} produto(s) com estoque baixo!"
            ttk.Label(alert_frame, text=alert_text, foreground='red', 
                     font=('Arial', 10, 'bold')).pack()
            
            # Mostrar primeiros 3 produtos
            for i, product in enumerate(low_stock[:3]):
                product_text = f"• {product['name']}: {product['quantity']} unid. (mín: {product['min_stock']})"
                ttk.Label(alert_frame, text=product_text, foreground='orange').pack(anchor='w')
    
    def manual_backup(self):
        """Realizar backup manual"""
        try:
            backup_path = self.db_manager.backup_database()
            messagebox.showinfo("Backup", f"Backup realizado com sucesso!\nArquivo: {backup_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar backup: {str(e)}")
    
    def show_sales(self):
        """Mostrar janela de vendas"""
        self.open_window(SalesWindow, "Sistema PDV - Vendas")
    
    def show_inventory(self):
        """Mostrar janela de estoque"""
        self.open_window(InventoryWindow, "Sistema PDV - Estoque")
    
    def show_reports(self):
        """Mostrar janela de relatórios"""
        self.open_window(ReportsWindow, "Sistema PDV - Relatórios")
    
    def show_users(self):
        """Mostrar janela de usuários (apenas admin)"""
        if self.auth_manager.is_admin():
            self.open_window(UsersWindow, "Sistema PDV - Usuários")
        else:
            messagebox.showerror("Acesso Negado", "Apenas administradores podem acessar esta seção.")
    
    def show_settings(self):
        """Mostrar janela de configurações"""
        self.open_window(SettingsWindow, "Sistema PDV - Configurações")
    
    def open_window(self, window_class, title):
        """Abrir nova janela"""
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("1000x700")
        new_window.transient(self.root)
        new_window.grab_set()
        
        # Criar a janela específica
        window_class(new_window, self.db_manager, self.auth_manager, self.config_manager)
    
    def logout(self):
        """Fazer logout"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.auth_manager.logout()
            self.show_login()
    
    def run(self):
        """Executar aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Evento de fechamento da aplicação"""
        if messagebox.askyesno("Sair", "Deseja fechar o sistema?"):
            self.db_manager.close()
            self.root.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.run()