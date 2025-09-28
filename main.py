#!/usr/bin/env python3
"""
Sistema PDV Completo
Ponto de Venda desenvolvido em Python

Desenvolvido por: Sistema PDV Team
Versão: 1.0.0
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Adicionar o diretório atual ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Função principal do sistema"""
    try:
        # Verificar se todas as dependências estão instaladas
        try:
            import sqlite3
            from tkinter import ttk
            from PIL import Image, ImageTk
            from reportlab.lib.pagesizes import letter
        except ImportError as e:
            missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
            messagebox.showerror(
                "Dependência Faltando", 
                f"Módulo não encontrado: {missing_module}\n\n" +
                "Por favor, instale as dependências:\n" +
                "pip install -r requirements.txt"
            )
            return
        
        # Importar e executar a aplicação principal
        from ui.main_ui import MainApplication
        
        # Criar e executar a aplicação
        app = MainApplication()
        app.run()
        
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar o sistema:\n{str(e)}")
        print(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()