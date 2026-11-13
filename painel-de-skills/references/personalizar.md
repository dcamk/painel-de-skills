# Personalizar o painel

## overrides.json

Chaves são o nome da skill (com ou sem `/`). Campos aceitos: `cat`, `desc`, `ex`, `tr` (lista de frases), `uw`.

```json
{
  "minha-skill": {
    "cat": "Visual",
    "desc": "Cria páginas de produto com seções e botões de compra.",
    "ex": "Crie a página de um tênis de corrida",
    "tr": ["crie uma página de produto", "landing do meu produto"]
  }
}
```

Categorias com ícone próprio: Visual, Animação, 3D, Vídeo, Áudio, Imagem, Documentos, Código, Projetos. Qualquer outra aparece com o ícone de reticências.

## previews.json

Liga a **Galeria** e os **catálogos completos**. Caminhos são relativos ao arquivo `previews.json`; o gerador copia a mídia para ao lado do HTML.

```json
{
  "previews": {
    "/minha-skill": [
      {"i": "midia/a.jpg", "v": "midia/a.mp4", "cap": "Exemplo do repositório: tênis de corrida"},
      {"i": "midia/b.jpg", "v": null, "cap": "Render meu: vista lateral"}
    ]
  },
  "catalogs": {
    "/minha-skill": {
      "kind": "media",
      "items": [{"t": "Título", "cap": "Melhor para...", "f": "16:9 · 12 s", "i": "midia/c.jpg", "v": "midia/c.mp4"}]
    },
    "/outra-skill": {
      "kind": "pal",
      "sect": {"Fintech": [1, 2]},
      "items": [{"n": 1, "name": "Nome", "c": ["#111111", "#222222", "#333333", "#444444"], "use": "clima e uso"}]
    }
  }
}
```

- `i` é a imagem de capa (JPG/PNG/WebP), `v` o vídeo opcional (MP4). Prefira miniaturas de até 720 px e clipes curtos, sem áudio.
- `kind: "media"` mostra cartões com vídeo ao passar o cursor; `kind: "pal"` mostra paletas de 4 cores com HEX copiável e filtros por setor.
- Legende sempre a origem de cada prévia no campo `cap`.

## Publicar como Artifact com mídia

Passe `root` (a pasta do HTML) e `files` com os caminhos da mídia, por exemplo `["midia/a.jpg", "midia/a.mp4"]`.
