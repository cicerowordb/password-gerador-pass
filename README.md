# GERADOR PASS
This component is part of a set of applications according to following diagram:

```
                          ┌───────────┐
                     ┌───►│LISTAR-PASS├────┐
                     │    └───────────┘    │
                     │                     ▼
 ┌────────┐    ┌─────┴──────┐          ┌────────┐
 │INTERNET├───►│GERADOR-PASS├─────────►│DATABASE│
 └────────┘    └─────┬──────┘          └────────┘
                     │                     ▲
                     │   ┌──────────────┐  │
                     └──►│ATUALIZAR-PASS├──┘
                         └──────────────┘
```

All external requests are processed by password_gen and:
- a new password can be created and inserted in database;
- a existing password can be updated in database by **atualizar**;
- all passwords can be recovered in database and listed by **list_data_base**.

Database component is a common MySQL database.

# Requirements
- Python3 and Pyton3-pip
- flask, requests and mysql-connector-python libraries

# Environment Variables

- **CONTAINER_ATUALIZAR**:
- **CONTAINER_LISTAR**:
- **GERADOR_PASS_PORT**:
- **ATUALIZAR_PASS_PORT**:
- **LISTAR_PASS_PORT**:
- **DATABASE_HOST**:
- **MYSQL_USER**: 
- **MYSQL_PASSWORD**: 
- **MYSQL_DATABASE**: 
- **PONTUACAO**: '@#$%()[]<>'

# GitHub Secrets
- AWS_ACCESS_KEY_ID: key to use Amanzon ERC image repository
- AWS_SECRET_ACCESS_KEY: secret to use Amanzon ERC image repository
- MANIFESTS_REPOSITORY: URL (with credentials) to clone manifests repository


