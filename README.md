# Monitoramento de Ping

Este projeto realiza o monitoramento contínuo de conectividade de rede utilizando o comando `ping`. Ele exibe o status da conexão, latência e notifica o usuário em caso de perda de pacotes, inclusive por voz.

## Funcionalidades

- Ping contínuo para um host configurável.
- Exibição colorida do status:
  - Verde: Latência baixa.
  - Amarelo: Latência alta.
  - Vermelho: Perda de pacote ou erro.
- Notificação por voz em caso de perda de pacote.
- Compatível com Windows, Linux e macOS.

## Requisitos

- Python 3.10 ou superior
- [colorama](https://pypi.org/project/colorama/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)

## Instalação

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git