# sistema_de_energia

Este projeto é uma aplicação web para simular o gerenciamento de consumo de energia de dispositivos domésticos, com integração de fontes de energia (Companhia Elétrica e Energia Solar). O sistema calcula o consumo em tempo real e alterna automaticamente entre as fontes de energia com base nas tarifas configuradas.

Índice
Recursos
Pré-requisitos
Como Rodar o Projeto
Funcionalidades
Estrutura de Arquivos
Explicação do Código
Contribuição
Licença
Recursos
Adicionar, remover e listar dispositivos com potência e horas de uso.
Atualizar tarifas de energia (Companhia e Solar).
Simulação em tempo real do consumo total e alternância automática de fonte de energia.
Interface moderna e responsiva com Bootstrap.
Backend implementado com Flask (Python).
Pré-requisitos
Python 3.7 ou superior
Gerenciador de pacotes pip
Biblioteca Flask instalada
Navegador Web (Chrome, Firefox, etc.)
Como Rodar o Projeto
Clone o Repositório

bash
Copiar código
git clone https://github.com/seu-usuario/sistema-de-energia.git
cd sistema-de-energia
Instale as Dependências Execute o seguinte comando para instalar o Flask:

bash
Copiar código
pip install flask
Inicie o Servidor Execute o arquivo principal:

bash
Copiar código
python app.py
Acesse no Navegador Após iniciar o servidor, acesse no navegador o seguinte endereço:

arduino
Copiar código
http://127.0.0.1:5000/
Funcionalidades
Consumo Atual

Mostra o consumo total em kWh e a fonte de energia atual (Companhia Elétrica ou Energia Solar).
Adicionar Dispositivo

Adicione dispositivos com:
Nome
Potência (em Watts)
Horas de uso por dia
Remover Dispositivo

Remova dispositivos específicos clicando no botão "Remover".
Atualizar Tarifas

Atualize as tarifas de energia da Companhia Elétrica e da Energia Solar.
Simulação em Tempo Real

A simulação calcula o consumo e alterna entre as fontes automaticamente com base nas tarifas configuradas.
Estrutura de Arquivos
plaintext
Copiar código
.
├── app.py                  # Backend em Flask
├── templates
│   └── index.html          # Interface HTML principal
└── static
    └── css                 # (Opcional) Estilos customizados
Explicação do Código
Backend (app.py)
Classe EnergySystem:

Gerencia os dispositivos adicionados.
Calcula o consumo total de energia com base na potência e nas horas de uso.
Alterna entre as fontes de energia com base nas tarifas.
Rotas da API:

GET /api/get_data: Retorna os dados atuais do sistema (consumo, dispositivos, tarifas).
POST /api/add_device: Adiciona um dispositivo ao sistema.
POST /api/remove_device: Remove um dispositivo do sistema.
POST /api/update_rates: Atualiza as tarifas de energia.
POST /api/start: Inicia a simulação em tempo real.
POST /api/stop: Para a simulação.
Simulação em Tempo Real:

Utiliza threading para realizar cálculos contínuos sem bloquear a interface.
Frontend (index.html)
Estrutura:

Interface responsiva construída com Bootstrap.
Elementos para exibir consumo, dispositivos e atualizações de tarifas.
JavaScript Integrado:

Atualiza os dados automaticamente a cada 2 segundos.
Realiza chamadas às APIs para adicionar, remover ou atualizar dispositivos e tarifas.
