# Problemas Identificados — Leitura Inicial do Código

Este arquivo é preenchido pelos estudantes na Aula 1 após a leitura do código legado.
Descreva em linguagem livre tudo que parecer estranho, errado ou difícil de entender.
Não é necessário usar termos técnicos neste momento.

---

## Minha leitura inicial

- O documento diz que o prazo minimo de emprestimo e 1 dia, mas o codigo aceita qualquer valor de dias (inclusive 0 ou negativo).
- A documentacao fala em enviar notificacao por e-mail, mas o sistema so imprime mensagens com "[EMAIL]" na tela.
- O sistema deveria ser facil de adaptar para novos tipos de equipamento, mas hoje precisa mexer em varios pontos diferentes para isso funcionar.
- O codigo depende de listas globais que ficam soltas no arquivo inteiro, entao uma parte mexe no estado da outra sem controle.
- As regras principais estao misturadas com entrada de usuario (input/menu), o que dificulta testar cada parte separadamente.
- O calculo de multa aparece repetido em mais de um lugar; se corrigir em um ponto e esquecer outro, o sistema pode ficar incoerente.
- O proprio projeto reconhece que nao ha testes automatizados, e isso bate com o repositorio atual: nao existe nenhuma bateria de testes para validar mudancas.

---

## Revisão com vocabulário técnico

- Ausencia de validacao de regra de negocio: o prazo minimo de emprestimo nao e protegido por nenhuma verificacao no metodo registrar, entao uma restricao do dominio fica fora do codigo e pode ser violada com facilidade.
- Alto acoplamento entre negocio e mecanismo de notificacao: o sistema afirma enviar e-mail, mas a implementacao mistura a regra de emprestimo com saidas em tela usando print, sem uma abstracao propria para notificacao.
- Violacao do principio aberto/fechado e alto acoplamento com tipos concretos: para adicionar um novo tipo de equipamento e preciso alterar condicionais espalhadas pelo sistema, o que mostra que a politica de multa nao esta encapsulada.
- Acoplamento por estado global compartilhado: a classe Sistema depende diretamente das listas globais equipamentos e emprestimos_registrados, sem ocultamento de informacao nem controle claro sobre quem pode alterar esse estado.
- Baixa coesao e violacao de SRP: entrada de usuario, fluxo de menu e regras de negocio estao misturados no mesmo arquivo, o que junta responsabilidades de apresentacao e dominio em um unico modulo.
- Duplicacao de regra de negocio: o calculo de multa aparece em mais de um metodo, criando multiplos pontos de mudanca e aumentando o risco de inconsistencias quando a regra evoluir.
- Baixa testabilidade e risco maior de regressao: a ausencia de testes automatizados impede validar o comportamento das regras com seguranca, o que agrava os efeitos do alto acoplamento e da mistura de responsabilidades.
