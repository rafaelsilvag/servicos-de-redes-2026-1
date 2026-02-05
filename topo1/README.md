# Topologia de Rede: 2 Hosts e 1 Roteador

## 1. Diagramas Visuais

### Diagrama

Este diagrama representa as conexões lógicas e físicas entre os dispositivos.

```mermaid
graph LR
    %% Definição dos Nós
    h1[Host: h1]
    r1((Roteador: r1))
    h2[Host: h2]

    %% Definição das Conexões com rótulos das portas
    %% h1 ethernet1 <-> r1 ethernet1
    h1 -- "eth1 ↔ eth1" --- r1

    %% r1 ethernet2 <-> h2 ethernet1
    r1 -- "eth2 ↔ eth1" --- h2

    %% Estilização visual (opcional)
    style r1 fill:#ff9,stroke:#333,stroke-width:2px
    style h1 fill:#dff,stroke:#333
    style h2 fill:#dff,stroke:#333
