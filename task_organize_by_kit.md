# CONTEXTO

Atue como Especialista em Engenharia de Dados e Desenvolvedor Python Sênior. Sua tarefa é criar um script de automação para organizar 991 arquivos PDF de uma editora escolar (Formando Cidadãos) no Windows.

## INPUTS

- Local dos arquivos: `./manuais_otimizados`
- Fonte de metadados: `./Catalogo_2026.pdf` (Contém a relação oficial de coleções/séries)
- Lista de arquivos: Gerada via `ls ./manuais_otimizados > lista_arquivos.txt`

## REGRAS DE NEGÓCIO PARA CLASSIFICAÇÃO

O script deve ler 'lista_arquivos.txt' e classificar cada item seguindo esta hierarquia:

1. IDENTIFICAÇÃO DE SÉRIE (Nível 1):
   Extrair do nome (ex: "1 Ano", "2 Anos", "Educação Infantil").
2. CATEGORIZAÇÃO POR KIT (Nível 2):
   - KIT A: Linguagem, Matemática, Natureza e Sociedade, Língua Portuguesa, Gramática, História, Geografia, Ciências, Cidadania Moral e Ética.
   - KIT B: Caligrafia, Tabuada, Arte, Inglês, Atividades de Desenho, Atividades Lúdicas.
   - KIT C: Trabalhando com a Literatura, Atividades de Reforço, Oficina de Negócios, Produção de Texto.
   - COMPLEMENTARES: Se o nome contiver "Manual do Educador", "Formação Continuada" ou "Guia do Professor".

## REQUISITOS DO SCRIPT PYTHON

Desenvolva um script `organizador.py` que:

1. Valide a existência da pasta de origem.
2. Utilize Expressões Regulares (RegEx) para identificar as palavras-chave dos Kits no nome dos arquivos.
3. Crie a estrutura de diretórios automaticamente usando `os.makedirs(exist_ok=True)`.
4. Mova os arquivos seguindo o padrão: `./saida/[SERIE]/[KIT]/[NOME_DO_ARQUIVO]`.
5. Gere um log simples (`organizacao.log`) de arquivos que não puderam ser classificados (Exceções).

## TAREFA

Forneça o código Python completo, comentado, e pronto para execução no terminal Windows.
