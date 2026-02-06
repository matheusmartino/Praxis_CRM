# Praxis CRM — Guia de Estilo v2

Referência visual oficial do projeto. Atualizado para refletir o **Style v2** — visual minimalista, institucional, focado em leitura e trabalho diário.

> **Princípio:** "Lapidar sem quebrar. Refinar sem chamar atenção. Software de trabalho diário, não peca de marketing."

---

## Filosofia Visual

- **Menos cores cheias, mais fundo branco.** Cor solida apenas em badges de status.
- **Cards de metricas** usam fundo branco com borda lateral colorida (4px).
- **Tabelas limpas** com headers cinza claro, zebra quase imperceptivel.
- **Tipografia com hierarquia clara**: labels uppercase, valores em destaque.
- **Icones discretos**, nunca protagonistas. Servem de apoio ao texto.
- **Interface que transmite metodo, disciplina e confiabilidade.**

---

## Arquitetura de CSS

O visual e construido em camadas incrementais, sem sobrescrever arquivos anteriores:

| Arquivo | Funcao | Pode remover? |
|---------|--------|---------------|
| Bootstrap 5.3.3 (CDN) | Framework base | Nao |
| `static/css/variables.css` | Tokens de design (cores, tipografia, espacamento) | Nao |
| `static/css/style.css` | Estilos globais minimos (body, card shadow, navbar-brand) | Nao |
| `static/css/praxis-v2.css` | **Overlay visual v2** — todas as refinacoes visuais | Sim (reverte ao visual v1) |

**Para reverter ao visual v1:** remova a linha `<link>` do `praxis-v2.css` em `base.html`.

**Importacao automatica:** O `praxis-v2.css` importa `variables.css` via `@import`, garantindo acesso a todos os tokens.

---

## Tipografia

### Familia de Fontes

```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### Hierarquia de Tamanhos (v2)

| Elemento | Tamanho | Peso | Cor | Extras |
|----------|---------|------|-----|--------|
| H2 (titulo de pagina) | 1.4rem | 600 | `#2c3e50` | `letter-spacing: -0.01em` |
| H3 | 1.2rem | 600 | `#2c3e50` | |
| H4 | 1.05rem | 600 | `#2c3e50` | |
| H5 (card-header) | 0.95rem / 0.9rem | 600 | `#2c3e50` | |
| Body | 0.9375rem | 400 | `#333333` | `line-height: 1.6` |
| Labels (form, table header, dt) | 0.75rem-0.78rem | 600 | `#7f8c8d` | `text-transform: uppercase; letter-spacing: 0.04em` |
| Card metric title | 0.75rem | 600 | `#7f8c8d` | `text-transform: uppercase; letter-spacing: 0.05em` |
| Texto auxiliar | 0.78rem | 400 | `#95a5a6` | |
| Badges | 0.73em | 500 | branco | `letter-spacing: 0.02em` |

### Line Height

```css
line-height: 1.6;  /* Padrao (body) */
line-height: 1.7;  /* Subtitulos longos */
line-height: 1.2;  /* Titulos grandes */
```

---

## Paleta de Cores

### Cores Principais

| Nome | Hex | Uso no v2 |
|------|-----|-----------|
| Azul Escuro | `#2c3e50` | Navbar, titulos (h1-h6), valores de metrica, borda card-dark |
| Azul Principal | `#3498db` | Links, botoes primarios, borda card-primary, focus de inputs |
| Azul Hover | `#2980b9` | Hover de links e botoes |
| Azul Medio | `#34495e` | Subtitulos |

### Cores de Texto

| Nome | Hex | Uso no v2 |
|------|-----|-----------|
| Texto Principal | `#333333` | Corpo de texto, valores em cards/tabelas |
| Texto Secundario | `#7f8c8d` | Labels uppercase, card-title de metricas, dt em definition lists |
| Texto Muted | `#95a5a6` | Informacoes terciarias, form-text |

### Cores de Fundo

| Nome | Hex | Uso no v2 |
|------|-----|-----------|
| Branco | `#ffffff` | Fundo de cards de metrica, fundo principal |
| Cinza Fundo | `#f8f9fa` | card-header, thead.table-dark (agora cinza), body |
| Cinza Claro | `#f4f4f4` | Code blocks |

### Cores de Status (unica excecao — cor cheia permitida)

| Nome | Hex | Uso no v2 |
|------|-----|-----------|
| Verde (OK) | `#27ae60` | Badge bg-success, borda card-success, alert-success |
| Laranja (Atencao) | `#f39c12` | Badge bg-warning, borda card-warning, alert-warning |
| Vermelho (Risco) | `#e74c3c` | Badge bg-danger, borda card-danger, alert-danger |

### Cores de Acento (bordas laterais)

| Contexto | Cor | Uso |
|----------|-----|-----|
| Card Primary | `#3498db` | Borda esquerda 4px |
| Card Success | `#27ae60` | Borda esquerda 4px |
| Card Info | `#17a2b8` | Borda esquerda 4px |
| Card Warning | `#f39c12` | Borda esquerda 4px |
| Card Secondary | `#6c757d` | Borda esquerda 4px |
| Card Dark | `#2c3e50` | Borda esquerda 4px |
| Card Danger | `#e74c3c` | Borda esquerda 4px |

---

## Variaveis CSS

Arquivo: `static/css/variables.css` (importado automaticamente pelo v2).

```css
:root {
    /* Cores */
    --praxis-azul-escuro: #2c3e50;
    --praxis-azul-principal: #3498db;
    --praxis-azul-hover: #2980b9;
    --praxis-azul-medio: #34495e;
    --praxis-texto-principal: #333333;
    --praxis-texto-secundario: #7f8c8d;
    --praxis-texto-muted: #95a5a6;
    --praxis-fundo-branco: #ffffff;
    --praxis-fundo-cinza: #f8f9fa;
    --praxis-verde: #27ae60;
    --praxis-verde-fundo: #e8f8f5;
    --praxis-laranja: #f39c12;
    --praxis-laranja-fundo: #fef9e7;
    --praxis-vermelho: #e74c3c;

    /* Tipografia */
    --praxis-font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --praxis-font-size-base: 16px;

    /* Bordas */
    --praxis-border-radius: 5px;
    --praxis-border-radius-lg: 8px;

    /* Sombras */
    --praxis-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);

    /* Transicoes */
    --praxis-transition: all 0.2s ease;
    --praxis-transition-fast: all 0.15s ease;
}
```

---

## Componentes

### Navbar

Fundo azul escuro institucional (nao preto). Links com opacidade reduzida, hover sutil.

```css
/* v2: bg-dark (#212529) sobrescrito para azul institucional */
.navbar.navbar-dark.bg-dark {
    background-color: #2c3e50 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

/* Nav links: discretos, opacity 0.7 → 1 no hover */
.navbar .nav-link {
    font-size: 0.85rem;
    opacity: 0.7;
}

/* Icones na navbar: menores que o texto */
.navbar .nav-link .bi {
    font-size: 0.8em;
}
```

**Dropdown:** bordas sutis (`rgba(0,0,0,0.08)`), sombra leve, border-radius 6px.

---

### Cards — Base

Todos os cards recebem bordas sutis e sombra minima.

```css
.card {
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    font-size: 0.9rem;
}
```

**Hover:** apenas em cards dentro de links (CTAs).

---

### Cards de Metricas — Fundo branco + Borda lateral

**Antes (v1):** Fundo solido colorido com texto branco.
**Depois (v2):** Fundo branco, borda esquerda de 4px colorida, texto escuro.

```css
/* Exemplo: card primary */
.card.bg-primary,
.card.text-bg-primary {
    background-color: #ffffff !important;
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-left: 4px solid #3498db !important;
    color: #333333 !important;
}

/* Titulo do card: label discreto */
.card.bg-primary .card-title {
    color: #7f8c8d !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Valor numerico: destaque */
.card.bg-primary h2 {
    color: #2c3e50 !important;
    font-weight: 700;
}

/* Icone marca d'agua: cor da marca a 12% */
.card.bg-primary .opacity-50 {
    color: #3498db !important;
    opacity: 0.12 !important;
}
```

**Todas as variantes:** primary, success, info, warning, secondary, dark, danger — mesmo padrao, cor diferente.

**Telas afetadas:** Dashboard (home.html), Dashboard Gestao, Minha Meta.

---

### Tabelas

**Antes (v1):** `thead.table-dark` com fundo preto e texto branco.
**Depois (v2):** Header cinza claro com labels uppercase muted. Zebra quase imperceptivel.

```css
/* Header: override via CSS custom properties do Bootstrap */
thead.table-dark {
    --bs-table-color: #7f8c8d;
    --bs-table-bg: #f8f9fa;
    --bs-table-border-color: rgba(0, 0, 0, 0.06);
}

/* Labels uppercase */
.table > thead th {
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #7f8c8d;
}

/* Zebra suave */
.table-striped > tbody > tr:nth-of-type(odd) > * {
    --bs-table-bg-type: rgba(0, 0, 0, 0.015);
}

/* Bordas quase invisiveis */
.table > :not(caption) > * > * {
    border-bottom-color: rgba(0, 0, 0, 0.05);
}
```

**Telas afetadas:** Todas as listagens e relatorios.

---

### Badges

Badges **mantem cor solida** — sao os unicos elementos com fundo colorido no v2. Servem como indicadores de status (OK, Atencao, Risco, etapas do pipeline).

```css
.badge {
    font-weight: 500;
    font-size: 0.73em;
    padding: 0.35em 0.6em;
    border-radius: 4px;
    letter-spacing: 0.02em;
}
```

**Cores de badge ativas no sistema:**

| Classe | Cor | Uso |
|--------|-----|-----|
| `badge bg-success` | Verde | ATIVO, OK, Fechamento, Em dia |
| `badge bg-warning text-dark` | Laranja | PROVISORIO, Atencao, Hoje |
| `badge bg-danger` | Vermelho | Risco, Perdida, Atrasado |
| `badge bg-primary` | Azul | Etapas do pipeline (padrao) |
| `badge bg-secondary` | Cinza | Status generico |
| `badge bg-info` | Ciano | Metricas, percentuais |

---

### Formularios

Labels uppercase discretos, inputs com foco azul suave.

```css
.form-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #7f8c8d;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.form-control:focus,
.form-select:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}
```

**Telas afetadas:** Todos os formularios de cadastro e edicao, filtros.

---

### Botoes

Cores da marca, tamanhos refinados.

```css
.btn {
    font-size: 0.85rem;
    font-weight: 500;
    border-radius: 5px;
    letter-spacing: 0.01em;
}

.btn-primary {
    background-color: #3498db;
    border-color: #3498db;
}

.btn-primary:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}

.btn-outline-primary {
    color: #3498db;
    border-color: #3498db;
}
```

---

### Alertas

**Antes (v1):** Borda completa do Bootstrap.
**Depois (v2):** Sem borda completa. Borda esquerda de 4px como acento. Fundo pastel.

```css
.alert {
    font-size: 0.85rem;
    border-radius: 8px;
    border: none;
    border-left: 4px solid transparent;
}

.alert-warning {
    background-color: #fef9e7;
    border-left-color: #f39c12;
}

.alert-success {
    background-color: #e8f8f5;
    border-left-color: #27ae60;
}

.alert-info {
    background-color: #e8f4f8;
    border-left-color: #17a2b8;
}

.alert-danger {
    background-color: #fdf0ef;
    border-left-color: #e74c3c;
}
```

---

### Caixas de Destaque (manual e landing)

Ja seguiam o padrao v2 desde a v1. Mantidas sem alteracao.

```css
.info-box {
    background-color: #e8f4f8;
    border-left: 4px solid #3498db;
    padding: 15px;
    border-radius: 0 5px 5px 0;
}

.warning-box {
    background-color: #fef9e7;
    border-left: 4px solid #f39c12;
}

.success-box {
    background-color: #e8f8f5;
    border-left: 4px solid #27ae60;
}
```

---

### Definition Lists (paginas de detalhe)

```css
dl.row dt {
    font-size: 0.75rem;
    font-weight: 600;
    color: #7f8c8d;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

dl.row dd {
    font-size: 0.875rem;
    color: #333333;
}
```

**Telas afetadas:** Detalhe de Cliente, Detalhe de Oportunidade.

---

### List Groups

```css
.list-group-item {
    border-color: rgba(0, 0, 0, 0.06);
    padding: 0.65rem 1rem;
    font-size: 0.875rem;
}
```

**Telas afetadas:** Dashboard (clientes recentes, oportunidades), Detalhe de Cliente (oportunidades).

---

### Paginacao

```css
.pagination .page-link {
    font-size: 0.85rem;
    color: #3498db;
    border-color: rgba(0, 0, 0, 0.08);
}

.pagination .page-item.active .page-link {
    background-color: #3498db;
    border-color: #3498db;
}
```

---

### Progress Bar

```css
.progress {
    border-radius: 5px;
    background-color: rgba(0, 0, 0, 0.04);
}

.progress-bar {
    font-size: 0.78rem;
    font-weight: 600;
}
```

**Tela afetada:** Minha Meta (barra de atingimento).

---

## Espacamento

### Padding (v2)

| Contexto | Valor |
|----------|-------|
| Container (bottom) | 2rem |
| Card body | Bootstrap padrao (1rem) |
| Card header | Bootstrap padrao |
| Table cells | 0.65rem 0.75rem |
| Table header cells | 0.7rem 0.75rem |
| Inputs | 0.5rem 0.75rem |

### Gap / Grid

| Contexto | Valor |
|----------|-------|
| Cards em grid | `g-4` (Bootstrap) |
| Botoes em row | `gap-2` |
| Form fields | `mb-3` |

---

## Sombras

```css
/* Card base */
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);

/* Card hover (somente dentro de links) */
box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);

/* Navbar */
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);

/* Dropdown */
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);

/* Focus de input */
box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
```

---

## Transicoes

```css
transition: all 0.15s ease;    /* Padrao v2 (rapido) */
transition: all 0.2s ease;     /* Padrao geral */
transition: opacity 0.15s ease; /* Nav links */
transition: color 0.15s ease;   /* Links */
```

---

## Breakpoints Responsivos

| Breakpoint | Uso |
|------------|-----|
| `col-sm-*` (576px+) | Definition lists, layouts basicos |
| `col-md-*` (768px+) | Grids de cards, colunas de formulario |
| `col-lg-*` (992px+) | Navbar collapse |
| `table-responsive` | Scroll horizontal em tabelas no mobile |

---

## Notas de Especificidade CSS

Referencia tecnica para manutencao do v2:

| Padrao | Tecnica | Motivo |
|--------|---------|--------|
| `.card.bg-primary` vs `.bg-primary` | Especificidade maior + `!important` | Bootstrap usa `!important` nas utilities |
| `thead.table-dark` | Override de CSS custom properties | Bootstrap usa `--bs-table-*` vars |
| `.card-header.bg-info` | **NAO** e atingido por `.card.bg-info` | Sao elementos diferentes (header vs card) |
| `.text-white` em cards | Sobrescrito para texto escuro | Fundo agora branco, texto precisa ser escuro |
| `.text-white h5` | `color: inherit` | Preserva branco no header de tips (followup_form) |

---

## Arquivos de Referencia

| Arquivo | Tipo | Descricao |
|---------|------|-----------|
| `static/css/variables.css` | CSS | Tokens de design (130 linhas) |
| `static/css/style.css` | CSS | Estilos globais base (12 linhas) |
| `static/css/praxis-v2.css` | CSS | **Overlay visual v2** (todas as refinacoes) |
| `templates/base.html` | Django | Template master (carrega todos os CSS) |
| `templates/landing.html` | HTML | Landing page standalone (inline styles, nao afetada pelo v2) |
| `docs/manual_usuario.html` | HTML | Manual do usuario (inline styles alinhados ao v2) |
| Bootstrap 5.3.3 | CDN | Framework CSS base |
| Bootstrap Icons 1.11.3 | CDN | Icones |

---

## Tom Visual

- **Institucional e maduro** — software de trabalho diario, nao peca de marketing
- **Clean, com muito espaco em branco** — respiro visual
- **Cores cheias apenas para status** (badges) — todo o resto usa fundo branco
- **Labels uppercase** para hierarquia clara (dt, form-label, thead)
- **Sombras quase invisiveis** — interface plana, nao flutuante
- **Icones discretos** — apoiam o texto, nunca protagonizam
- **Sem animacoes** — transicoes rapidas (0.15s), apenas em hover/focus
- **Metodo e disciplina** — cada elemento no lugar certo, sem excessos
