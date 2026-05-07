# Diagramas e Decomposição

## Decomposição em camadas

Arquitetura de referência: ADR-001 (duas camadas — `cli/` e `negocio/`).

| Classe / Módulo                      | Camada     | Justificativa                                                                                                                                                                                                                             |
| ------------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `models/Equipamento`                 | `negocio/` | Tipo do domínio com alta coesão: agrupa apenas os atributos e o estado de um equipamento, sem lógica de interface ou persistência.                                                                                                        |
| `models/Emprestimo`                  | `negocio/` | Tipo do domínio que representa o vínculo entre um equipamento e um aluno; encapsula as regras de data e multa, isolando o conceito de negócio de qualquer detalhe de I/O.                                                                 |
| `services/ServicoEmprestimo`         | `negocio/` | Concentra os três casos de uso do fluxo principal (registrar, devolver, listar atrasados); tem um único motivo para mudar — a regra de negócio de empréstimo —, satisfazendo o princípio de responsabilidade única (SRP, Cap. 5 Valente). |
| `services/Notificador`               | `negocio/` | Isola o canal de aviso ao usuário; separado de `ServicoEmprestimo` porque mudar o meio de notificação (console, e-mail, SMS) não deve exigir alteração na lógica de empréstimo — ocultamento de informação aplicado à camada de serviço.  |
| `repositories/RepositorioEmprestimo` | `negocio/` | Esconde o mecanismo de armazenamento (lista em memória, arquivo, banco) atrás de uma interface estável; reduz o acoplamento de `ServicoEmprestimo` com a infraestrutura de persistência.                                                  |
| `main.py` / `cli/App`                | `cli/`     | Ponto de entrada que apenas lê comandos do usuário e delega para `ServicoEmprestimo`; não contém regra de negócio, garantindo separação entre apresentação e domínio (ADR-001).                                                           |

---

## Diagramas de sequência

### UC01 — Registrar Empréstimo

![alt text](image.png)

```mermaid
sequenceDiagram
    actor Atendente
    participant main as main.py
    participant servico as ServicoEmprestimo
    participant repo as RepositorioEmprestimo
    participant notif as Notificador

    Atendente->>main: informa equip_id, nome, email, dias
    main->>servico: registrar(equip_id, nome, email, dias)
    servico->>repo: buscar_equipamento(equip_id)
    repo-->>servico: Equipamento
    alt equipamento disponível
        servico->>repo: salvar_emprestimo(emprestimo)
        servico->>repo: marcar_indisponivel(equip_id)
        servico->>notif: notificar_emprestimo(email, data_devolucao)
        servico-->>main: True
    else equipamento indisponível
        servico-->>main: False
    end
```

### UC02 — Registrar Devolução

![alt text](image-1.png)

```mermaid
sequenceDiagram
    actor Atendente
    participant main as main.py
    participant servico as ServicoEmprestimo
    participant repo as RepositorioEmprestimo
    participant notif as Notificador

    Atendente->>main: informa emprestimo_id
    main->>servico: devolver(emprestimo_id)
    servico->>repo: buscar_emprestimo(emprestimo_id)
    repo-->>servico: Emprestimo
    alt empréstimo existe e não foi devolvido
        servico->>servico: calcular_atraso(data_devolucao)
        servico->>servico: calcular_multa(dias_atraso, tipo_equipamento)
        servico->>repo: registrar_devolucao(emprestimo_id, data_devolucao)
        servico->>repo: marcar_disponivel(equip_id)
        servico->>notif: notificar_devolucao(email, multa)
        servico-->>main: multa
    else empréstimo inválido ou já devolvido
        servico-->>main: None
    end
```

### UC03 — Listar Empréstimos em Atraso

![alt text](image-2.png)

```mermaid
sequenceDiagram
    actor Coordenador
    participant main as main.py
    participant servico as ServicoEmprestimo
    participant repo as RepositorioEmprestimo
    participant notif as Notificador

    Coordenador->>main: seleciona "listar atrasados"
    main->>servico: listar_atrasados()
    servico->>repo: listar_todos()
    repo-->>servico: lista de Emprestimo
    loop para cada empréstimo ativo
        servico->>servico: verificar_atraso(data_devolucao)
        alt empréstimo em atraso
            servico->>notif: notificar_atraso(email, dias_atraso, multa)
        end
    end
    servico-->>main: lista de atrasados
    alt há empréstimos em atraso
        main-->>Coordenador: exibe nome, dias de atraso e multa por linha
    else nenhum atraso
        main-->>Coordenador: "Nenhum empréstimo em atraso"
    end
```
