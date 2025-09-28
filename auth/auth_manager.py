import hashlib
import sqlite3
from datetime import datetime

class AuthManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.current_user = None
        self.create_default_admin()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_admin(self):
        # Verificar se admin já existe
        admin = self.db.fetch_one("SELECT * FROM users WHERE username = ?", ('admin',))
        if not admin:
            password_hash = self.hash_password('Esqs2018$')
            self.db.execute_query(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                ('admin', password_hash, 'Administrador', 'admin')
            )
    
    def login(self, username, password):
        password_hash = self.hash_password(password)
        user = self.db.fetch_one(
            "SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1",
            (username, password_hash)
        )
        
        if user:
            self.current_user = dict(user)
            return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def is_logged_in(self):
        return self.current_user is not None
    
    def is_admin(self):
        return self.current_user and self.current_user['role'] == 'admin'
    
    def get_current_user(self):
        return self.current_user
    
    def add_user(self, username, password, full_name, role='user'):
        try:
            password_hash = self.hash_password(password)
            self.db.execute_query(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                (username, password_hash, full_name, role)
            )
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_users(self):
        return self.db.fetch_all("SELECT id, username, full_name, role, created_at, is_active FROM users ORDER BY created_at DESC")
    
    def update_user(self, user_id, username, full_name, role):
        self.db.execute_query(
            "UPDATE users SET username = ?, full_name = ?, role = ? WHERE id = ?",
            (username, full_name, role, user_id)
        )
    
    def deactivate_user(self, user_id):
        self.db.execute_query("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
    
    def activate_user(self, user_id):
        self.db.execute_query("UPDATE users SET is_active = 1 WHERE id = ?", (user_id,))
    
    def change_password(self, user_id, new_password):
        password_hash = self.hash_password(new_password)
        self.db.execute_query(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, user_id)
        )