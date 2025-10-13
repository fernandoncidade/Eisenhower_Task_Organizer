<!-- Multilanguage README.md for Eisenhower_Task_Organizer -->

<p align="center">
  <b>Selecione o idioma / Select language:</b><br>
  <a href="#ptbr">🇧🇷 Português (BR)</a> |
  <a href="#enus">🇺🇸 English (US)</a>
</p>

---

## <a id="ptbr"></a>🇧🇷 Português (BR)

<details>
<summary>Clique para expandir o README em português</summary>

# EISENHOWER ORGANIZER — Organizador de Tarefas pela Matriz de Eisenhower

Versão: v0.0.0.0 — 13 de Outubro de 2025  
Autor: Fernando Nillsson Cidade

**Total de downloads acumulados:**  
![GitHub all releases](https://img.shields.io/github/downloads/fernandoncidade/Eisenhower_Task_Organizer/total?label=Downloads%20totais%20(Eisenhower%20Task%20Organizer))

## Resumo
EISENHOWER ORGANIZER é um aplicativo leve para gerenciar tarefas usando a Matriz de Eisenhower (Importante/Urgente). Permite criar tarefas, classificá-las por quadrante, marcar como concluídas (movendo automaticamente entre listas), remover itens com confirmação e exportar/importar para XLSX/PDF. Interface com suporte a Português (Brasil) e Inglês (Estados Unidos).

## Principais funcionalidades
- Adicionar tarefas rapidamente com seletor de quadrante.
- Marcar/desmarcar como concluída, movendo entre listas pendentes/concluídas.
- Remover tarefas via menu de contexto (clique direito) com confirmação.
- Salvamento automático local em tasks.json no diretório persistente do usuário.
- Exportar para XLSX e PDF (Arquivo → Salvar).
- Importar de XLSX e PDF (Arquivo → Abrir).
- Interface multilíngue: Português (Brasil) e Inglês (Estados Unidos).
- Janela “Sobre” com histórico, detalhes, avisos, licenças e política de privacidade.
- Operação offline (sem telemetria).

## Requisitos
- Windows 10 ou superior.
- Para executar a partir do código-fonte: Python 3.9+.
- Dependências: PySide6, openpyxl, reportlab, PyPDF2.

## Instalação (a partir do código-fonte Windows)
1) Criar ambiente virtual
- PowerShell:
  - py -m venv .venv
  - .\.venv\Scripts\Activate.ps1
- CMD:
  - py -m venv .venv
  - .venv\Scripts\activate

2) Instalar dependências
- pip install PySide6 openpyxl reportlab PyPDF2

3) Executar a aplicação
- py main.py

## Como usar
1) Digite a tarefa no campo “Adicione uma tarefa...” e selecione o quadrante.
2) Clique em “Adicionar Tarefa” ou pressione Enter.
3) Marque a caixa de seleção para mover a tarefa para “Concluídas”; desmarque para retornar.
4) Clique com o botão direito em uma tarefa para remover (com confirmação).
5) Menu Arquivo:
   - Novo: inicia sessão limpa.
   - Abrir: importa XLSX/PDF.
   - Salvar: exporta para XLSX/PDF.
   - Limpar: remove todos os dados.
   - Sair: fecha o app.
6) Configurações → Idioma: alterna entre pt-BR e en-US (textos atualizam imediatamente).
7) Opções → Sobre: exibe histórico, detalhes, licenças, avisos, política de privacidade e notas de versão.

## Formato e persistência de dados
- O arquivo tasks.json é salvo automaticamente no diretório persistente do usuário (ex.: AppData).
- Estrutura geral:
  {
    "quadrant1": [...],
    "quadrant1_completed": [...],
    "quadrant2": [...],
    "quadrant2_completed": [...],
    "quadrant3": [...],
    "quadrant3_completed": [...],
    "quadrant4": [...],
    "quadrant4_completed": [...]
  }

## Importação/Exportação
- XLSX:
  - Exporta/Importa 8 abas: quadrant1, quadrant1_completed, quadrant2, quadrant2_completed, quadrant3, quadrant3_completed, quadrant4, quadrant4_completed.
  - Os valores são lidos/escritos na primeira coluna de cada aba.
- PDF:
  - Exporta seções com títulos dos quadrantes e das listas concluídas.
  - Importa PDFs com seções identificáveis; caso o formato não seja reconhecido, o app informa.

## Idiomas suportados
- pt_BR: Português (Brasil)
- en_US: English (United States)

## Solução de problemas
- Não vejo minhas tarefas:
  - Verifique permissões de escrita na sua pasta de usuário (para o tasks.json).
- Importação XLSX/PDF falha:
  - Use o formato esperado (abas nomeadas por quadrante no XLSX, seções identificáveis no PDF).
- Alto consumo de recursos:
  - A aplicação é leve; problemas costumam ser externos (outros programas).

## Licenças, avisos e privacidade
- Acesse em Opções → Sobre.
- Textos são carregados de arquivos internos do aplicativo.

## Autor
- Fernando Nillsson Cidade

---

</details>

## <a id="enus"></a>🇺🇸 English (US)

<details>
<summary>Click to expand the README in English</summary>

# EISENHOWER ORGANIZER — Task Organizer using the Eisenhower Matrix

Version: v0.0.0.0 — October 13, 2025  
Author: Fernando Nillsson Cidade

**Total cumulative downloads:**  
![GitHub all releases](https://img.shields.io/github/downloads/fernandoncidade/Eisenhower_Task_Organizer/total?label=Total%20Downloads%20(Eisenhower%20Task%20Organizer))

## Summary
EISENHOWER ORGANIZER is a lightweight app to manage tasks with the Eisenhower Matrix (Important/Urgent). It lets you create tasks, classify them into quadrants, mark as completed (auto-moving between lists), remove items with confirmation, and export/import to XLSX/PDF. UI supports Portuguese (Brazil) and English (United States).

## Key features
- Quickly add tasks with a quadrant selector.
- Check/uncheck to move between pending and completed lists automatically.
- Remove tasks via right-click context menu with confirmation.
- Automatic local save to tasks.json in the user’s persistent directory.
- Export to XLSX and PDF (File → Save).
- Import from XLSX and PDF (File → Open).
- Multilingual interface: Portuguese (Brazil) and English (United States).
- “About” window with history, details, notices, licenses, privacy policy, and release notes.
- Offline operation (no telemetry).

## Requirements
- Windows 10 or later.
- To run from source: Python 3.9+.
- Dependencies: PySide6, openpyxl, reportlab, PyPDF2.

## Installation (from source on Windows)
1) Create a virtual environment
- PowerShell:
  - py -m venv .venv
  - .\.venv\Scripts\Activate.ps1
- CMD:
  - py -m venv .venv
  - .venv\Scripts\activate

2) Install dependencies
- pip install PySide6 openpyxl reportlab PyPDF2

3) Run the app
- py main.py

## How to use
1) Type the task in “Add a task...” and pick the quadrant.
2) Click “Add Task” or press Enter.
3) Tick the checkbox to move the task to “Completed”; untick to restore it.
4) Right-click a task to remove it (with confirmation).
5) File menu:
   - New: starts a clean session.
   - Open: import XLSX/PDF.
   - Save: export to XLSX/PDF.
   - Clear: remove all data.
   - Exit: close the app.
6) Settings → Language: switch between pt-BR and en-US (texts update immediately).
7) Options → About: shows history, details, licenses, notices, privacy policy, and release notes.

## Data format and persistence
- tasks.json is saved automatically in the user’s persistent directory (e.g., AppData).
- General structure:
  {
    "quadrant1": [...],
    "quadrant1_completed": [...],
    "quadrant2": [...],
    "quadrant2_completed": [...],
    "quadrant3": [...],
    "quadrant3_completed": [...],
    "quadrant4": [...],
    "quadrant4_completed": [...]
  }

## Import/Export
- XLSX:
  - Exports/Imports 8 sheets: quadrant1, quadrant1_completed, quadrant2, quadrant2_completed, quadrant3, quadrant3_completed, quadrant4, quadrant4_completed.
  - Values are written/read from the first column of each sheet.
- PDF:
  - Exports sections with quadrant and completed titles.
  - Imports PDFs with recognizable sections; if not supported, the app will warn.

## Supported languages
- pt_BR: Portuguese (Brazil)
- en_US: English (United States)

## Troubleshooting
- Tasks not appearing:
  - Check write permissions for your user folder (tasks.json).
- XLSX/PDF import fails:
  - Use the expected format (named sheets in XLSX, recognizable sections in PDF).
- High resource usage:
  - The app is lightweight; issues are likely due to other software.

## Licenses, notices, and privacy
- Available under Options → About.
- Texts are loaded from internal resource files.

## Author
- Fernando Nillsson Cidade

---

</details>
