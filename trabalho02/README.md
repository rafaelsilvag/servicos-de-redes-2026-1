# Atividade Prática: Orquestração de Containers em Cluster

## Disciplina
**Serviços de Redes para Internet**

## Modalidade
Atividade em **dupla** ou **trio**

## Valor
**30,0 pontos**

| Critério | Peso | Pontos |
| :--- | :--- | :--- |
| Entrevista técnica em sala (03/07/2026) | 80% | 24,0 |
| Entrega do repositório e implementação funcional | 20% | 6,0 |

---

## Contexto

Esta atividade é uma evolução direta do **Trabalho 01**, no qual cada grupo implementou uma aplicação web conteinerizada com Docker Compose (NGINX + FastAPI + PostgreSQL). Agora, os grupos deverão **portar e adaptar** essa mesma aplicação para rodar em um **orquestrador de containers em cluster com múltiplas VMs**, expandindo a topologia com um serviço adicional de coleta de logs e impondo restrições de posicionamento que separam a camada de dados da camada de aplicação.

O objetivo é que os alunos compreendam na prática os seguintes conceitos:

- Diferença entre orquestração local (Compose) e orquestração distribuída em cluster;
- Redes overlay e descoberta de serviços entre hosts;
- Isolamento por camada usando restrições de nó (*placement constraints* / *node selectors*);
- Observabilidade: coleta e consulta centralizada de logs de containers.

---

## Ferramentas e Distribuição dos Grupos

> Todas as ferramentas abaixo são **100% gratuitas, open source** e **não requerem cadastro nem licença** para uso local ou em laboratório.

| Grupo | Orquestrador | Licença | Observação |
| :--- | :--- | :--- | :--- |
| **Grupo 1** | Docker Swarm | Apache 2.0 (incluso no Docker Engine) | Nativo no Docker, sem instalação adicional |
| **Grupo 2** | K3s | Apache 2.0 (Rancher/SUSE) | Kubernetes leve para uso local e edge |
| **Grupo 3** | uncloud | Apache 2.0 | Orquestrador minimalista open source |
| **Grupo 4** | Docker Swarm | Apache 2.0 (incluso no Docker Engine) | Nativo no Docker, sem instalação adicional |
| **Grupo 5** | K3s | Apache 2.0 (Rancher/SUSE) | Kubernetes leve para uso local e edge |
| **Grupo 6** | uncloud | Apache 2.0 | Orquestrador minimalista open source |
| **Grupo 7** | Docker Swarm | Apache 2.0 (incluso no Docker Engine) | Nativo no Docker, sem instalação adicional |
| **Grupo 8** | K3s | Apache 2.0 (Rancher/SUSE) | Kubernetes leve para uso local e edge |

---

## Temas dos Grupos (herdados do Trabalho 01)

Cada grupo mantém o mesmo tema do Trabalho 01 e deverá portar a aplicação já implementada para o novo orquestrador.

| Grupo | Tema | Entidades |
| :--- | :--- | :--- |
| **Grupo 1** | Sistema de Cadastro de Usuários e Perfis | usuários, perfis |
| **Grupo 2** | Catálogo de Produtos e Categorias | produtos, categorias |
| **Grupo 3** | Sistema de Biblioteca | livros, autores |
| **Grupo 4** | Controle de Alunos e Cursos | alunos, cursos |
| **Grupo 5** | Sistema de Agendamentos | clientes, agendamentos |
| **Grupo 6** | Controle de Pedidos | pedidos, itens_pedido |
| **Grupo 7** | Sistema de Filmes e Avaliações | filmes, avaliacoes |
| **Grupo 8** | Controle de Tarefas e Projetos | tarefas, projetos |

---

## Topologia do Cluster

Todos os grupos devem implantar a aplicação em um cluster formado por **no mínimo 2 VMs**, com a seguinte separação obrigatória de camadas:

```
┌──────────────────────────────────┐      ┌──────────────────────────────────┐
│       VM1  —  Camada de Dados    │      │    VM2  —  Camada de Aplicação   │
│                                  │      │                                  │
│   ┌────────────┐  ┌───────────┐  │      │  ┌─────────┐   ┌─────────────┐  │
│   │ PostgreSQL │  │   Loki    │  │      │  │  NGINX  │   │   FastAPI   │  │
│   │  porta     │  │  porta    │  │      │  │porta 80 │   │  porta 8080 │  │
│   │  5432      │  │  3100     │  │      │  │  / 443  │   │  (interno)  │  │
│   └────────────┘  └───────────┘  │      │  └─────────┘   └─────────────┘  │
│                                  │      │                                  │
│   (sem portas expostas ao host)  │      │   (NGINX exposto ao host)        │
└──────────────┬───────────────────┘      └──────────────┬───────────────────┘
               │                                         │
               └──────────── rede interna do cluster ────┘
                          (overlay / cluster network)
```

### Regras de posicionamento obrigatórias

| Serviço | VM obrigatória | Justificativa |
| :--- | :--- | :--- |
| PostgreSQL | VM1 (dados) | Dados persistentes ficam em nó fixo |
| Loki | VM1 (dados) | Serviço de infraestrutura junto aos dados |
| NGINX | VM2 (aplicação) | Único ponto de entrada, na VM da aplicação |
| FastAPI | VM2 (aplicação) | Backend junto ao ponto de entrada |

Cada orquestrador impõe essas restrições de forma diferente — veja a seção específica do seu grupo.

---

## Serviço Adicional: Loki (Coleta de Logs)

Todos os grupos devem adicionar o **Grafana Loki** como serviço de agregação centralizada de logs, implantado na **VM1** junto ao PostgreSQL.

> **Loki** é 100% gratuito, open source (Apache 2.0) e não requer cadastro.  
> Imagem oficial: `grafana/loki:3.0.0`

O Loki recebe logs via sua API HTTP (porta 3100) e os armazena para consulta. O FastAPI deve enviar ao Loki ao menos os seguintes eventos:
- Inicialização da aplicação.
- Cada requisição recebida (método HTTP, rota, código de resposta).
- Erros de conexão com o PostgreSQL.

### Configuração mínima do Loki

Criar o arquivo `loki/loki-config.yaml` no repositório com o seguinte conteúdo:

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  instance_addr: 127.0.0.1
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h
```

### Como enviar logs ao Loki

O FastAPI deve realizar requisições `POST` ao endpoint `/loki/api/v1/push` do Loki com o payload no formato JSON esperado pela [Loki Push API](https://grafana.com/docs/loki/latest/reference/loki-http-api/#ingest-logs). Recomenda-se criar um módulo `logger.py` no backend responsável por essa integração.

### Como consultar os logs

A API do Loki pode ser consultada diretamente via HTTP, sem necessidade de interface gráfica:

```bash
# Listar todos os labels disponíveis
curl http://<IP-VM1>:3100/loki/api/v1/labels

# Consultar logs do serviço fastapi dos últimos 10 minutos
curl -G 'http://<IP-VM1>:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={service="fastapi"}' \
  --data-urlencode 'start='"$(date -d '10 minutes ago' +%s000000000)"'' \
  --data-urlencode 'end='"$(date +%s000000000)"''
```

Durante a entrevista, o grupo deve demonstrar uma consulta de logs diretamente pela API HTTP do Loki, sem interface gráfica.

> **Desafio extra:** Adicionar o **Grafana** (imagem `grafana/grafana:latest`, gratuita) como serviço na VM2 para visualizar os logs do Loki via interface web.

---

## Objetivos por Orquestrador

### Docker Swarm (Grupos 1, 4 e 7)

O Docker Swarm é o orquestrador nativo do Docker Engine. Com ele é possível criar um cluster de nós (managers e workers) e implantar serviços distribuídos usando arquivos de Stack Compose.

**Infraestrutura mínima:**

| Nó | Papel no Swarm | Serviços |
| :--- | :--- | :--- |
| VM1 | Worker | PostgreSQL, Loki |
| VM2 | Manager | NGINX, FastAPI |

**Requisitos específicos:**

- Inicializar o Swarm e ingressar ambas as VMs no cluster.
- Rotular os nós para distinguir a camada de dados da camada de aplicação.
- Implantar a aplicação como uma **Stack** a partir de um arquivo de configuração compatível com o formato Swarm.
- Utilizar rede **overlay** para comunicação entre os serviços.
- Configurar **placement constraints** baseadas nos labels dos nós para fixar cada serviço à VM correta.
- NGINX e FastAPI com mínimo de 2 réplicas cada, fixadas na VM2.
- PostgreSQL e Loki com 1 réplica cada, fixados na VM1.
- Utilizar **secrets** do Swarm para a senha do banco de dados.

---

### K3s (Grupos 2, 5 e 8)

O K3s é uma distribuição leve de Kubernetes, projetada para ambientes com recursos limitados, edge computing e laboratório. Oferece a API completa do Kubernetes sem a complexidade da instalação padrão.

**Infraestrutura mínima:**

| Nó | Papel no K3s | Serviços |
| :--- | :--- | :--- |
| VM1 | Agent (worker) | PostgreSQL, Loki |
| VM2 | Server (control plane + worker) | NGINX, FastAPI |

**Requisitos específicos:**

- Instalar o K3s e adicionar ambas as VMs ao cluster (server + agent).
- Rotular os nós para distinguir a camada de dados da camada de aplicação.
- Implantar a aplicação com **manifests YAML** do Kubernetes organizados em um diretório `k8s/`.
- Usar `nodeSelector` em todos os manifests para fixar cada serviço ao nó correto.
- Recursos obrigatórios:
  - `Deployment` para NGINX e FastAPI (mínimo 2 réplicas cada, fixadas na VM2).
  - `StatefulSet` para PostgreSQL (1 réplica, fixado na VM1).
  - `Deployment` para Loki (1 réplica, fixado na VM1).
  - `Service` do tipo `ClusterIP` para FastAPI, PostgreSQL e Loki.
  - `Service` do tipo `NodePort` para NGINX (exposto ao host na VM2).
  - `PersistentVolumeClaim` para PostgreSQL e para os dados do Loki.
  - `Secret` para credenciais do banco.
  - `ConfigMap` para configuração do NGINX e do Loki.

---

### uncloud (Grupos 3 e 6)

O uncloud é um orquestrador de containers open source minimalista, projetado para ser simples de operar em servidores próprios (self-hosted) sem a complexidade do Kubernetes. Ele gerencia containers em múltiplos hosts de forma declarativa.

**Repositório oficial:** https://github.com/psviderski/uncloud

**Infraestrutura mínima:**

| Máquina | Serviços |
| :--- | :--- |
| VM1 (dados) | PostgreSQL, Loki |
| VM2 (aplicação) | NGINX, FastAPI |

**Requisitos específicos:**

- Instalar o `uncloud` CLI seguindo a documentação oficial.
- Adicionar as duas VMs ao cluster como máquinas gerenciadas.
- Implantar cada serviço especificando a máquina de destino para garantir a separação de camadas.
- Configurar o Loki na VM1 com arquivo de configuração próprio mapeado via volume.
- Utilizar volume persistente para PostgreSQL e para os dados do Loki.
- Publicar o serviço NGINX para acesso externo apenas na VM2.
- Documentar no README do grupo todos os comandos utilizados para deploy e verificação de estado.

---

## Requisitos Comuns a Todos os Grupos

### 1. Infraestrutura mínima de VMs

- O cluster deve ser composto por **no mínimo 2 VMs**.
- A separação de camadas é **obrigatória**:
  - **VM1 (dados):** PostgreSQL + Loki.
  - **VM2 (aplicação):** NGINX + FastAPI.
- As VMs podem ser criadas localmente com VirtualBox, QEMU/KVM, Vagrant ou qualquer ferramenta de virtualização gratuita. Também é aceito o uso de instâncias cloud com camada gratuita (ex: Oracle Cloud Free Tier, Google Cloud Free Tier).
- Ambas as VMs devem estar na mesma rede local ou VPN para que o cluster funcione.

### 2. Aplicação

- Manter a mesma funcionalidade do Trabalho 01 (NGINX + FastAPI + PostgreSQL com CRUD completo).
- Os `Dockerfile`s podem ser reaproveitados do Trabalho 01.
- As imagens devem ser publicadas no **Docker Hub** (conta gratuita, sem necessidade de login para `pull`) ou construídas localmente e documentadas.

### 3. Serviço de logs (Loki)

- O Loki **é obrigatório** e deve rodar na VM1.
- O FastAPI deve enviar logs estruturados ao Loki (ao menos: inicialização, requisições recebidas e erros).
- Durante a entrevista, o grupo deve demonstrar uma consulta de logs via API HTTP do Loki.

### 4. Persistência

- PostgreSQL e Loki devem persistir dados mesmo após reiniciar os containers/pods.
- O volume do PostgreSQL deve estar fixado na VM1 (não pode migrar para outra VM).

### 5. Rede

- Apenas o NGINX deve ser acessível diretamente do host externo (portas 80 e 443).
- PostgreSQL, Loki e FastAPI devem ser acessíveis apenas pela rede interna do cluster.
- Durante a entrevista, o grupo deve demonstrar que as portas internas dos serviços de dados não estão acessíveis de fora do cluster.

### 6. Credenciais

- A senha do banco deve ser gerenciada pelo mecanismo de segredo nativo do orquestrador:
  - **Docker Swarm:** secrets do Swarm
  - **K3s:** Secret do Kubernetes
  - **uncloud:** mecanismo equivalente conforme documentado

### 7. Repositório no GitHub

O repositório deverá conter, no mínimo:

```text
nome-do-projeto/
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── database.py
│       ├── logger.py          ← novo: cliente HTTP para envio de logs ao Loki
│       ├── routes/
│       └── schemas/
├── nginx/
│   ├── nginx.conf
│   └── html/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── loki/
│   └── loki-config.yaml
└── [pasta do orquestrador]/   # docker-stack/  |  k8s/  |  uncloud/
    └── [arquivos de configuração]
```

O `README.md` do grupo deve conter:
- Descrição do projeto e do orquestrador utilizado.
- Integrantes do grupo.
- Diagrama da topologia do cluster (VMs, serviços e rede).
- Instruções completas para provisionar as VMs, inicializar o cluster e implantar a aplicação.
- Comandos para verificar o estado dos serviços e consultar logs no Loki.

---

## Entrega

Cada grupo deverá entregar até **03/07/2026 (antes da entrevista)**:

1. **Link do repositório GitHub** (enviar ao professor pelo canal definido em aula).
2. Aplicação **funcionando** no cluster com 2 VMs, pronta para demonstração em sala.
3. Presença na **entrevista técnica** no dia **07/07/2026**.

---

## Sugestão de desafio extra

Os itens abaixo não substituem os requisitos obrigatórios, mas podem ser considerados positivamente em casos limítrofes:

- **Docker Swarm:** Demonstrar *failover* removendo um nó worker e acompanhando o reagendamento de réplicas.
- **K3s:** Configurar um `Ingress` com Traefik (já incluso no K3s) no lugar do `NodePort`.
- **uncloud:** Adicionar uma terceira VM ao cluster e redistribuir serviços.
- **Qualquer grupo:** Adicionar o **Grafana** (porta 3000) como interface visual para os logs do Loki.
- **Qualquer grupo:** Configurar `healthcheck` para o FastAPI no orquestrador, reiniciando automaticamente pods/tarefas com falha de saúde.

---

## Datas importantes

| Evento | Data |
| :--- | :--- |
| Início da atividade | 24/06/2026 |
| Entrega do repositório e entrevista | **07/07/2026** |

---
