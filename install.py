#!/usr/bin/env python3
"""
Script de instalação para o Sistema PDV Completo
"""

import subprocess
import sys
import os

def install_requirements():
    """Instalar dependências necessárias"""
    
    print("🏪 Sistema PDV - Instalação")
    print("=" * 40)
    
    requirements = [
        'pillow>=9.0.0',
        'reportlab>=3.6.0'
    ]
    
    print("Instalando dependências...")
    
    for req in requirements:
        try:
            print(f"  Instalando {req}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
            print(f"  ✓ {req} instalado com sucesso")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Erro ao instalar {req}: {e}")
            return False
    
    print("\n✅ Todas as dependências foram instaladas!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python main.py")
    print("2. Faça login com:")
    print("   Usuário: admin")
    print("   Senha: Esqs2018$")
    print("3. (Opcional) Execute python add_sample_data.py para dados de exemplo")
    
    return True

if __name__ == "__main__":
    install_requirements()