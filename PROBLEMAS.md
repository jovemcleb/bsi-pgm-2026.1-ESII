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

-

_(Este espaço será preenchido após a Aula 4, quando os termos técnicos corretos forem aprendidos)_
