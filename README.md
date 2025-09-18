# Sistema de Vendas

Um sistema de consultas para análise de dados de vendas desenvolvido em Python com PostgreSQL, criado como projeto da disciplina de Programação para Administração de Banco de Dados (PA-BD).

## 📋 Objetivo do Projeto

Este projeto tem como objetivo demonstrar a integração entre Python e PostgreSQL para realizar consultas complexas em um sistema de vendas. O sistema permite executar diversas consultas pré-definidas para análise de dados de clientes, produtos, pedidos e vendas, oferecendo insights valiosos para a gestão do negócio.

## 🗄️ Estrutura do Banco de Dados

O sistema trabalha com as seguintes entidades principais:
- **Usuários**: Clientes do sistema com dados pessoais e status
- **Produtos**: Itens disponíveis para venda com categorias e estoque
- **Pedidos**: Transações realizadas pelos clientes
- **Itens do Pedido**: Detalhamento dos produtos em cada pedido

## 🔍 Funcionalidades

O sistema oferece 12 consultas diferentes para análise dos dados:

1. **Usuários Ativos** - Lista todos os usuários ativos do sistema
2. **Produtos por Categoria** - Filtra produtos da categoria 'Informática'
3. **Status dos Pedidos** - Conta pedidos por status
4. **Produtos com Estoque Baixo** - Identifica produtos com menos de 30 unidades
5. **Histórico de Pedidos** - Pedidos dos últimos 60 dias
6. **Produtos Mais Caros** - Produto mais caro por categoria
7. **Dados Incompletos** - Clientes sem telefone cadastrado
8. **Pedidos Enviados** - Pedidos pendentes de entrega
9. **Detalhamento de Pedidos** - Informações completas dos pedidos
10. **Produtos Mais Vendidos** - Ranking por quantidade vendida
11. **Clientes Inativos** - Usuários que nunca fizeram pedidos
12. **Estatísticas de Clientes** - Análise de gastos por cliente

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **PostgreSQL**
- **psycopg2** - Driver PostgreSQL para Python
- **Interface CLI** - Terminal interativo

## ⚙️ Configuração

### Pré-requisitos
- Python 3.x instalado
- PostgreSQL instalado e configurado
- Biblioteca psycopg2 (`pip install psycopg2-binary`)

### Configuração do Banco
1. Configure as credenciais do banco no arquivo `sistema_vendas_cli.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'sistema_vendas'
}
```

2. Execute as queries SQL do arquivo `querys_db_sistema_vendas.sql` para popular o banco com dados de teste.

## 🚀 Como Usar

1. Execute o sistema:
```bash
python sistema_vendas_cli.py
```

2. Use o menu interativo para navegar pelas consultas:
   - Digite o número da consulta desejada (1-12)
   - Digite `0` para sair do sistema

## 🎯 Objetivos Pedagógicos

Este projeto demonstra:
- Conexão Python-PostgreSQL
- Execução de consultas SQL complexas
- Manipulação de resultados de banco de dados
- Interface de linha de comando (CLI)
- Boas práticas de programação em Python
- Análise de dados com SQL

## 📝 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

---

**Desenvolvido para fins educacionais - TADS IFRN - Disciplina: Programação para Administração de Banco de Dados**