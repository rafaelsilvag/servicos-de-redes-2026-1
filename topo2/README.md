# Documentação de Topologia de Rede Linear (3 Roteadores e 2 hosts)

## Visão Geral

Este documento detalha uma topologia de rede linear onde dois hosts terminais (`h1` e `h2`) estão conectados através de uma cadeia de três roteadores intermediários (`r1`, `r2` e `r3`). Esta configuração cria quatro segmentos de rede distintos.

## Diagrama da Topologia (Mermaid)

O diagrama abaixo ilustra as conexões físicas exatas entre as portas dos dispositivos.

```mermaid
graph LR
    %% Definição dos Nós
    h1[Host: h1]
    r1((Roteador: r1))
    r2((Roteador: r2))
    r3((Roteador: r3))
    h2[Host: h2]

    %% Definição das Conexões com rótulos das portas
    %% h1 ethernet1 <-> r1 ethernet1
    h1 -- "eth1 ↔ eth1" --- r1

    %% r1 ethernet2 <-> r2 ethernet1
    r1 -- "eth2 ↔ eth1" --- r2

    %% r2 ethernet2 <-> r3 ethernet1
    r2 -- "eth2 ↔ eth1" --- r3

    %% r3 ethernet2 <-> h2 ethernet1
    r3 -- "eth2 ↔ eth1" --- h2

    %% Estilização visual (opcional)
    style r1 fill:#ff9,stroke:#333,stroke-width:2px
    style r2 fill:#ff9,stroke:#333,stroke-width:2px
    style r3 fill:#ff9,stroke:#333,stroke-width:2px
    style h1 fill:#dff,stroke:#333
    style h2 fill:#dff,stroke:#333
