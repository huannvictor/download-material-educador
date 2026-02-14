# Download Material Educador

Este projeto é uma coleção de scripts para baixar, otimizar e organizar materiais educacionais da editora "Formando Cidadãos".

## Descrição

O objetivo principal deste projeto é automatizar o processo de download de materiais didáticos, como manuais e catálogos, e organizá-los de forma estruturada para fácil acesso e utilização.

## Como Usar

1. **Configuração do Ambiente:**
    Para garantir que o ambiente virtual (`venv`) esteja configurado e as dependências instaladas, execute o script `check_env.ps1` no PowerShell:

    ```powershell
    .\check_env.ps1
    ```

    Este comando criará o ambiente virtual se ele não existir, o ativará e instalará as bibliotecas necessárias a partir do `requirements.txt`.

2. **Download:** Execute os scripts em `automation_download/` para baixar os materiais. Pode ser necessário ajustar os scripts para lidar com logins ou alterações na estrutura do site.

3. **Otimização:** Utilize os scripts em `optimizer/` para processar e otimizar os arquivos baixados.

4. **Organização:** Rode os scripts em `sanitaze_and_organize/` para arrumar os arquivos em uma estrutura de pastas limpa.

## Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`:

```text
selenium
requests
beautifulsoup4
PyPDF2
fitz
```

## Estrutura do Projeto

```text
.
├── ai/                     # Tarefas e prompts para IA
│   ├── task_organize_by_kit.md
│   └── task_organize_by_subject.md
├── automation_download/    # Scripts para download de materiais
│   ├── script.py
│   └── script_async.py
├── files/                  # Arquivos baixados e catálogos
│   ├── Catalogo_2026.pdf
│   └── ...
├── optimizer/              # Scripts para otimização de arquivos
│   ├── otimizador.py
│   └── otimizadorv2.py
├── sanitaze_and_organize/  # Scripts para limpeza e organização
│   ├── organizador.py
│   └── sanitize_manuais_pdfs.bat
├── venv/                   # Ambiente virtual Python
├── .gitignore
├── check_env.ps1           # Script para configurar o ambiente
├── README.md
└── requirements.txt        # Lista de dependências Python
```

## Tarefas de IA (Inteligência Artificial)

A pasta `ai/` contém descrições detalhadas de tarefas que podem ser executadas por um modelo de linguagem para automatizar a organização dos arquivos.

- `task_organize_by_kit.md`: Descreve a tarefa de organizar os manuais em "Kits" (A, B, C, etc.) com base em regras de negócio específicas.
- `task_organize_by_subject.md`: Descreve a tarefa de organizar os manuais por disciplina acadêmica (Matemática, Português, etc.), analisando o conteúdo dos PDFs.
