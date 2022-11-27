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

# Run Containers Locally to Test

To run all containers locally, I sugest use host network with each container
using a different TCP port. Also sugest create .env files with all environment
variables used. All these values are used as example, do not reuse any of them.
Remember, to build each image you must to be in the right directory.
```bash
echo "
MYSQL_ROOT_PASSWORD=my-secret-pw
MYSQL_USER=passwordappuser 
MYSQL_PASSWORD=Iu7MPxYB9FM63EUkb1GkGpSWIbZDVwcwA 
MYSQL_ROOT_PASSWORD=mZ5Nh3X0v0SuuBtHD4ZPOAuTXVM6K4hV9 
MYSQL_DATABASE=passworddados
" > mysql.env
echo "
CONTAINER_ATUALIZAR=localhost
CONTAINER_LISTAR=localhost
PONTUACAO=@#$%()[]<>
GERADOR_PASS_PORT=8087
ATUALIZAR_PASS_PORT=8088
LISTAR_PASS_PORT=8089
DATABASE_HOST=localhost
MYSQL_USER=passwordappuser
MYSQL_PASSWORD=Iu7MPxYB9FM63EUkb1GkGpSWIbZDVwcwA
MYSQL_DATABASE=passworddados
" > container.env

docker container run --name password-mysql -d \
  --network host \
  --env-file mysql.env
  mysql

cd ../password-gerador-pass
docker build --tag=password-gerador-pass:latest .
docker container run --name password-gerador-pass -d \
  --network host \
  --env-file container.env \
  password-gerador-pass:latest

cd ../password-listar-pass
docker build --tag=password-listar-pass:latest .
docker container run --name password-listar-pass -d \
  --network host \
  --env-file container.env \
  password-listar-pass:latest

cd ../password-atualizar-pass
docker build --tag=password-atualizar-pass:latest .
docker container run --name password-atualizar-pass -d \
  --network host \
  --env-file container.env \
  password-atualizar-pass:latest
```

To erase all created resources:
```bash
docker container rm --force password-mysql
docker container rm --force password-gerador-pass
docker container rm --force password-listar-pass
docker container rm --force password-atualizar-pass
docker image rm --force password-gerador-pass
docker image rm --force password-listar-pass
docker image rm --force password-atualizar-pass
rm -f mysql.env container.env
```