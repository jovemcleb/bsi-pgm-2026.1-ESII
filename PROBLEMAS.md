# Problemas Identificados — Leitura Inicial do Código

Este arquivo é preenchido pelos estudantes na Aula 1 após a leitura do código legado.
Descreva em linguagem livre tudo que parecer estranho, errado ou difícil de entender.
Não é necessário usar termos técnicos neste momento.

---

## Minha leitura inicial

- O documento diz que o prazo mínimo de empréstimo é 1 dia, mas o código aceita qualquer valor de dias (inclusive 0 ou negativo).
- A documentação fala em enviar notificação por e-mail, mas o sistema só imprime mensagens com "[EMAIL]" na tela.
- O sistema deveria ser fácil de adaptar para novos tipos de equipamento, mas hoje precisa mexer em vários pontos diferentes para isso funcionar.
- O código depende de listas globais que ficam soltas no arquivo inteiro, então uma parte mexe no estado da outra sem controle.
- As regras principais estão misturadas com entrada de usuário (input/menu), o que dificulta testar cada parte separadamente.
- O cálculo de multa aparece repetido em mais de um lugar; se corrigir em um ponto e esquecer outro, o sistema pode ficar incoerente.
- O próprio projeto reconhece que não há testes automatizados, e isso bate com o repositório atual: não existe nenhuma bateria de testes para validar mudanças.

---

## Revisão com vocabulário técnico

- Ausência de validação de regra de negócio: o prazo mínimo de empréstimo não é protegido por nenhuma verificação no método registrar, então uma restrição do domínio fica fora do código e pode ser violada com facilidade.
- Alto acoplamento entre negócio e mecanismo de notificação: o sistema afirma enviar e-mail, mas a implementação mistura a regra de empréstimo com saídas em tela usando print, sem uma abstração própria para notificação.
- Violação do princípio aberto/fechado e alto acoplamento com tipos concretos: para adicionar um novo tipo de equipamento é preciso alterar condicionais espalhadas pelo sistema, o que mostra que a política de multa não está encapsulada.
- Acoplamento por estado global compartilhado: a classe Sistema depende diretamente das listas globais equipamentos e emprestimos_registrados, sem ocultamento de informação nem controle claro sobre quem pode alterar esse estado.
- Baixa coesão e violação de SRP: entrada de usuário, fluxo de menu e regras de negócio estão misturados no mesmo arquivo, o que junta responsabilidades de apresentação e domínio em um único módulo.
- Duplicação de regra de negócio: o cálculo de multa aparece em mais de um método, criando múltiplos pontos de mudança e aumentando o risco de inconsistências quando a regra evoluir.
- Baixa testabilidade e risco maior de regressão: a ausência de testes automatizados impede validar o comportamento das regras com segurança, o que agrava os efeitos do alto acoplamento e da mistura de responsabilidades.
