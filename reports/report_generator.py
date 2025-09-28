from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime, timedelta
import os

class ReportGenerator:
    def __init__(self, db_manager):
        self.db = db_manager
        self.styles = getSampleStyleSheet()
        
        # Criar estilo customizado
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Centro
        )
    
    def generate_sales_report(self, start_date=None, end_date=None):
        """Gerar relatório de vendas"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
        
        # Buscar dados de vendas
        sales_data = self.db.fetch_all(
            """SELECT s.id, s.total_amount, s.payment_method, s.customer_name, 
                      s.sale_date, u.full_name as seller
               FROM sales s 
               LEFT JOIN users u ON s.user_id = u.id 
               WHERE DATE(s.sale_date) BETWEEN DATE(?) AND DATE(?)
               ORDER BY s.sale_date DESC""",
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        )
        
        # Criar PDF
        filename = f"relatorio_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Título
        title = Paragraph("RELATÓRIO DE VENDAS", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Período
        period = Paragraph(f"<b>Período:</b> {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}", self.styles['Normal'])
        elements.append(period)
        elements.append(Spacer(1, 12))
        
        if sales_data:
            # Dados da tabela
            table_data = [['ID', 'Data', 'Cliente', 'Vendedor', 'Método Pag.', 'Total']]
            total_vendas = 0
            
            for sale in sales_data:
                table_data.append([
                    str(sale['id']),
                    datetime.strptime(sale['sale_date'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y'),
                    sale['customer_name'] or 'N/A',
                    sale['seller'] or 'N/A',
                    sale['payment_method'] or 'N/A',
                    f"R$ {sale['total_amount']:.2f}"
                ])
                total_vendas += sale['total_amount']
            
            # Criar tabela
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 12))
            
            # Total
            total_text = Paragraph(f"<b>Total de Vendas: R$ {total_vendas:.2f}</b>", self.styles['Heading2'])
            elements.append(total_text)
        else:
            elements.append(Paragraph("Nenhuma venda encontrada no período.", self.styles['Normal']))
        
        doc.build(elements)
        return filename
    
    def generate_inventory_report(self):
        """Gerar relatório de estoque"""
        products = self.db.fetch_all("SELECT * FROM products ORDER BY name")
        
        filename = f"relatorio_estoque_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Título
        title = Paragraph("RELATÓRIO DE ESTOQUE", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        if products:
            # Dados da tabela
            table_data = [['Produto', 'Categoria', 'Estoque', 'Estoque Min.', 'Preço', 'Status']]
            
            for product in products:
                status = "⚠️ BAIXO" if product['quantity'] <= product['min_stock'] else "✅ OK"
                table_data.append([
                    product['name'],
                    product['category'] or 'N/A',
                    str(product['quantity']),
                    str(product['min_stock']),
                    f"R$ {product['price']:.2f}",
                    status
                ])
            
            # Criar tabela
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("Nenhum produto cadastrado.", self.styles['Normal']))
        
        doc.build(elements)
        return filename