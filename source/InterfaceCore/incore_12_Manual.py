from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente

_DATA_DIR = obter_caminho_persistente()


@dataclass(frozen=True)
class ManualDetails:
    summary: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManualSection:
    id: str
    title: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()
    details: tuple[ManualDetails, ...] = ()


@dataclass(frozen=True)
class ManualBlock:
    kind: str
    text: str = ""
    section_id: str | None = None


def normalize_language(lang: str | None) -> str:
    if not lang:
        return "pt_BR"

    v = lang.strip().replace("-", "_").lower()
    if v in ("pt_br", "pt"):
        return "pt_BR"

    if v in ("en_us", "en"):
        return "en_US"

    return "pt_BR"


def get_manual_title(lang: str | None = None) -> str:
    lang = normalize_language(lang)
    return "Manual de Utilização — EISENHOWER ORGANIZER" if lang == "pt_BR" else "User Manual — EISENHOWER ORGANIZER"

def to_unicode_bold(s: str) -> str:
    out: list[str] = []
    for ch in s:
        if "A" <= ch <= "Z":
            out.append(chr(ord(ch) - ord("A") + 0x1D400))

        elif "a" <= ch <= "z":
            out.append(chr(ord(ch) - ord("a") + 0x1D41A))

        elif "0" <= ch <= "9":
            out.append(chr(ord(ch) - ord("0") + 0x1D7CE))

        else:
            out.append(ch)

    return "".join(out)

def get_manual_document(lang: str | None = None) -> tuple[ManualSection, ...]:
    lang = normalize_language(lang)
    return _DOC_EN_US if lang == "en_US" else _DOC_PT_BR


def get_manual_blocks(lang: str | None = None) -> tuple[tuple[ManualBlock, ...], Tuple[str, ...]]:
    lang = normalize_language(lang)
    sections = get_manual_document(lang)

    blocks: list[ManualBlock] = []
    order: list[str] = []

    def blank() -> None:
        blocks.append(ManualBlock(kind="blank"))

    def line(text: str) -> None:
        blocks.append(ManualBlock(kind="line", text=text))

    def toc_title(text: str) -> None:
        blocks.append(ManualBlock(kind="toc_title", text=text))

    def toc_item(text: str, section_id: str) -> None:
        blocks.append(ManualBlock(kind="toc_item", text=text, section_id=section_id))

    def section_title(text: str, section_id: str) -> None:
        blocks.append(ManualBlock(kind="section_title", text=text, section_id=section_id))

    def detail_title(text: str) -> None:
        blocks.append(ManualBlock(kind="detail_title", text=text))

    def paragraph(text: str) -> None:
        blocks.append(ManualBlock(kind="paragraph", text=text))

    def bullet(text: str) -> None:
        blocks.append(ManualBlock(kind="bullet", text=text))

    def divider() -> None:
        blocks.append(ManualBlock(kind="divider", text="-" * 60))

    line(get_manual_title(lang))
    line("=" * len(get_manual_title(lang)))
    blank()

    if lang == "pt_BR":
        paragraph(
            "Este manual descreve como operar o aplicativo EISENHOWER ORGANIZER (modo de uso), cobrindo funcionalidades, atalhos, "
            "fluxo de trabalho sugerido, solução de problemas e informações sobre persistência de dados."
        )
        paragraph("Não é um guia de desenvolvimento.")
        blank()
        toc_title("Índice")

    else:
        paragraph(
            "This manual describes how to operate the EISENHOWER ORGANIZER application (user guide), covering features, shortcuts, "
            "suggested workflows, troubleshooting, and information about data persistence."
        )
        paragraph("It is not a development guide.")
        blank()
        toc_title("Table of Contents")

    for idx, s in enumerate(sections, start=1):
        toc_item(f"{idx}. {s.title}", section_id=s.id)

    blank()
    divider()
    blank()

    for s in sections:
        order.append(s.id)

        section_title(s.title, section_id=s.id)
        blank()

        for p in s.paragraphs:
            paragraph(p)
            blank()

        for b in s.bullets:
            bullet(b)

        if s.bullets:
            blank()

        for d in s.details:
            detail_title(d.summary)
            blank()

            for p in d.paragraphs:
                paragraph(p)
                blank()

            for b in d.bullets:
                bullet(b)

            if d.bullets:
                blank()

        divider()
        blank()

    return tuple(blocks), tuple(order)


def get_manual_text(lang: str | None = None) -> str:
    text, _positions, _order = get_manual_text_with_positions(lang)
    return text


def get_manual_text_with_positions(lang: str | None = None,) -> tuple[str, Dict[str, int], Tuple[str, ...]]:
    lang = normalize_language(lang)
    sections = get_manual_document(lang)

    lines: list[str] = []
    positions: dict[str, int] = {}
    order: list[str] = []

    def add_line(s: str = "") -> None:
        lines.append(s)

    def current_offset() -> int:
        return sum(len(l) + 1 for l in lines)

    title = get_manual_title(lang)
    add_line(title)
    add_line("=" * len(title))
    add_line()

    if lang == "pt_BR":
        add_line(
            "Este manual descreve como operar o aplicativo EISENHOWER ORGANIZER (modo de uso), cobrindo funcionalidades, atalhos, "
            "fluxo de trabalho sugerido, solução de problemas e informações sobre persistência de dados."
        )
        add_line("Não é um guia de desenvolvimento.")
        add_line()
        add_line("Índice")
        add_line("----------")

    else:
        add_line(
            "This manual describes how to operate the EISENHOWER ORGANIZER application (user guide), covering features, shortcuts, "
            "suggested workflows, troubleshooting, and information about data persistence."
        )
        add_line("It is not a development guide.")
        add_line()
        add_line("Table of Contents")
        add_line("------------------------------")

    for idx, s in enumerate(sections, start=1):
        add_line(f"{idx}. {s.title}")

    add_line()
    add_line("-" * 60)
    add_line()

    for s in sections:
        positions[s.id] = current_offset()
        order.append(s.id)

        add_line(s.title)
        add_line("-" * len(s.title))
        add_line()

        for p in s.paragraphs:
            add_line(p)
            add_line()

        for b in s.bullets:
            add_line(f"- {b}")

        if s.bullets:
            add_line()

        for d in s.details:
            add_line(d.summary)
            add_line("." * len(d.summary))
            add_line()

            for p in d.paragraphs:
                add_line(p)
                add_line()

            for b in d.bullets:
                add_line(f"- {b}")

            if d.bullets:
                add_line()

        add_line("-" * 60)
        add_line()

    return "\n".join(lines), positions, tuple(order)

# ----------------------------
# Conteúdo do manual (texto)
# ----------------------------

_DOC_PT_BR: tuple[ManualSection, ...] = (
    ManualSection(
        id="visao-geral",
        title="Visão Geral",
        paragraphs=(
            "Bem-vindo ao Eisenhower Organizer! Este manual explica, de forma simples e direta, como usar o aplicativo para organizar suas tarefas diárias usando a Matriz de Eisenhower.",
            "Não é preciso ser técnico — siga os passos e dicas apresentadas nas seções seguintes.",
        ),
    ),
    ManualSection(
        id="requisitos-basicos-usuario",
        title="Requisitos básicos (usuário)",
        bullets=(
            "Campo de texto para digitar a descrição da tarefa.",
            "Botão 'Adicionar Tarefa' para inserir a tarefa no quadrante selecionado.",
            "Botão 'Calendário' para visualizar tarefas por data.",
            "Checkbox 'Vincular data' e 'Vincular horário' para anexar datas/horários.",
            "Seletor de quadrante para escolher em qual dos 4 quadrantes a tarefa ficará.",
            "Quatro colunas (quadrantes) com listas de tarefas ativas e, abaixo, listas de tarefas concluídas.",
        ),
    ),
    ManualSection(
        id="como-iniciar-o-aplicativo",
        title="Como iniciar o aplicativo",
        bullets=(
            "Abra o aplicativo a partir do atalho ou executando o arquivo principal.",
            "Digite a descrição da tarefa no campo principal.",
            "Escolha o quadrante no seletor e marque 'Vincular data'/'Vincular horário' quando necessário.",
            "Clique em 'Adicionar Tarefa' para inserir a tarefa na lista.",
        ),
    ),
    ManualSection(
        id="abertura-e-controles-globais",
        title="Abertura e controles globais",
        paragraphs=(
            "A tela principal apresenta o campo de entrada, controles para vincular data e horário, o seletor de quadrante e quatro colunas que representam a Matriz de Eisenhower.",
            "No menu superior há opções de 'Arquivo', 'Configurações' e 'Opções' com acesso ao 'Sobre' e ao manual.",
        ),
    ),
    ManualSection(
        id="modulos",
        title="Matriz de Eisenhower",
        paragraphs=(
            "As tarefas são organizadas em quatro quadrantes segundo os critérios importância e urgência:",
            "Quadrante 1 (🔴): Importante e Urgente — fazer agora.",
            "Quadrante 2 (🟠): Importante, não urgente — planejar e executar com calma.",
            "Quadrante 3 (🟡): Não importante, urgente — delegar quando possível.",
            "Quadrante 4 (🟢): Não importante, não urgente — considerar eliminar ou deixar para depois.",
        ),
    ),
    ManualSection(
        id="menus-e-acoes-rapidas",
        title="Menus e ações rápidas",
        bullets=(
            "Novo: inicia uma nova sessão, limpando as listas atuais.",
            "Abrir: permite carregar uma sessão salva ou importar visualizações suportadas.",
            "Salvar / Salvar como: exporta ou salva suas tarefas para backup manual.",
            "Limpar: remove todas as tarefas após confirmação.",
            "Sair: fecha o aplicativo.",
            "Opções → Sobre / Manual: informações sobre a aplicação, licenças e este manual.",
        ),
    ),
    ManualSection(
        id="atalhos-teclado",
        title="Atalhos de teclado",
        paragraphs=(
            "A seguir estão os atalhos de teclado implementados e como ativá‑los. Para que os atalhos funcionem, a janela do aplicativo deve estar com foco. Alguns atalhos têm contexto de aplicação e funcionam mesmo com widgets internos em foco; em alguns sistemas operacionais, combinações com Alt podem ser interceptadas pelo SO ou pela barra de menus.",
        ),
        bullets=(
            to_unicode_bold("Novo — Ctrl+N:") + " cria uma nova sessão (Arquivo → Novo).",
            to_unicode_bold("Abrir — Ctrl+O:") + " abre diálogo para carregar arquivo (Arquivo → Abrir).",
            to_unicode_bold("Salvar — Ctrl+S:") + " salva sessão atual (Arquivo → Salvar).",
            to_unicode_bold("Limpar — Ctrl+Shift+L:") + " remove todas as tarefas após confirmação (Arquivo → Limpar).",
            to_unicode_bold("Sair — Ctrl+Q:") + " fecha o aplicativo (Arquivo → Sair).",
            to_unicode_bold("Abrir menu Arquivo — Alt+A:") + " mostra o menu 'Arquivo' (atalho global do app).",
            to_unicode_bold("Alterar idioma — Alt+I:") + " abre o menu 'Idioma' dentro de 'Configurações'.",
            to_unicode_bold("Calendário — Ctrl+M:") + " abre a janela do calendário (Configurações → Calendário).",
            to_unicode_bold("Abrir menu Opções — Alt+O:") + " mostra o menu 'Opções' (atalho global do app).",
            to_unicode_bold("Sobre / Ajuda — F1 (ou tecla de ajuda do sistema):") + " abre a janela 'Sobre' (Opções → Sobre).",
            to_unicode_bold("Manual — Ctrl+Shift+M:") + " abre o manual de utilização (Opções → Manual).",
        ),
    ),
    ManualSection(
        id="solucao-de-problemas",
        title="Solução de problemas",
        details=(
            ManualDetails(
                summary="Não vejo minhas tarefas",
                paragraphs=(
                    "Verifique se não foi usada a opção 'Limpar' acidentalmente.",
                ),
                bullets=(
                    "Tente usar 'Arquivo' → 'Abrir' para carregar um arquivo salvo.",
                    "Verifique se o arquivo de persistência correto está sendo lido.",
                ),
            ),
            ManualDetails(
                summary="Data/hora não aparecem",
                paragraphs=(
                    "Confirme se ao criar/editar a tarefa você marcou 'Vincular data' e/ou 'Vincular horário'.",
                ),
                bullets=(
                    "Edite a tarefa e reative as caixas de vínculo de data/horário se necessário.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="logs-e-diagnostico",
        title="Logs e diagnóstico",
        bullets=(
            f"Os logs de execução podem ajudar a diagnosticar problemas; verifique o arquivo de log gerado pela aplicação em: { _DATA_DIR }",
        ),
    ),
    ManualSection(
        id="faq",
        title="Perguntas frequentes (FAQ)",
        details=(
            ManualDetails(
                summary="Onde meus dados são salvos?",
                paragraphs=(
                    f"As tarefas e arquivos de configuração são armazenados no diretório: { _DATA_DIR }",
                    "Consulte esse diretório para localizar arquivos de persistência e logs.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="suporte",
        title="Como obter ajuda e suporte",
        bullets=(
            "Consulte a seção 'Sobre' dentro do aplicativo para informações oficiais e notas de versão.",
            f"Para problemas mais complexos, gere logs e envie-os ao suporte. Os arquivos de log estão em: { _DATA_DIR }",
        ),
    ),
)

_DOC_EN_US: tuple[ManualSection, ...] = (
    ManualSection(
        id="overview",
        title="Overview",
        paragraphs=(
            "Welcome to Eisenhower Organizer! This manual explains, in a simple and direct way, how to use the application to organize your daily tasks using the Eisenhower Matrix.",
            "No technical knowledge is required — follow the steps and tips in the sections below.",
        ),
    ),
    ManualSection(
        id="basic-requirements-user",
        title="Basic Requirements (User)",
        bullets=(
            "Text field to enter the task description.",
            "'Add Task' button to insert the task into the selected quadrant.",
            "'Calendar' button to view tasks by date.",
            "'Link date' and 'Link time' checkboxes to attach dates/times.",
            "Quadrant selector to choose which of the 4 quadrants the task will go to.",
            "Four columns (quadrants) showing active tasks and completed lists below each column.",
        ),
    ),
    ManualSection(
        id="how-to-start-the-application",
        title="How to Start the Application",
        bullets=(
            "Open the application from the shortcut or by running the main script.",
            "Type the task description in the main field.",
            "Choose the quadrant and enable 'Link date'/'Link time' when needed.",
            "Click 'Add Task' to insert the task into the list.",
        ),
    ),
    ManualSection(
        id="startup-and-global-controls",
        title="Startup and Global Controls",
        paragraphs=(
            "The main screen presents the input field, controls to link date/time, the quadrant selector and four columns that represent the Eisenhower Matrix.",
            "Top menu provides 'File', 'Settings' and 'Options' with access to About and the manual.",
        ),
    ),
    ManualSection(
        id="modules",
        title="Eisenhower Matrix",
        paragraphs=(
            "Tasks are organized into four quadrants according to importance and urgency:",
            "Quadrant 1 (🔴): Important and Urgent — do it now.",
            "Quadrant 2 (🟠): Important, not urgent — plan and execute calmly.",
            "Quadrant 3 (🟡): Not important, urgent — delegate when possible.",
            "Quadrant 4 (🟢): Not important, not urgent — consider removing or postponing.",
        ),
    ),
    ManualSection(
        id="menus-and-quick-actions",
        title="Menus and Quick Actions",
        bullets=(
            "New: starts a new session, clearing current lists.",
            "Open: allows loading a saved session or importing supported views.",
            "Save / Save as: exports or saves your tasks for manual backup.",
            "Clear: removes all tasks after confirmation.",
            "Exit: closes the application.",
            "Options → About / Manual: information about the app, licenses and this manual.",
        ),
    ),
    ManualSection(
        id="keyboard-shortcuts",
        title="Keyboard Shortcuts",
        paragraphs=(
            "Below are the implemented keyboard shortcuts and how to trigger them. The application window must be focused for shortcuts to work. Some shortcuts use application-wide context and work even when internal widgets have focus; on some OSes Alt combinations may be intercepted by the system or menu bar.",
        ),
        bullets=(
            to_unicode_bold("New — Ctrl+N:") + " creates a new session (File → New).",
            to_unicode_bold("Open — Ctrl+O:") + " opens file dialog to load a session (File → Open).",
            to_unicode_bold("Save — Ctrl+S:") + " saves current session (File → Save).",
            to_unicode_bold("Clear — Ctrl+Shift+L:") + " removes all tasks after confirmation (File → Clear).",
            to_unicode_bold("Exit — Ctrl+Q:") + " closes the application (File → Exit).",
            to_unicode_bold("Open File menu — Alt+A:") + " shows the 'File' menu (application global shortcut).",
            to_unicode_bold("Change language — Alt+I:") + " opens the 'Language' submenu inside 'Settings'.",
            to_unicode_bold("Calendar — Ctrl+M:") + " opens the calendar window (Settings → Calendar).",
            to_unicode_bold("Open Options menu — Alt+O:") + " shows the 'Options' menu (application global shortcut).",
            to_unicode_bold("About / Help — F1 (or system help key):") + " opens the 'About' dialog (Options → About).",
            to_unicode_bold("Manual — Ctrl+Shift+M:") + " opens the user manual (Options → Manual).",
        ),
    ),
    ManualSection(
        id="troubleshooting",
        title="Troubleshooting",
        details=(
            ManualDetails(
                summary="I don't see my tasks",
                paragraphs=(
                    "Check that you did not use the 'Clear' option by mistake.",
                ),
                bullets=(
                    "Try 'File' → 'Open' to load a saved session or backup.",
                    "Verify the persistence file and data directory used by the application.",
                ),
            ),
            ManualDetails(
                summary="Date/time not showing",
                paragraphs=(
                    "Confirm that 'Link date' and/or 'Link time' were enabled when creating or editing the task.",
                ),
                bullets=(
                    "Edit the task and re-enable date/time linking if required.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="logs-and-diagnostics",
        title="Logs and Diagnostics",
        bullets=(
            f"Execution logs can help diagnose issues; check the application's log file located at: { _DATA_DIR }",
        ),
    ),
    ManualSection(
        id="faq",
        title="FAQ (Frequently Asked Questions)",
        details=(
            ManualDetails(
                summary="Where are my data saved?",
                paragraphs=(
                    f"Tasks and configuration files are stored under: { _DATA_DIR }",
                    "Check that folder to locate persistence files and logs.",
                ),
            ),
        ),
    ),
    ManualSection(
        id="support",
        title="How to Get Help / Support",
        bullets=(
            "See the 'About' section inside the application for official information and release notes.",
            f"For complex issues, generate logs and send them to support. Log files are located at: { _DATA_DIR }",
        ),
    ),
)
