# Simplificando o Acesso ao Material Didático "Formando Cidadãos"

Este projeto automatiza o acesso e a organização dos materiais educacionais da editora "Formando Cidadãos", tornando a vida de professores, coordenadores e diretores mais fácil.

## O Desafio do Acesso Digital

O portal oficial da "Formando Cidadãos", embora completo, pode ser um labirinto digital para educadores com conhecimento técnico limitado. A dificuldade em navegar, encontrar e baixar os materiais corretos gera frustração e desperdiça um tempo precioso que poderia ser usado no que realmente importa: a educação.

## A Solução: Automação e Organização em 4 Passos

Este repositório oferece uma solução completa para eliminar essa dor de cabeça. Com uma série de scripts inteligentes, transformamos o processo manual e complicado em uma tarefa simples e automatizada.

### Como Funciona?

1. **Download Automático:** O robô em `automation_download/` acessa o portal e baixa todos os documentos necessários em formato PDF, sem que você precise clicar em dezenas de links.

2. **Organização Inteligente por Kits:** Usando uma tarefa de Inteligência Artificial (descrita em `ai/`), os materiais são automaticamente organizados em pastas separadas por "Kit" (Kit A, Kit B, etc.), seguindo a estrutura do **Catálogo 2026**. Chega de adivinhar qual arquivo pertence a qual coleção!

3. **Otimização para a Nuvem:** Os scripts em `optimizer/` comprimem e otimizam os PDFs, reduzindo o tamanho dos arquivos para facilitar o compartilhamento e o armazenamento em serviços de nuvem como Google Drive ou Dropbox.

4. **Compartilhamento Fácil:** Ao final do processo, você terá um link único para a pasta na nuvem com todo o material organizado, pronto para ser compartilhado via WhatsApp ou qualquer outro meio de comunicação.

## Como Usar

1. **Configuração do Ambiente:**
    Para garantir que o ambiente virtual (`venv`) esteja configurado e as dependências instaladas, execute o script `check_env.ps1` no PowerShell:

    ```powershell
    .\check_env.ps1
    ```

    Este comando criará o ambiente virtual se ele não existir, o ativará e instalará as bibliotecas necessárias a partir do `requirements.txt`.

2. **Execução dos Passos:**
    Siga a ordem dos scripts nas pastas `automation_download/`, `optimizer/` e `sanitaze_and_organize/` para executar o fluxo completo.

## Estrutura do Projeto

```text
.
├── ai/                     # Tarefas e prompts para IA (Inteligência Artificial)
├── automation_download/    # Scripts para download de materiais
├── files/                  # Arquivos de referência, como o catálogo
├── optimizer/              # Scripts para otimização de arquivos
├── sanitaze_and_organize/  # Scripts para limpeza e organização final
├── venv/                   # Ambiente virtual Python
├── .gitignore
├── check_env.ps1           # Script para configurar o ambiente
├── README.md
└── requirements.txt        # Lista de dependências Python
```

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

```text
selenium
requests
beautifulsoup4
PyPDF2
fitz
```
