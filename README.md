# Remote Procedure Call


Com objetivo demonstrar a integração entre:

- Interface gráfica moderna com **Tkinter**
- Processamento matemático remoto
- Comunicação cliente–servidor (RPC)
- Integração com **IA para resolução de problemas matemáticos**
- Consumo e exibição de notícias
- Sistema de DNS customizado para resolução de serviços

A aplicação demonstra conceitos de sistemas distribuídos, separação de responsabilidades e comunicação entre sockets de forma prática.

<div align="center">
  <img href="">
</div>


### Arquitetura

O sistema segue um modelo **Cliente → RPC → Servidor**, com resolução DNS customizada, onde:

- O **cliente** é responsável pela interface gráfica
- O **servidor** executa as operações matemáticas e chamadas de IA
- A comunicação ocorre por meio de **Remote Procedure Calls**

```
┌──────────────┐         ┌──────────────┐         ┌─────────────────┐
│   Cliente    │   RPC   │ DNS Resolver │  Query  │    DNS Server   │
│  (Interface) │◄───────►│              │◄───────►│ (Authoritative) │
└──────┬───────┘         └──────────────┘         └─────────────────┘
       │                                                   │
       │ RPC Call                                         │
       ▼                                                   ▼
┌──────────────────┐                                  ┌──────────────┐
│     Servidor     │                                  │  DNS Table   │
│ (Operações + IA) │                                  │ (Serviços)   │
└──────────────────┘                                  └──────────────┘
```


### Funcionalidades

### - Calculadora
- Operações básicas: soma, subtração, multiplicação e divisão
- Interface moderna com feedback visual
- Execução remota das operações

#### - Fatorial
- Cálculo de fatorial de números inteiros positivos
- Validação de entrada
- Processamento via servidor RPC

#### - Verificador de Números Primos
- Verificação de múltiplos números simultaneamente
- Entrada por lista separada por vírgulas
- Retorno estruturado dos resultados

### - Notícias
- Exibição de notícias atualizadas
- Interface somente leitura
- Suporte a scroll vertical

### - Resolvedor com IA
- Envio de problemas matemáticos em linguagem natural
- Integração com IA (ex.: Gemini)
- Retorno de soluções explicadas


### Estrutura do Projeto
```
.
| main.py
├── client/
| |── client_server.py
| |── operations.py
| |── resolver_dns.py
│
├── interface/
| |── calculator_frame.py 
│ ├── chat_frame.py 
│ ├── factorial_frame.py
│ ├── home_frame.py
│ ├── interface.py 
│ ├── menu_fram.py
│ ├── news_frame.py
│ └── prime_frame.py
│
├── server/
| |── authoritative_dns
| |── consts.py
| |── dns_table.json
│ ├── exceptions.py
│ ├── general_operations_service.py
| |── math_operations_service.py
| |── operations_server.py
| |── settings.json
│ └── utils.py
│
├── requirements.txt
└── README.md
```


### Principais Componentes

#### `HomeFrame`
Tela inicial com apresentação do sistema e atalhos visuais para as funcionalidades.

#### `CalculatorFrame`
Calculadora gráfica com botões interativos e exibição de resultados.

#### `FactorialFrame`
Interface dedicada ao cálculo de fatoriais.

#### `PrimeFrame`
Interface para verificação de números primos em lote.

#### `NewsFrame`
Exibição de notícias em formato de texto com rolagem.

#### `ChatFrame`
Interface de interação com a IA para resolução de problemas matemáticos.


### Tecnologias Utilizadas

- **Python 3.10+**
- **Tkinter**
- **RPC (Remote Procedure Call)**
- **Inteligência Artificial (Gemini)**
- **Arquitetura modular**


### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Conexão com a internet (para IA e notícias)
- Chave de API do Google Gemini (para funcionalidade de IA)


### Como Executar

#### Clonar o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

#### Instalar dependências
```
pip install -r requirements.txt
```

#### Iniciar o servidor
```
python3 -m server.operatrions_server.py
```

#### Iniciar o serviços de dns
```
python3 -m server.authoritative_dns
```

#### Iniciar o cliente
```
python3 -m client.client_server
```

#### Iniciar a aplicação
```
python3 main.py
```
