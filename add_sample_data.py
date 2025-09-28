"""
Script para adicionar dados de exemplo ao sistema PDV
Execute após a primeira inicialização do sistema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_manager import DatabaseManager
from inventory.inventory_manager import InventoryManager

def add_sample_data():
    """Adicionar dados de exemplo"""
    
    # Conectar ao banco
    db = DatabaseManager()
    inventory = InventoryManager(db)
    
    # Produtos de exemplo
    sample_products = [
        {
            'name': 'Coca-Cola 350ml',
            'description': 'Refrigerante Coca-Cola lata 350ml',
            'price': 3.50,
            'quantity': 100,
            'min_stock': 20,
            'category': 'Bebidas',
            'barcode': '7894900011517'
        },
        {
            'name': 'Pão Frances',
            'description': 'Pão francês tradicional - unidade',
            'price': 0.75,
            'quantity': 50,
            'min_stock': 10,
            'category': 'Padaria',
            'barcode': None
        },
        {
            'name': 'Leite Integral 1L',
            'description': 'Leite integral UHT 1 litro',
            'price': 4.20,
            'quantity': 30,
            'min_stock': 15,
            'category': 'Laticínios',
            'barcode': '7891000100103'
        },
        {
            'name': 'Sabonete Dove',
            'description': 'Sabonete Dove hidratante 90g',
            'price': 2.80,
            'quantity': 25,
            'min_stock': 5,
            'category': 'Higiene',
            'barcode': '7891150047303'
        },
        {
            'name': 'Arroz Branco 5kg',
            'description': 'Arroz branco tipo 1 - 5kg',
            'price': 18.90,
            'quantity': 40,
            'min_stock': 10,
            'category': 'Grãos',
            'barcode': '7896273200013'
        }
    ]
    
    print("Adicionando produtos de exemplo...")
    
    for product in sample_products:
        try:
            inventory.add_product(
                product['name'],
                product['description'], 
                product['price'],
                product['quantity'],
                product['min_stock'],
                product['category'],
                product['barcode']
            )
            print(f"✓ {product['name']} adicionado")
        except Exception as e:
            print(f"✗ Erro ao adicionar {product['name']}: {e}")
    
    print("\nDados de exemplo adicionados com sucesso!")
    print("Execute o sistema com: python main.py")
    
    db.close()

if __name__ == "__main__":
    add_sample_data()