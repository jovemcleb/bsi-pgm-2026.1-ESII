# ADR-001 - Arquitetura da v2.0

## Contexto

A versao 1.0 concentra menu, regras de negocio, estado em memoria e notificacoes no mesmo arquivo, o que ja aparece como problema em [PROBLEMAS.md](../PROBLEMAS.md) e no codigo legado em [emprestimos.py](../emprestimos.py).

Para a versao 2.0, a decisao arquitetural precisa atender dois requisitos nao funcionais:

- RNF03: adicionar um novo tipo de equipamento sem alterar multiplos modulos.
- RNF04: testar regras de negocio de forma isolada, sem entrada do usuario nem estado externo.

Ao mesmo tempo, o projeto continua sendo uma aplicacao de linha de comando simples, mantida por uma equipe iniciante e sem dependencias externas.

## Opcoes consideradas

| Criterio | Arquivo unico | Em camadas | MVC |
|---|---|---|---|
| Atende RNF03 (novo tipo sem modificar multiplos modulos)? | Nao | Sim | Parcial |
| Atende RNF04 (testar regras sem estado externo)? | Nao | Sim | Parcial |
| Adequado para CLI sem interface grafica? | Sim | Sim | Parcial |
| Familiar para equipe iniciante? | Sim no curto prazo, mas escala mal | Sim | Parcial |

- Arquivo unico: foi descartado porque repete o problema da v1.0. A interface, o estado e as regras continuam acoplados, entao mudar tipos de equipamento e testar regras isoladas segue caro.
- Em camadas: separa responsabilidades sem introduzir estruturas desnecessarias para um sistema de CLI. Permite manter as regras puras no dominio e deixar entrada, saida e adaptadores fora dessa camada.
- MVC: tambem poderia separar partes do sistema, mas adiciona mais cerimonia do que o projeto precisa. Para uma CLI textual e uma equipe iniciante, controller e view tendem a aumentar a complexidade sem ganho proporcional.

## Decisao

Adotar arquitetura em camadas com duas camadas para a v2.0.

As camadas definidas para o repositorio sao:

- cli/: interacao com a CLI, menu textual, leitura de entradas e exibicao de mensagens.
- negocio/: regras de negocio do sistema, validacoes, calculo de multas, controle de emprestimos e organizacao do estado em memoria.

O arquivo main.py sera o ponto de entrada da aplicacao e, mais adiante, chamara a camada cli.

Para atender RNF03, a variacao por tipo de equipamento deve ficar centralizada em um unico modulo da camada de negocio, evitando espalhar ifs por diferentes partes do sistema.

Para atender RNF04, a camada cli apenas coleta entradas e mostra saidas, enquanto a camada de negocio permanece testavel sem input(), print() ou dependencia de interface.

## Consequencias

- As regras de negocio passam a poder ser testadas sem input(), print() ou listas globais compartilhadas.
- A CLI deixa de decidir regras; ela apenas coleta dados e mostra resultados.
- A adicao de novos tipos de equipamento fica concentrada na camada de negocio, reduzindo o impacto de manutencao.
- O projeto ganha uma separacao simples o bastante para a equipe iniciante, sem a cerimonia extra de uma decomposicao mais detalhada.
- Durante a transicao, [emprestimos.py](../emprestimos.py) permanece intacto como referencia do legado enquanto a v2.0 nasce ao lado dele.