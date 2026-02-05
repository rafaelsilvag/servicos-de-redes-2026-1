# Topologia de Rede: 2 Hosts e 1 Roteador

Abaixo está a documentação da topologia solicitada, incluindo diagramas visuais, descrição física e uma sugestão de configuração lógica (IP) para torná-la funcional.

## 1. Diagramas Visuais

### Diagrama

Este diagrama representa as conexões lógicas e físicas entre os dispositivos.

```mermaid
graph TR
    subgraph "Rede A (Sub-rede 1)"
        h1[Host: h1]
    end

    subgraph "Roteador Central"
        r1((Roteador: r1))
    end

    subgraph "Rede B (Sub-rede 2)"
        h2[Host: h2]
    end

    %% Conexões Físicas especificadas
    h1 -- "Cabo Ethernet" --- eth1_r1[Porta: ethernet1]
    eth1_r1 --- r1
    r1 --- eth2_r1[Porta: ethernet2]
    eth2_r1 -- "Cabo Ethernet" --- h2

    %% Estilização simples
    style r1 fill:#ff9,stroke:#333,stroke-width:2px
