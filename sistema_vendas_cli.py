import os
import sys
from typing import Optional
import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'sistema_vendas'
}

class SistemaVendasCLI:
    def __init__(self):
        self.conexao = None
        print("Sistema de Vendas - CLI Inicializado")
        print("=" * 50)
    
    def conectar_banco(self):
        try:
            self.conexao = psycopg2.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            
            print("Conectando ao banco PostgreSQL...")
            #self.conexao = psycopg2.connect(**pg_config)
            self.conexao.autocommit = True
            print("Conexão estabelecida com sucesso!")
            return True
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False
        return True
    
    def desconectar_banco(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados encerrada.")
                        
    def executar_consulta(self, sql: str, descricao: str) -> None:
        """
        Executa uma consulta SQL e exibe os resultados formatados
        
        Args:
            sql (str): Comando SQL a ser executado
            descricao (str): Descrição da consulta para exibição
        """
        if not self.conexao:
            print("Erro: Não há conexão com o banco de dados.")
            return
            
        try:
            print(f"\n{descricao}")
            print("=" * len(descricao))
            
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            
            # Busca todos os resultados
            resultados = cursor.fetchall()
            
            if not resultados:
                print("Nenhum resultado encontrado.")
            else:
                # Obtém os nomes das colunas
                colunas = [desc[0] for desc in cursor.description]
                
                # Calcula a largura máxima para cada coluna
                larguras = []
                for i, coluna in enumerate(colunas):
                    largura_coluna = len(str(coluna))
                    for linha in resultados:
                        valor = str(linha[i]) if linha[i] is not None else "NULL"
                        largura_coluna = max(largura_coluna, len(valor))
                    larguras.append(largura_coluna + 2)  # +2 para espaçamento
                
                # Imprime cabeçalho
                linha_cabecalho = ""
                for i, coluna in enumerate(colunas):
                    linha_cabecalho += str(coluna).ljust(larguras[i])
                print(linha_cabecalho)
                print("-" * len(linha_cabecalho))
                
                # Imprime resultados
                for linha in resultados:
                    linha_formatada = ""
                    for i, valor in enumerate(linha):
                        valor_str = str(valor) if valor is not None else "NULL"
                        linha_formatada += valor_str.ljust(larguras[i])
                    print(linha_formatada)
                
                print(f"\nTotal de registros: {len(resultados)}")
            
            cursor.close()
            
        except psycopg2.Error as e:
            print(f"Erro ao executar consulta SQL: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    # ========================================
    # FUNCOES COM CONSULTAS SQL
    # ========================================
    
    def consulta_01_usuarios_ativos(self):
        """1. Listagem de Usuários Ativos"""
        sql = """
        SELECT id_usuario, nome, email, telefone FROM usuario 
        WHERE ativo = TRUE;
        """
        self.executar_consulta(sql, "1. Listagem de Usuários Ativos")
    
    def consulta_02_produtos_categoria(self):
        
        sql = """
        SELECT nome, preco, quantidade_estoque FROM produto
        WHERE categoria = 'Informática'
        ORDER BY preco ASC;
        """
        self.executar_consulta(sql, "2. Catálogo de Produtos por Categoria")
    
    def consulta_03_pedidos_status(self):
        
        sql = """
        SELECT status_pedido, COUNT(*) AS total_pedidos FROM pedido
        GROUP BY status_pedido 
        ORDER BY status_pedido;
        """
        self.executar_consulta(sql, "3. Contagem de Pedidos por Status")
    
    def consulta_04_estoque_baixo(self):
        
        sql = """
        SELECT nome, quantidade_estoque, categoria FROM produto
        WHERE quantidade_estoque < 30
        ORDER BY quantidade_estoque ASC;
        """
        self.executar_consulta(sql, "4. Alerta de Estoque Baixo")
    
    def consulta_05_pedidos_recentes(self):
        
        sql = """
        SELECT id_pedido, data_pedido, valor_total, status_pedido FROM pedido
        WHERE data_pedido >= CURRENT_DATE - INTERVAL '60 days'
        ORDER BY data_pedido DESC;
        """
        self.executar_consulta(sql, "5. Histórico de Pedidos Recentes")
    
    def consulta_06_produtos_caros_categoria(self):
        
        sql = """
        SELECT p.categoria, p.nome, p.preco
        FROM produto p
        JOIN (
            SELECT categoria, MAX(preco) AS maior_preco
            FROM produto
            GROUP BY categoria
        ) sub
        ON p.categoria = sub.categoria
        AND p.preco = sub.maior_preco;
        """
        self.executar_consulta(sql, "6. Produtos Mais Caros por Categoria")
    
    def consulta_07_contatos_incompletos(self):
        
        sql = """
        SELECT * FROM usuario
        WHERE ativo = TRUE AND (telefone IS NULL OR telefone = '');
        """
        self.executar_consulta(sql, "7. Clientes com Dados Incompletos")
    
    def consulta_08_pedidos_enviados(self):
        
        sql = """
        SELECT p.id_pedido, p.data_pedido, p.status_pedido, u.id_usuario, u.nome 
        AS cliente, u.email, u.telefone, p.endereco_entrega
        FROM pedido p
        JOIN usuario u ON p.id_usuario = u.id_usuario
        WHERE p.status_pedido = 'enviado'
        ORDER BY p.data_pedido DESC;
        """
        self.executar_consulta(sql, "8. Pedidos Pendentes de Entrega")
    
    def consulta_09_detalhamento_pedido(self):
        
        sql = """
        SELECT 
            p.id_pedido,
            p.data_pedido,
            p.status_pedido,
            p.endereco_entrega,
            u.id_usuario,
            u.nome AS cliente,
            u.email,
            u.telefone,
            pr.nome AS produto,
            ip.quantidade,
            ip.preco_unitario,
            ip.subtotal
        FROM 
            pedido p
        JOIN 
            usuario u ON p.id_usuario = u.id_usuario
        JOIN 
            itens_pedido ip ON p.id_pedido = ip.id_pedido
        JOIN 
            produto pr ON ip.id_produto = pr.id_produto
        WHERE 
            p.id_pedido = 1
        ORDER BY 
            pr.nome;
        """
        self.executar_consulta(sql, "9. Detalhamento Completo de Pedidos")
    
    def consulta_10_ranking_produtos(self):
    
        sql = """
        SELECT 
            pr.nome,
            pr.categoria,
            COALESCE(SUM(ip.quantidade), 0) AS total_vendido
        FROM 
            produto pr
        LEFT JOIN 
            itens_pedido ip ON pr.id_produto = ip.id_produto
        GROUP BY 
            pr.id_produto, pr.nome, pr.categoria
        ORDER BY 
            total_vendido DESC;
        """
        self.executar_consulta(sql, "10. Ranking dos Produtos Mais Vendidos")
    
    def consulta_11_clientes_sem_compras(self):
        
        sql = """
        SELECT 
            u.id_usuario,
            u.nome,
            u.email,
            u.telefone
        FROM 
            usuario u
        LEFT JOIN 
            pedido p ON u.id_usuario = p.id_usuario
        WHERE 
            u.ativo = TRUE
            AND p.id_pedido IS NULL;
        """
        self.executar_consulta(sql, "11. Análise de Clientes Sem Compras")
    
    def consulta_12_estatisticas_cliente(self):
        
        sql = """
        SELECT
            u.id_usuario,
            u.nome AS cliente,
            COUNT(p.id_pedido) AS total_pedidos,
            ROUND(AVG(p.valor_total), 2) AS valor_medio_por_pedido,
            ROUND(SUM(p.valor_total), 2) AS valor_total_gasto
        FROM
            usuario u
        JOIN
            pedido p ON u.id_usuario = p.id_usuario
        GROUP BY
            u.id_usuario, u.nome
        ORDER BY
            valor_total_gasto DESC;
        """
        self.executar_consulta(sql, "12. Estatísticas de Compras por Cliente")
    
    def consulta_13_relatorio_mensal(self):
        
        sql = """
        SELECT 
            TO_CHAR(DATE_TRUNC('month', p.data_pedido), 'MM/YYYY') AS periodo,
            COUNT(DISTINCT p.id_pedido) AS total_pedidos,
            COUNT(DISTINCT ip.id_produto) AS produtos_diferentes,
            ROUND(SUM(ip.subtotal), 2) AS faturamento_total
        FROM 
            pedido p
        JOIN 
            itens_pedido ip ON p.id_pedido = ip.id_pedido
        GROUP BY 
            DATE_TRUNC('month', p.data_pedido)
        ORDER BY 
            DATE_TRUNC('month', p.data_pedido);
        """
        self.executar_consulta(sql, "13. Relatório Mensal de Vendas")
    
    def consulta_14_produtos_nao_vendidos(self):
        
        sql = """
        SELECT 
            p.id_produto,
            p.nome,
            p.categoria,
            p.preco,
            p.quantidade_estoque
        FROM 
            produto p
        LEFT JOIN 
            itens_pedido ip ON p.id_produto = ip.id_produto
        WHERE 
            p.ativo = TRUE
            AND ip.id_item IS NULL
        ORDER BY 
            p.nome;
        """
        self.executar_consulta(sql, "14. Produtos que Nunca Foram Vendidos")
    
    def consulta_15_ticket_medio_categoria(self):
        
        sql = """
        SELECT 
            pr.categoria,
            ROUND(SUM(ip.subtotal) / COUNT(DISTINCT p.id_pedido), 2) AS ticket_medio
        FROM 
            pedido p
        JOIN 
            itens_pedido ip ON p.id_pedido = ip.id_pedido
        JOIN 
            produto pr ON ip.id_produto = pr.id_produto
        WHERE 
            p.status_pedido <> 'cancelado'
        GROUP BY 
            pr.categoria
        ORDER BY 
            ticket_medio DESC;
        """
        self.executar_consulta(sql, "15. Análise de Ticket Médio por Categoria")
    
    # ========================================
    # MENUS 
    # ======================================== 
    def menu_exercicios(self):
        """MENU"""
        while True:            
            print("=" * 40)
            print("1. Listagem de Usuários Ativos")
            print("2. Catálogo de Produtos por Categoria")
            print("3. Contagem de Pedidos por Status")
            print("4. Alerta de Estoque Baixo")
            print("5. Histórico de Pedidos Recentes")
            print("6. Produtos Mais Caros por Categoria")
            print("7. Clientes com Dados Incompletos")
            print("8. Pedidos Pendentes de Entrega")
            print("9. Detalhamento Completo de Pedidos")
            print("10. Ranking dos Produtos Mais Vendidos")
            print("11. Análise de Clientes Sem Compras")
            print("12. Estatísticas de Compras por Cliente")
            print("13. Relatório Mensal de Vendas")
            print("14. Produtos que Nunca Foram Vendidos")
            print("15. Análise de Ticket Médio por Categoria")            
            print("0. Voltar ao Menu Principal")
            print("=" * 40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.consulta_01_usuarios_ativos()
            elif opcao == "2":
                self.consulta_02_produtos_categoria()
            elif opcao == "3":
                self.consulta_03_pedidos_status()
            elif opcao == "4":
                self.consulta_04_estoque_baixo()
            elif opcao == "5":
                self.consulta_05_pedidos_recentes()
            elif opcao == "6":
                self.consulta_06_produtos_caros_categoria()
            elif opcao == "7":
                self.consulta_07_contatos_incompletos()
            elif opcao == "8":
                self.consulta_08_pedidos_enviados()
            elif opcao == "9":
                self.consulta_09_detalhamento_pedido()
            elif opcao == "10":
                self.consulta_10_ranking_produtos()
            elif opcao == "11":
                self.consulta_11_clientes_sem_compras()
            elif opcao == "12":
                self.consulta_12_estatisticas_cliente()
            elif opcao == "13":
                self.consulta_13_relatorio_mensal()
            elif opcao == "14":
                self.consulta_14_produtos_nao_vendidos()
            elif opcao == "15":
                self.consulta_15_ticket_medio_categoria()                
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
            
            input("\nPressione ENTER para continuar...")

def main():
    cli = SistemaVendasCLI()
    if cli.conectar_banco():
        try:
            cli.menu_exercicios()
        finally:
            cli.desconectar_banco()
    else:
        print("Falha ao conectar ao banco de dados.")
        sys.exit(1)

if __name__ == "__main__":
    main()