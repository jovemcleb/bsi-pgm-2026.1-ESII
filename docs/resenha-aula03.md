# Resenha Aula 3 - Modelos UML e Design de Componentes

**Aluno:** Caleb Cardoso Lima
**Data:** 29/04/2026

## Questão 1 - Modelos UML como ferramentas de modelagem

### (a) Estrutura x comportamento

No Cap. 4, nas seções "Diagrama de Classes" e "Diagrama de Sequência", Valente lembra que diagramas UML são modelos: destacam um aspecto e omitem outros. O diagrama de classes mostra a estrutura estática do sistema, isto é, classes, responsabilidades, métodos e relações. Ele não mostra a ordem das chamadas nem o fluxo de um cenário. Já o diagrama de sequência mostra objetos em interação e a ordem temporal das mensagens. Por isso os dois são complementares: um explica a organização do sistema; o outro, seu comportamento em execução.

### (b) Consequência prática

Na prática, o diagrama de classes ajuda a decidir a decomposição da solução: que classes devem existir, quais interfaces públicas expor e onde ficam as dependências. Ele apoia decisões de responsabilidade, coesão e acoplamento. O diagrama de sequência ajuda a decidir colaboração: quem chama quem, em que ponto entra uma validação e se a interface com o usuário está invadindo a regra de negócio. Assim, classes ajudam a projetar a forma; sequências, o protocolo de execução.

### (c) Aplicação ao UC01

No UC01, o texto de casos_de_uso.md diz apenas que o sistema pede dados, registra o empréstimo, marca indisponibilidade e notifica. Um diagrama de sequência revela quem faz cada passo e em que ordem. No desenho final do projeto, o fluxo passa por Atendente -> CLI -> ServicoEmprestimo -> RepositorioEmprestimo -> Notificador. Isso obriga o design a explicitar mensagens como buscar_equipamento, salvar_emprestimo, marcar_indisponivel e notificar_emprestimo, além da criação do objeto Emprestimo com a data de devolução calculada. Ou seja, o caso de uso textual descreve o que acontece; a sequência mostra como os objetos colaboram para fazer acontecer.

## Questão 2 - Arquitetura, design e os princípios de decomposição

### (a) Definições

No Cap. 5, nas seções sobre ocultamento de informação, coesão e acoplamento, eu entendo coesão como foco claro: dados e métodos empurram para a mesma responsabilidade. Acoplamento é o quanto uma mudança em um módulo tende a obrigar mudanças em outros; ele é baixo quando a dependência passa por contratos pequenos e estáveis. Ocultamento de informação é esconder decisões de implementação que podem mudar, expondo só a interface necessária ao restante do sistema.

### (b) Relações entre os princípios

O ocultamento de informação reduz acoplamento porque o cliente deixa de depender de listas, ifs e detalhes internos, passando a depender de uma interface previsível. Ele também reforça coesão: só é possível esconder bem um módulo cuja responsabilidade esteja concentrada. Há, sim, uma tensão prática: se eu dividir demais o sistema para deixar tudo muito "puro", posso multiplicar dependências entre classes. O objetivo, então, não é maximizar cada princípio isoladamente, mas criar fronteiras claras, poucas interfaces e responsabilidades bem definidas.

### (c) Aplicação ao projeto v2.0

Seguindo o ADR-001 e o Cap. 7, a arquitetura macro da v2.0 continua em cli/ e negocio/. Dentro de negocio/, eu adotaria uma decomposição interna mais próxima da solução-guia porque ela passa melhor no critério de responsabilidade única. Em models/, deixaria Equipamento e Emprestimo como tipos do domínio, com alta coesão e campos explícitos, sem lógica de interface. Em services/, ServicoEmprestimo concentraria registrar, devolver e listar atrasados, porque os três casos de uso pertencem ao mesmo fluxo de negócio; e Notificador ficaria separado, pois mudar o canal de aviso não deve alterar a regra de empréstimo. Em repositories/, RepositorioEmprestimo esconderia o armazenamento e reduziria o acoplamento do serviço com listas ou banco. Em main.py, ficaria só a CLI.

## Questão 3 - Crítica fundamentada à documentação do sistema legado

### (a) Pontos frágeis

À luz do Cap. 7, vejo duas fragilidades em docs/projeto.md. A primeira é baixa coesão arquitetural: ao assumir, em DP01, que toda a lógica fica em um único arquivo, o documento junta interface, regras de negócio, estado e notificações no mesmo módulo. Isso enfraquece a decomposição em partes independentes, que é o papel da arquitetura. A segunda é acoplamento por variável global com violação de ocultamento de informação: o próprio diagrama registra que Sistema acessa diretamente equipamentos[] e emprestimos_registrados[]. Nesse desenho, a lógica de negócio depende de detalhes internos de armazenamento; qualquer mudança na representação dos dados tende a se propagar pelo sistema.

### (b) Ponto forte

O melhor ponto do documento é que ele não romantiza a v1.0: já registra que a ausência de camadas é dívida técnica intencional e aponta a refatoração para arquitetura em camadas na v2.0. À luz do Cap. 7, isso é uma boa decisão porque reconhece a separação dos módulos mais importantes e de suas dependências. Ao mirar camadas, o documento aponta para mais coesão por módulo e menor acoplamento entre interface e negócio.

### (c) Síntese

Para mim, a transparência da tabela DT01-DT07 revela um desenvolvedor mais maduro do que o código da v1.0 sugere. No Cap. 1, na discussão sobre manutenção e envelhecimento do software, Valente mostra que sistemas mudam e precisam de cuidado contínuo; logo, assumir dívida técnica explicitamente é melhor do que fingir que uma solução provisória já basta. Aqui a dívida foi deliberada: aceitou-se um atalho para entregar, mas sem esconder seus custos. Isso inaugura para a v2.0 uma postura importante: evoluir o sistema por refatoração orientada por critérios, atacando primeiro o que compromete testabilidade, manutenibilidade e extensão futura.

## Questão 4 - Tipos como contratos: dicionários x classes

### (a) Prevenção de erros

Em emprestimos.py, o sistema depende de chaves soltas, como equipamento["disponivel"] e emprestimo["data_devolucao"]. Isso deixa passar erros que uma classe reduziria. Se alguém digitar equipamento["dispnoivel"], por exemplo, o problema só aparece em execução, com KeyError. Com uma dataclass como Equipamento, a forma equivalente, equipamento.dispnoivel, tende a ser apontada antes por ferramentas como Pyright ou pelo próprio editor. O mesmo vale para campos ausentes ou tipos inadequados, como guardar texto onde o código espera uma data. Com classes, o contrato fica mais explícito: Equipamento teria atributos esperados, Emprestimo teria campos com significado definido e ferramentas de análise acusariam usos inconsistentes mais cedo. O perfil do erro muda: sai um erro implícito e tardio; entra um erro mais localizado.

### (b) Capacidade de evolução

Uma classe também melhora a evolução porque pode ganhar comportamento sem obrigar o resto do sistema a conhecer sua estrutura interna. Se amanhã Emprestimo receber um método calcular_multa(), clientes passam a pedir um serviço ao objeto, não a reconstruir a regra com chaves e ifs espalhados. Isso preserva ocultamento de informação: a política pode mudar por dentro sem quebrar quem consome o objeto. Já um dicionário carrega dados, mas não define onde o comportamento deve morar; por isso a lógica tende a se espalhar, como já acontece com a multa no legado.

### (c) Comunicação do design

Por isso, nos Caps. 4 e 5, Valente trata clareza de modelo como decisão de projeto, não como detalhe de estilo. O nome de um tipo como Equipamento comunica papel no domínio e limites do objeto; dict não comunica nada além de "há pares chave-valor aqui". Quando leio Equipamento, espero disponibilidade, identificação e regras ligadas ao item emprestado. Quando leio dict, preciso inspecionar o uso para descobrir o que ele representa. Em projeto, essa diferença importa porque bons tipos tornam o sistema mais legível para quem vai mantê-lo e evoluí-lo.
