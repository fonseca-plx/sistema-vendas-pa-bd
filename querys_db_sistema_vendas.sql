-- Escreva uma consulta que exiba o ID, nome, email e telefone de todos os usuários que estão ativos no sistema.
SELECT id_usuario, nome, email, telefone FROM usuario 
WHERE ativo = TRUE;

-- Crie uma consulta que mostre todos os produtos da categoria 'Informática', exibindo nome, preço e quantidade em estoque. Ordene por preço crescente.
SELECT nome, preco, quantidade_estoque FROM produto
WHERE categoria = 'Informática'
ORDER BY preco ASC;

-- Desenvolva uma consulta que conte quantos pedidos existem para cada status diferente.
SELECT status_pedido, COUNT(*) AS total_pedidos FROM pedido
GROUP BY status_pedido 
ORDER BY status_pedido;

-- Faça uma consulta que identifique produtos com quantidade em estoque menor que 30 unidades. Mostre nome do produto, quantidade atual e categoria.
SELECT nome, quantidade_estoque, categoria FROM produto
WHERE quantidade_estoque < 30
ORDER BY quantidade_estoque ASC;

-- Escreva uma consulta que liste todos os pedidos realizados nos últimos 60 dias, mostrando ID do pedido, data, valor total e status.
SELECT id_pedido, data_pedido, valor_total, status_pedido FROM pedido
WHERE data_pedido >= CURRENT_DATE - INTERVAL '60 days'
ORDER BY data_pedido DESC;

-- Crie uma consulta que mostre o produto mais caro de cada categoria, exibindo categoria, nome do produto e preço.
SELECT 
    p.categoria,
    p.nome,
    p.preco
FROM 
    produto p
JOIN (
    SELECT categoria, MAX(preco) AS maior_preco
    FROM produto
    GROUP BY categoria
) sub
ON p.categoria = sub.categoria
AND p.preco = sub.maior_preco;

-- Desenvolva uma consulta para identificar usuários ativos que não possuem telefone cadastrado.
SELECT * FROM usuario
WHERE ativo = TRUE AND (telefone IS NULL OR telefone = '');

-- Faça uma consulta que liste todos os pedidos com status 'enviado', mostrando dados do cliente e endereço de entrega.
SELECT 
    p.id_pedido,
    p.data_pedido,
    p.status_pedido,
    u.id_usuario,
    u.nome AS cliente,
    u.email,
    u.telefone,
    p.endereco_entrega
FROM 
    pedido p
JOIN 
    usuario u ON p.id_usuario = u.id_usuario
WHERE 
    p.status_pedido = 'enviado'
ORDER BY 
    p.data_pedido DESC;

-- Crie uma consulta que mostre, para um pedido específico (ID = 1), todas as informações: dados do cliente, produtos comprados, quantidades, preços unitários e subtotais.
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

-- Desenvolva uma consulta que liste os produtos ordenados pela quantidade total vendida (soma de todas as vendas). Mostre nome, categoria e total vendido.
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

-- Escreva uma consulta que identifique todos os usuários ativos que nunca fizeram um pedido no sistema.
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

-- Crie uma consulta que calcule, para cada cliente que já fez pedidos: número total de pedidos, valor médio por pedido e valor total gasto.
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

-- Desenvolva uma consulta que agrupe as vendas por mês/ano, mostrando: período, quantidade de pedidos, número de produtos diferentes vendidos e faturamento total.


