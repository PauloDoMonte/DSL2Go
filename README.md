# DSL2Go

DSL2Go é uma ferramenta que transpila um Domain Specific Language (DSL) para a estrutura de um projeto Go completo. A ferramenta lê um arquivo DSL com definições de API, rotas, modelos, repositórios, controladores, serviços e middlewares e gera automaticamente os arquivos e pastas necessários para iniciar o desenvolvimento de uma aplicação Go.

## Funcionalidades

- Parse do arquivo DSL e extração dos comandos definidos para API, rotas, modelos, repositórios, controladores, serviços e middlewares.
- Geração automática de arquivos Go baseados no DSL fornecido.
- Organização da estrutura do projeto em pastas (models, repositories, controllers, services, middlewares, routes).
- Criação de arquivos de suporte, como `main.go` e `Dockerfile`, a partir de templates.
