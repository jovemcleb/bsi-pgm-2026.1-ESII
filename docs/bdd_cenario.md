# language: pt
Funcionalidade: Limite de empréstimos simultâneos

  Cenário: bloquear terceiro empréstimo em aberto do mesmo usuário
    Dado que Ana já possui 2 empréstimos em aberto
    E que o equipamento de id 3 está disponível
    Quando ela tenta registrar um novo empréstimo
    Então o registro deve ser recusado
