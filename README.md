# Download Material Educador

Este projeto é uma coleção de scripts para baixar, otimizar e organizar materiais educacionais da editora "Formando Cidadãos".

## Descrição

O objetivo principal deste projeto é automatizar o processo de download de materiais didáticos, como manuais e catálogos, e organizá-los de forma estruturada para fácil acesso e utilização.

## Funcionalidades

- **Download Automatizado:** Scripts para baixar conteúdo diretamente do portal "Formando Cidadãos".
- **Otimização de Arquivos:** Scripts para otimizar os arquivos baixados (provavelmente PDFs).
- **Organização de Materiais:** Scripts para renomear, limpar e organizar os materiais em uma estrutura de pastas lógica, seja por matéria ou por kit.

## Estrutura do Projeto

```text
.
├── automation_download/  # Scripts para download de materiais
│   ├── script.py
│   └── script_async.py
├── files/                # Arquivos baixados e catálogos
│   ├── Catalogo_2026.pdf
│   └── ...
├── optimizer/            # Scripts para otimização de arquivos
│   ├── otimizador.py
│   └── otimizadorv2.py
├── sanitaze_and_organize/ # Scripts para limpeza e organização
│   ├── organizador.py
│   ├── organize_pdfs.py
│   └── sanitize_manuais_pdfs.bat
├── .gitignore
├── task_organize_by_kit.md     # Descrição da tarefa de organização por kit
└── task_organize_by_subject.md # Descrição da tarefa de organização por matéria
```

## Como Usar

1. **Download:** Execute os scripts em `automation_download/` para baixar os materiais. Pode ser necessário ajustar os scripts para lidar com logins ou alterações na estrutura do site.
2. **Otimização:** Utilize os scripts em `optimizer/` para processar e otimizar os arquivos baixados.
3. **Organização:** Rode os scripts em `sanitaze_and_organize/` para arrumar os arquivos em uma estrutura de pastas limpa.

## Dependências

Este projeto utiliza principalmente Python. As dependências exatas podem ser encontradas no início de cada script (`.py`). As bibliotecas comuns para este tipo de projeto são:

- `requests`
- `BeautifulSoup4`
- `PyPDF2`
- `selenium`

Certifique-se de instalar as bibliotecas necessárias antes de executar os scripts.

```bash
pip install -r requirements.txt
```
