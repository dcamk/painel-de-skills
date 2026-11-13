---
name: painel-de-skills
description: Gera um painel visual (uma página HTML) com todas as skills instaladas do Claude Code, agrupadas por categoria, com busca, descrição, exemplo de pedido e botões para copiar o comando. Barra superior que expande ao passar o cursor, cartões que abrem com os detalhes, galeria opcional de prévias e catálogos completos. Use quando o usuário pedir "um painel das minhas skills", "ver minhas skills", "catálogo de skills", "lista de skills com exemplos" ou "painel para chamar as skills".
---

# painel-de-skills

Cria uma página única (`painel-skills.html`) que lista as skills que a pessoa tem instaladas. Cada skill vira um cartão com nome do comando, resumo, exemplo de pedido e botões **Copiar comando** e **Copiar exemplo**. O painel só lê os `SKILL.md`: não copia nem altera as skills.

## Como gerar

1. Rode o gerador (Python 3, sem dependências):

   ```bash
   python3 SKILL_DIR/scripts/build_panel.py --out painel-skills.html
   ```

   `SKILL_DIR` é a pasta desta skill (normalmente `~/.claude/skills/painel-de-skills`). Por padrão ele lê `~/.claude/skills`.

2. Para ver dentro do Claude, publique o HTML como Artifact (ferramenta `Artifact`, `file_path` apontando para o arquivo). Se usou prévias, publique também a pasta de mídia com `files` (veja abaixo).

3. Diga à pessoa quantas skills entraram e em quais categorias. Se uma skill ficou na categoria "Outros" ou com descrição ruim, ofereça ajustar com um arquivo de overrides.

## Opções

| Opção | Efeito |
|---|---|
| `--skills-dir PASTA` | Outra pasta de skills (por exemplo a de um projeto: `.claude/skills`). |
| `--include a,b` / `--exclude c` | Só estas skills / todas menos estas. |
| `--overrides arquivo.json` | Troca categoria, descrição, exemplo ou frases de uma skill. Veja `references/personalizar.md`. |
| `--previews arquivo.json` | Liga a galeria de prévias e os catálogos completos. Veja `references/personalizar.md`. |
| `--title "Nome"` | Título da página. |

## O que o painel tem

- Barra superior recolhida (só ícones) que alarga ao passar o cursor; busca ao lado, sem acento.
- Cartões compactos com a linha "Ex."; ao passar o cursor abrem com descrição, frases que ativam a skill (lidas do arquivo) e botões de copiar. No toque, o cartão abre ao tocar.
- Aba **Galeria** (só se houver prévias) com mosaico e janela de ampliação; botão "Ver catálogo completo" nas skills que tiverem catálogo.
- Transições de página e de estado, grão e desfoque suaves, tema claro e escuro pelo sistema, respeita `prefers-reduced-motion`.

## Regras

- Não copie as skills da pessoa para outro lugar e não publique o painel em lugar público sem pedir. O painel mostra nomes e descrições das skills dela.
- As descrições automáticas vêm do arquivo da skill e podem estar em inglês; diga isso e ofereça escrever resumos em português via overrides.
- Não invente prévias: só inclua mídia que existe de verdade, e legende a origem (exemplo do repositório, render da pessoa, demo criada para a prévia).
