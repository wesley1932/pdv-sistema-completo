from datetime import datetime

class InventoryManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_product(self, name, description, price, quantity, min_stock, category, barcode=None):
        try:
            self.db.execute_query(
                '''INSERT INTO products (name, description, price, quantity, min_stock, category, barcode) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (name, description, price, quantity, min_stock, category, barcode)
            )
            return True
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            return False
    
    def get_all_products(self):
        return self.db.fetch_all("SELECT * FROM products ORDER BY name")
    
    def get_product_by_id(self, product_id):
        return self.db.fetch_one("SELECT * FROM products WHERE id = ?", (product_id,))
    
    def get_product_by_barcode(self, barcode):
        return self.db.fetch_one("SELECT * FROM products WHERE barcode = ?", (barcode,))
    
    def update_product(self, product_id, name, description, price, quantity, min_stock, category, barcode=None):
        self.db.execute_query(
            '''UPDATE products SET name = ?, description = ?, price = ?, quantity = ?, 
               min_stock = ?, category = ?, barcode = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?''',
            (name, description, price, quantity, min_stock, category, barcode, product_id)
        )
    
    def update_stock(self, product_id, new_quantity):
        self.db.execute_query(
            "UPDATE products SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (new_quantity, product_id)
        )
    
    def reduce_stock(self, product_id, quantity):
        product = self.get_product_by_id(product_id)
        if product and product['quantity'] >= quantity:
            new_quantity = product['quantity'] - quantity
            self.update_stock(product_id, new_quantity)
            return True
        return False
    
    def get_low_stock_products(self):
        return self.db.fetch_all(
            "SELECT * FROM products WHERE quantity <= min_stock ORDER BY quantity ASC"
        )
    
    def search_products(self, search_term):
        return self.db.fetch_all(
            "SELECT * FROM products WHERE name LIKE ? OR description LIKE ? OR barcode LIKE ?",
            (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
        )
    
    def delete_product(self, product_id):
        self.db.execute_query("DELETE FROM products WHERE id = ?", (product_id,))
    
    def get_categories(self):
        categories = self.db.fetch_all("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")
        return [cat['category'] for cat in categories if cat['category']]
    
    def get_products_by_category(self, category):
        return self.db.fetch_all("SELECT * FROM products WHERE category = ?", (category,))