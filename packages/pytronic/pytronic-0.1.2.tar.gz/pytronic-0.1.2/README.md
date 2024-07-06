# Pytronic Framework 🤖

**Pytronic** é um framework de automação robusto, projetado para executar processos repetitivos com eficiência e confiabilidade, utilizando persistência de dados e tentativas automáticas. Ideal para qualquer tipo de automação RPA.

## Tecnologias Utilizadas 🚀

- **Python** ^3.12
- **Blue** (formatação de código)
- **Pytest** (testes)
- **Taskipy** (gerenciamento de tarefas)
- **PyAutoGUI** (automação de interface gráfica)
- **SQLmodel** (mapeamento objeto-relacional)

## Requisitos 📋

- Python 3.12 ou superior
- Poetry

## Documentação de Desenvolvimento 💻

### 1. Instale o Poetry
Se você ainda não tem o Poetry instalado, siga as instruções [aqui](https://python-poetry.org/docs/#installation) para instalar.

### 2. Clone o Repositório 🧩
```sh
git clone https://github.com/seu-usuario/pytronic.git
cd pytronic
```

### 3. Instale as Dependências 📦
```sh
poetry install
```

### 4. Ative o Ambiente Virtual do Poetry 🌟
Para facilitar o uso dos comandos do Taskipy, ative o ambiente virtual do Poetry:
```sh
poetry shell
```
💡 **Dica:** Se você não ativar o `poetry shell`, será necessário prefixar os comandos do Taskipy com `poetry run`. Por exemplo: `poetry run task lint`.

### 5. Rodando as Tarefas 🔧
#### Comandos de Desenvolvimento (`task`)
Os comandos `task` são específicos para o desenvolvimento do pacote e ajudam a manter a qualidade e a consistência do código.

- **Linting:** Verifica a formatação do código
    ```sh
    task lint
    ```

- **Testes:** Executa os testes
    ```sh
    task test
    ```

- **Pipeline:** Executa linting e testes
    ```sh
    task pipeline
    ```

### Comandos de Uso do Framework (`pytronic`)
Os comandos `pytronic` são usados para interagir com o framework Pytronic, permitindo inicializar projetos, criar bots e executá-los.

#### Comando `start`
Inicializa a estrutura básica do projeto:
```sh
pytronic start
```
- **O que faz:** Cria a pasta `bots` e adiciona um bot de exemplo.
- **Exemplo de uso:**
    ```sh
    pytronic start
    ```

#### Comando `createbot`
Cria um novo bot com o nome especificado:
```sh
pytronic createbot --name ExampleBot
```
- **O que faz:** Gera automaticamente a estrutura de diretórios e arquivos necessários, utilizando templates.
- **Exemplo de uso:**
    ```sh
    pytronic createbot --name ExampleBot
    ```
    ```sh
    pytronic createbot ExampleBot
    ```

#### Comando `run`
Executa um bot especificado, identificando a classe do bot pelo nome da pasta e carregando a tarefa a ser executada:
```sh
pytronic run --bot ExampleBot --task '{"key": "value"}'
```
- **O que faz:** Carrega o bot correspondente pelo nome da pasta e executa a tarefa dinamicamente. Se a opção `--task` não for informada, o comando carrega a tarefa do arquivo `task.json` dentro da pasta do bot criado.
- **Exemplos de uso:**
    ```sh
    pytronic run --bot ExampleBot --task '{"key": "value"}'
    ```
    ```sh
    pytronic run --bot ExampleBot --task /caminho/para/task.json
    ```
    ```sh
    pytronic run ExampleBot --task '{"key": "value"}'
    ```
    ```sh
    pytronic run ExampleBot
    ```

## Integração Contínua com GitHub Actions ⚙️
O projeto Pytronic utiliza GitHub Actions para automação do pipeline de linting e testes. Toda vez que uma nova branch é criada ou um pull request é aberto, a pipeline é executada para garantir a qualidade do código. As etapas incluem:

1. **Linting:** Verifica a formatação do código para garantir a conformidade com os padrões estabelecidos.
2. **Testes:** Executa a suíte de testes para assegurar que todas as funcionalidades estão funcionando conforme esperado.

Além disso, sempre que novos commits são sincronizados com uma branch que já possui um pull request aberto, a pipeline é acionada novamente. Isso garante que todas as alterações submetidas passam pelas verificações de qualidade.

## Suporte 🌐
Este projeto pode ser executado tanto no Linux quanto no Windows. Atenção: Implementações que utilizam o PyAutoGUI só funcionarão em ambientes que tenham uma interface gráfica (que renderize um desktop no monitor). Caso contrário, o PyAutoGUI não funcionará. Se você encontrar algum problema, sinta-se à vontade para abrir uma issue no repositório.
