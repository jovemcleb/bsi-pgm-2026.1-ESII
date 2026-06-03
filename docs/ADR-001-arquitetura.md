# ADR-001 - Arquitetura da v2.0

**Status:** Accepted
**Data:** 2026-04-22

## Contexto

A versão 1.0 concentra menu, regras de negócio, estado em memória e notificações no mesmo arquivo, o que já aparece como problema em [PROBLEMAS.md](../PROBLEMAS.md) e no código legado em [emprestimos.py](../emprestimos.py).

Para a versão 2.0, a decisão arquitetural precisa atender dois requisitos não funcionais:

- RNF03: adicionar um novo tipo de equipamento sem alterar múltiplos módulos.
- RNF04: testar regras de negócio de forma isolada, sem entrada do usuário nem estado externo.

Ao mesmo tempo, o projeto continua sendo uma aplicação de linha de comando simples, mantida por uma equipe iniciante e sem dependências externas.

## Opções consideradas

| Critério                                                  | Arquivo único                      | Em camadas | MVC     |
| --------------------------------------------------------- | ---------------------------------- | ---------- | ------- |
| Atende RNF03 (novo tipo sem modificar múltiplos módulos)? | Não                                | Sim        | Parcial |
| Atende RNF04 (testar regras sem estado externo)?          | Não                                | Sim        | Parcial |
| Adequado para CLI sem interface gráfica?                  | Sim                                | Sim        | Parcial |
| Familiar para equipe iniciante?                           | Sim no curto prazo, mas escala mal | Sim        | Parcial |

- Arquivo único: foi descartado porque repete o problema da v1.0. A interface, o estado e as regras continuam acoplados, então mudar tipos de equipamento e testar regras isoladas segue caro.
- Em camadas: separa responsabilidades sem introduzir estruturas desnecessárias para um sistema de CLI. Permite manter as regras puras no domínio e deixar entrada, saída e adaptadores fora dessa camada.
- MVC: também poderia separar partes do sistema, mas adiciona mais cerimônia do que o projeto precisa. Para uma CLI textual e uma equipe iniciante, controller e view tendem a aumentar a complexidade sem ganho proporcional.

## Decisão

Adotar arquitetura em camadas com separação por pacotes para a v2.0.

As camadas definidas para o repositório são:

- main.py: ponto de entrada da aplicação, menu textual, leitura de entradas e exibição de mensagens.
- models/: tipos do domínio, como Equipamento e Emprestimo.
- repositories/: contratos e implementações de persistência, escondendo o armazenamento em memória.
- services/: casos de uso, regras de negócio e notificações.

O arquivo main.py será o ponto de composição da aplicação, criando as implementações concretas e injetando essas dependências em ServicoEmprestimo.

Para atender RNF03, a variação por tipo de equipamento deve ficar centralizada em models/, evitando espalhar ifs por diferentes partes do sistema.

Para atender RNF04, ServicoEmprestimo depende das abstrações IRepositorioEmprestimo e INotificador, o que permite testar as regras com fakes ou mocks sem input(), print() ou estado externo.

## Consequências

- As regras de negócio passam a poder ser testadas sem input(), print() ou listas globais compartilhadas.
- A CLI deixa de decidir regras; main.py apenas coleta dados, mostra resultados e monta as dependências.
- A adição de novos tipos de equipamento fica concentrada em models/, reduzindo o impacto de manutenção.
- O projeto ganha uma separação simples o bastante para a equipe iniciante, sem a cerimônia extra de uma decomposição mais detalhada.
- Durante a transição, [emprestimos.py](../emprestimos.py) permanece intacto como referência do legado enquanto a v2.0 nasce ao lado dele.
