# Diagramas e Decomposição

## Decomposição em camadas

Arquitetura de referência: ADR-001 (entrada em `main.py` e separação em `models/`, `repositories/` e `services/`).

| Classe / Módulo                      | Camada     | Justificativa                                                                                                                                                                                                                             |
| ------------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `models/Equipamento`                 | `models/`  | Tipo do domínio com alta coesão: agrupa apenas os atributos e o estado de um equipamento, sem lógica de interface ou persistência.                                                                                                        |
| `models/Emprestimo`                  | `models/`  | Tipo do domínio que representa o vínculo entre um equipamento e um aluno; reúne os dados do empréstimo com campos explícitos e tipados, sem misturar interface, persistência ou detalhes de I/O.                                          |
| `services/ServicoEmprestimo`         | `services/` | Concentra os três casos de uso do fluxo principal (registrar, devolver, listar atrasados); tem um único motivo para mudar — a regra de negócio de empréstimo —, satisfazendo o princípio de responsabilidade única (SRP, Cap. 5 Valente). |
| `services/Notificador`               | `services/` | Isola o canal de aviso ao usuário; separado de `ServicoEmprestimo` porque mudar o meio de notificação (console, e-mail, SMS) não deve exigir alteração na lógica de empréstimo — ocultamento de informação aplicado à camada de serviço.  |
| `repositories/RepositorioEmprestimo` | `repositories/` | Esconde o mecanismo de armazenamento (lista em memória, arquivo, banco) atrás de uma interface estável; reduz o acoplamento de `ServicoEmprestimo` com a infraestrutura de persistência.                                                  |
| `main.py`                            | `entrada`  | Ponto de entrada que apenas lê comandos do usuário e delega para `ServicoEmprestimo`; não contém regra de negócio, garantindo separação entre apresentação e domínio (ADR-001).                                                           |

---

## Diagrama de classes — v2.0

```mermaid
classDiagram
    class IRepositorioEmprestimo {
        <<interface>>
        +buscar_equipamento(equip_id) Equipamento
        +salvar_emprestimo(emprestimo) None
        +marcar_indisponivel(equip_id) None
        +buscar_emprestimo(emprestimo_id) Emprestimo
        +registrar_devolucao(emprestimo_id, data_devolucao) None
        +marcar_disponivel(equip_id) None
        +listar_todos() List~Emprestimo~
    }

    class INotificador {
        <<interface>>
        +notificar_emprestimo(email, data_devolucao) None
        +notificar_devolucao(email, multa) None
        +notificar_atraso(email, dias_atraso, multa) None
    }

    class RepositorioEmprestimo {
        -equipamentos
        -emprestimos_registrados
        +buscar_equipamento(equip_id) Equipamento
        +salvar_emprestimo(emprestimo) None
        +marcar_indisponivel(equip_id) None
        +buscar_emprestimo(emprestimo_id) Emprestimo
        +registrar_devolucao(emprestimo_id, data_devolucao) None
        +marcar_disponivel(equip_id) None
        +listar_todos() List~Emprestimo~
    }

    class Notificador {
        +notificar_emprestimo(email, data_devolucao) None
        +notificar_devolucao(email, multa) None
        +notificar_atraso(email, dias_atraso, multa) None
    }

    class ServicoEmprestimo {
        -repositorio: IRepositorioEmprestimo
        -notificador: INotificador
        +registrar(equip_id, nome, email, dias) bool
        +devolver(emprestimo_id) float
        +listar_atrasados() List~ResumoAtraso~
        +calcular_atraso(data_devolucao) int
        +calcular_multa(dias_atraso, equipamento_id) float
        +verificar_atraso(data_devolucao) bool
    }

    class Equipamento {
        <<abstract>>
        +id: int
        +nome: str
        +tipo: str
        +disponivel: bool
        +calcular_multa(dias_atraso) float
    }

    class Notebook
    class Projetor
    class CaboHDMI

    class Emprestimo {
        +id: int
        +equipamento_id: int
        +equipamento_nome: str
        +tipo: str
        +usuario_nome: str
        +usuario_email: str
        +data_emprestimo: date
        +data_devolucao: date
        +devolvido: bool
    }

    IRepositorioEmprestimo <|.. RepositorioEmprestimo
    INotificador <|.. Notificador
    ServicoEmprestimo --> IRepositorioEmprestimo : usa
    ServicoEmprestimo --> INotificador : usa
    RepositorioEmprestimo o-- Equipamento : equipamentos
    RepositorioEmprestimo o-- Emprestimo : emprestimos
    Emprestimo --> Equipamento : referencia
    Equipamento <|-- Notebook
    Equipamento <|-- Projetor
    Equipamento <|-- CaboHDMI
```

---

## Diagramas de sequência

### UC01 — Registrar Empréstimo

<!-- ![alt text](image.png) -->

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

<!-- ![alt text](image-1.png) -->

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

<!-- ![alt text](image-2.png) -->

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
