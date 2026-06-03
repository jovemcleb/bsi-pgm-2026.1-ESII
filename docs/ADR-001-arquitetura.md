# ADR-001 - Arquitetura da v2.0

**Status:** Accepted
**Data:** 2026-04-22

## Contexto

A versao 1.0 concentra menu, regras de negocio, estado em memoria e notificacoes no mesmo arquivo, o que ja aparece como problema em [PROBLEMAS.md](../PROBLEMAS.md) e no codigo legado em [emprestimos.py](../emprestimos.py).

Para a versao 2.0, a decisao arquitetural precisa atender dois requisitos nao funcionais:

- RNF03: adicionar um novo tipo de equipamento sem alterar multiplos modulos.
- RNF04: testar regras de negocio de forma isolada, sem entrada do usuario nem estado externo.

Ao mesmo tempo, o projeto continua sendo uma aplicacao de linha de comando simples, mantida por uma equipe iniciante e sem dependencias externas.

## Opcoes consideradas

| Criterio                                                  | Arquivo unico                      | Em camadas | MVC     |
| --------------------------------------------------------- | ---------------------------------- | ---------- | ------- |
| Atende RNF03 (novo tipo sem modificar multiplos modulos)? | Nao                                | Sim        | Parcial |
| Atende RNF04 (testar regras sem estado externo)?          | Nao                                | Sim        | Parcial |
| Adequado para CLI sem interface grafica?                  | Sim                                | Sim        | Parcial |
| Familiar para equipe iniciante?                           | Sim no curto prazo, mas escala mal | Sim        | Parcial |

- Arquivo unico: foi descartado porque repete o problema da v1.0. A interface, o estado e as regras continuam acoplados, entao mudar tipos de equipamento e testar regras isoladas segue caro.
- Em camadas: separa responsabilidades sem introduzir estruturas desnecessarias para um sistema de CLI. Permite manter as regras puras no dominio e deixar entrada, saida e adaptadores fora dessa camada.
- MVC: tambem poderia separar partes do sistema, mas adiciona mais cerimonia do que o projeto precisa. Para uma CLI textual e uma equipe iniciante, controller e view tendem a aumentar a complexidade sem ganho proporcional.

## Decisao

Adotar arquitetura em camadas com separacao por pacotes para a v2.0.

As camadas definidas para o repositorio sao:

- main.py: ponto de entrada da aplicacao, menu textual, leitura de entradas e exibicao de mensagens.
- models/: tipos do dominio, como Equipamento e Emprestimo.
- repositories/: contratos e implementacoes de persistencia, escondendo o armazenamento em memoria.
- services/: casos de uso, regras de negocio e notificacoes.

O arquivo main.py sera o ponto de composicao da aplicacao, criando as implementacoes concretas e injetando essas dependencias em ServicoEmprestimo.

Para atender RNF03, a variacao por tipo de equipamento deve ficar centralizada em models/, evitando espalhar ifs por diferentes partes do sistema.

Para atender RNF04, ServicoEmprestimo depende das abstracoes IRepositorioEmprestimo e INotificador, o que permite testar as regras com fakes ou mocks sem input(), print() ou estado externo.

## Consequencias

- As regras de negocio passam a poder ser testadas sem input(), print() ou listas globais compartilhadas.
- A CLI deixa de decidir regras; main.py apenas coleta dados, mostra resultados e monta as dependencias.
- A adicao de novos tipos de equipamento fica concentrada em models/, reduzindo o impacto de manutencao.
- O projeto ganha uma separacao simples o bastante para a equipe iniciante, sem a cerimonia extra de uma decomposicao mais detalhada.
- Durante a transicao, [emprestimos.py](../emprestimos.py) permanece intacto como referencia do legado enquanto a v2.0 nasce ao lado dele.
