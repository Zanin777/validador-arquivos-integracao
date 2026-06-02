# 📄 Validador de Arquivos de Integração (Texto Fixo)

## 📌 Sobre o Projeto

Este projeto consiste em um validador de arquivos de integração em formato texto (`.txt`), utilizados com frequência em sistemas bancários, ERPs e processos de troca de dados entre empresas.

Esses arquivos seguem o padrão de **texto de largura fixa (fixed-width)**, onde cada informação ocupa posições específicas dentro da linha.

O script realiza a leitura do arquivo, identifica os tipos de registros e verifica se os dados estão formatados corretamente, gerando um relatório detalhado em JSON com todos os erros encontrados.

---

## 🎯 Objetivos

O projeto foi desenvolvido para praticar:

* Manipulação de arquivos (`open`, `readlines`)
* Expressões regulares (`re`)
* Fatiamento de strings (slicing)
* Validação matemática de CNPJ
* Tratamento de exceções
* Geração de relatórios JSON
* Estruturação de lógica de validação de dados

---

## 📂 Estrutura dos Registros

### Header (Tipo 0)

Representa o cabeçalho do arquivo.

| Posição  | Tamanho | Descrição            |
| -------- | ------- | -------------------- |
| 1        | 1       | Tipo de Registro (0) |
| 2-15     | 14      | CNPJ                 |
| Restante | -       | Dados complementares |

### Detalhe (Tipo 1)

Representa um registro de movimentação.

| Posição | Tamanho | Descrição                    |
| ------- | ------- | ---------------------------- |
| 1       | 1       | Tipo de Registro (1)         |
| 12-21   | 10      | Valor                        |
| 22-29   | 8       | Data de Pagamento (DDMMAAAA) |

### Trailer (Tipo 9)

Representa o encerramento do arquivo.

| Posição | Tamanho | Descrição            |
| ------- | ------- | -------------------- |
| 1       | 1       | Tipo de Registro (9) |

---

## 🔍 Validações Implementadas

### Header

* Verifica se possui pelo menos 45 caracteres.
* Extrai o CNPJ.
* Verifica se o CNPJ possui apenas números.
* Realiza validação matemática dos dígitos verificadores.

### Detalhe

* Verifica se possui pelo menos 29 caracteres.
* Valida o campo valor.
* Valida a data no formato `DDMMAAAA`.

### Registro

* Aceita apenas os tipos:

  * `0` → Header
  * `1` → Detalhe
  * `9` → Trailer

Qualquer outro valor é considerado inválido.

---

## 🏗️ Funcionamento

### Leitura do arquivo

O sistema lê todas as linhas do arquivo informado:

```python
with open(caminho_txt, 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()
```

---

### Identificação do tipo de registro

O primeiro caractere da linha determina seu tipo:

```python
tipo_registro = linha[0]
```

---

### Validação de CNPJ

A função `validar_cnpj()`:

1. Remove caracteres não numéricos.
2. Verifica tamanho.
3. Calcula os dois dígitos verificadores.
4. Compara com os dígitos informados.

Retorna:

```python
True
```

ou

```python
False
```

---

### Tratamento de Exceções

O projeto utiliza:

```python
try
except
```

para capturar:

* Arquivo inexistente
* Linhas mal formatadas
* Campos inválidos
* Erros inesperados

---

## 📊 Relatório de Erros

Ao encontrar problemas, o sistema gera um arquivo JSON contendo:

```json
[
    {
        "linha": 5,
        "tipo_registro": "1",
        "conteudo_suspeito": "100000001234ABC01012026",
        "motivo_rejeicao": "O campo 'Valor' (ABC) deve conter apenas números."
    }
]
```

### Campos do relatório

| Campo             | Descrição                  |
| ----------------- | -------------------------- |
| linha             | Número da linha no arquivo |
| tipo_registro     | Tipo identificado          |
| conteudo_suspeito | Trecho da linha analisada  |
| motivo_rejeicao   | Motivo do erro             |

---

## 🚀 Como Executar

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/validador-integracao.git
```

### 2. Acesse a pasta

```bash
cd validador-integracao
```

### 3. Execute o script

```bash
python validador.py
```

---

## 📁 Arquivos Esperados

### Entrada

```text
remessa_teste.txt
```

### Saída

```text
relatorio_erros.json
```

---

## 📝 Exemplo de Uso

```python
if __name__ == "__main__":
    analisar_arquivo_integracao(
        "remessa_teste.txt",
        "relatorio_erros.json"
    )
```

---

## ✅ Exemplo de Saída

```text
Validação concluída. 3 erro(s) encontrado(s).
Relatório gerado em: relatorio_erros.json
```

---

## 👨‍💻 Tecnologias Utilizadas

* Python 3
* Regex (`re`)
* JSON (`json`)
* Manipulação de Arquivos
* Tratamento de Exceções

---

## 📚 Conceitos Aplicados

* Arquivos de largura fixa (Fixed Width)
* Validação de dados
* Validação de documentos brasileiros (CNPJ)
* Geração de relatórios
* Programação defensiva
* Estruturas de repetição
* Funções e modularização

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos e de aprendizado.
