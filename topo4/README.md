# Documentação da Topologia 4 (Alterada)

## Visão Geral

Este documento detalha a topologia de rede com 9 roteadores (correspondentes a cidades do Brasil) e 4 hosts conectados em pontos específicos, totalizando 13 dispositivos.

### Roteadores e Cidades correspondentes:
- `r1`: Vitória
- `r2`: Salvador
- `r3`: Rio de Janeiro
- `r4`: Belo Horizonte
- `r5`: Brasília
- `r6`: São Paulo
- `r7`: Fortaleza
- `r8`: Curitiba
- `r9`: Aracaju

### Hosts:
- `h1`: Conectado em Vitória (`r1`)
- `h2`: Conectado em Brasília (`r5`)
- `h3`: Conectado em Aracaju (`r9`)
- `h4`: Conectado em Curitiba (`r8`)

## Portas Utilizadas

### Acesso Remoto (Telnet)
As conexões Telnet são direcionadas para a interface VRF de cada dispositivo da seguinte forma:
- Roteadores: Porta `1000X`, onde `X` é o número do roteador. Exemplo: `r1` é porta `10001`, `r9` é porta `10009`.
- Hosts: Porta `2000Y`, onde `Y` é o número do host. Exemplo: `h1` é porta `20001`.

## Diagrama da Topologia (Mermaid)

O diagrama abaixo ilustra as conexões físicas exatas entre as portas dos dispositivos.

```mermaid
graph LR
    %% Definição dos Hosts
    h1[Host: h1<br>Vitória]
    h2[Host: h2<br>Brasília]
    h3[Host: h3<br>Aracaju]
    h4[Host: h4<br>Curitiba]

    %% Definição dos Roteadores
    r1((r1<br>Vitória))
    r2((r2<br>Salvador))
    r3((r3<br>Rio de Janeiro))
    r4((r4<br>Belo Horizonte))
    r5((r5<br>Brasília))
    r6((r6<br>São Paulo))
    r7((r7<br>Fortaleza))
    r8((r8<br>Curitiba))
    r9((r9<br>Aracaju))

    %% Conexões r1
    r1 -- "eth1 ↔ eth1" --- r2
    r1 -- "eth2 ↔ eth1" --- r3
    r1 -- "eth3 ↔ eth1" --- h1

    %% Conexões r2
    r2 -- "eth2 ↔ eth1" --- r9
    r2 -- "eth3 ↔ eth1" --- r4

    %% Conexões r3
    r3 -- "eth2 ↔ eth2" --- r4
    r3 -- "eth3 ↔ eth1" --- r5
    r3 -- "eth4 ↔ eth1" --- r6

    %% Conexões r4
    r4 -- "eth3 ↔ eth2" --- r6

    %% Conexões r5
    r5 -- "eth2 ↔ eth3" --- r6
    r5 -- "eth3 ↔ eth1" --- h2

    %% Conexões r6
    r6 -- "eth4 ↔ eth1" --- r8
    r6 -- "eth5 ↔ eth1" --- r7

    %% Conexões r8
    r8 -- "eth2 ↔ eth1" --- h4

    %% Conexões r9
    r9 -- "eth2 ↔ eth1" --- h3

    %% Estilização visual
    style r1 fill:#ff9,stroke:#333,stroke-width:2px
    style r2 fill:#ff9,stroke:#333,stroke-width:2px
    style r3 fill:#ff9,stroke:#333,stroke-width:2px
    style r4 fill:#ff9,stroke:#333,stroke-width:2px
    style r5 fill:#ff9,stroke:#333,stroke-width:2px
    style r6 fill:#ff9,stroke:#333,stroke-width:2px
    style r7 fill:#ff9,stroke:#333,stroke-width:2px
    style r8 fill:#ff9,stroke:#333,stroke-width:2px
    style r9 fill:#ff9,stroke:#333,stroke-width:2px

    style h1 fill:#dff,stroke:#333
    style h2 fill:#dff,stroke:#333
    style h3 fill:#dff,stroke:#333
    style h4 fill:#dff,stroke:#333
```
