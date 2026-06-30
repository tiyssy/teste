-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    data_nascimento DATE,
    endereco VARCHAR(500),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_data_criacao ON usuarios(data_criacao);

-- Criar tabela de log de atividades
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    acao VARCHAR(100) NOT NULL,
    descricao TEXT,
    data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados de exemplo
INSERT INTO usuarios (nome, email, telefone, data_nascimento, endereco, cidade, estado, cep)
VALUES 
    ('João Silva', 'joao@example.com', '(11) 98765-4321', '1990-05-15', 'Rua A, 123', 'São Paulo', 'SP', '01310-100'),
    ('Maria Santos', 'maria@example.com', '(21) 99876-5432', '1992-08-20', 'Avenida B, 456', 'Rio de Janeiro', 'RJ', '20040020'),
    ('Pedro Oliveira', 'pedro@example.com', '(31) 97654-3210', '1988-03-10', 'Rua C, 789', 'Belo Horizonte', 'MG', '30140071')
ON CONFLICT DO NOTHING;
