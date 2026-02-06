# Praxis CRM — Guia de Estilo

Referência de tipografia, cores e estilos visuais do projeto.

---

## Tipografia

### Família de Fontes

```css
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
```

### Tamanhos

| Elemento | Tamanho | Peso |
|----------|---------|------|
| H1 (título principal) | 2.5em / 2.8em (hero) | 600 |
| H2 (seções) | 1.8em | 600 |
| H3 (subtítulos) | 1.3em | 600 |
| Texto corpo | 1em (16px base) | 400 |
| Texto pequeno | 0.9em - 0.95em | 400 |
| Badges | 0.85em | 700 |

### Line Height

```css
line-height: 1.6;  /* Padrão */
line-height: 1.7;  /* Subtítulos longos */
line-height: 1.2;  /* Títulos grandes */
```

---

## Paleta de Cores

### Cores Principais

| Nome | Hex | Uso |
|------|-----|-----|
| Azul Escuro | `#2c3e50` | Títulos, textos principais, navbar, footer |
| Azul Principal | `#3498db` | CTAs, links, bordas de destaque, badges |
| Azul Médio | `#34495e` | Subtítulos, textos secundários |

### Cores de Texto

| Nome | Hex | Uso |
|------|-----|-----|
| Texto Principal | `#333333` | Corpo de texto |
| Texto Secundário | `#7f8c8d` | Subtítulos, labels |
| Texto Muted | `#95a5a6` | Informações secundárias |

### Cores de Fundo

| Nome | Hex | Uso |
|------|-----|-----|
| Branco | `#ffffff` | Fundo principal |
| Cinza Fundo | `#f8f9fa` | Seções alternadas, cards |
| Cinza Claro | `#f4f4f4` | Code blocks |

### Cores de Status

| Nome | Hex | Uso |
|------|-----|-----|
| Verde (OK) | `#27ae60` | Sucesso, confirmação |
| Laranja (Atenção) | `#f39c12` | Alertas, warnings |
| Vermelho (Risco) | `#e74c3c` | Erros, perigo |

### Cores de Borda

| Nome | Hex | Uso |
|------|-----|-----|
| Borda Padrão | `#dddddd` | Bordas de tabelas, divisores |
| Borda Clara | `#bdc3c7` | Bordas sutis |

---

## Variáveis CSS

```css
:root {
    --azul-escuro: #2c3e50;
    --azul-principal: #3498db;
    --azul-medio: #34495e;
    --cinza-texto: #7f8c8d;
    --cinza-claro: #95a5a6;
    --cinza-fundo: #f8f9fa;
    --verde: #27ae60;
    --laranja: #f39c12;
    --vermelho: #e74c3c;
    --branco: #ffffff;
    --borda: #dddddd;
}
```

---

## Componentes

### Botões

#### Primário
```css
.btn-primary {
    background-color: #3498db;
    color: #ffffff;
    padding: 14px 32px;
    border-radius: 5px;
    font-weight: 600;
}

.btn-primary:hover {
    background-color: #2980b9;
}
```

#### Secundário
```css
.btn-secondary {
    background-color: transparent;
    color: #3498db;
    border: 2px solid #3498db;
    padding: 14px 32px;
    border-radius: 5px;
    font-weight: 600;
}

.btn-secondary:hover {
    background-color: #3498db;
    color: #ffffff;
}
```

#### Outline (navbar)
```css
.btn-outline-light {
    background-color: transparent;
    color: #2c3e50;
    border: 2px solid #2c3e50;
    padding: 10px 20px;
    border-radius: 5px;
}
```

### Cards

```css
/* Card padrão */
.card {
    background: #ffffff;
    padding: 30px;
    border-radius: 8px;
    border-top: 4px solid #3498db;
}

/* Card de problema/alerta */
.card-warning {
    background: #ffffff;
    padding: 30px;
    border-radius: 8px;
    border-left: 4px solid #f39c12;
}
```

### Caixas de Destaque

```css
/* Info box (azul) */
.info-box {
    background-color: #e8f4f8;
    border-left: 4px solid #3498db;
    padding: 15px;
    border-radius: 0 5px 5px 0;
}

/* Warning box (laranja) */
.warning-box {
    background-color: #fef9e7;
    border-left: 4px solid #f39c12;
    padding: 15px;
    border-radius: 0 5px 5px 0;
}

/* Success box (verde) */
.success-box {
    background-color: #e8f8f5;
    border-left: 4px solid #27ae60;
    padding: 15px;
    border-radius: 0 5px 5px 0;
}
```

### Badges de Perfil

```css
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 0.85em;
    font-weight: bold;
}

.badge-vendedor {
    background-color: #3498db;
    color: white;
}

.badge-gestor {
    background-color: #9b59b6;
    color: white;
}

.badge-admin {
    background-color: #e74c3c;
    color: white;
}
```

### Tabelas

```css
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9em;
}

th {
    background-color: #3498db;
    color: white;
    padding: 12px;
    text-align: left;
}

td {
    border: 1px solid #ddd;
    padding: 12px;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}
```

### Títulos com Borda

```css
/* H1 com borda inferior */
h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
}

/* H2 com borda lateral */
h2 {
    color: #34495e;
    padding-left: 10px;
    border-left: 4px solid #3498db;
}
```

---

## Espaçamento

### Padding

| Contexto | Valor |
|----------|-------|
| Container | 0 20px |
| Seções | 80px 0 |
| Cards | 30px |
| Caixas de destaque | 15px |
| Botões | 14px 32px |

### Margin

| Contexto | Valor |
|----------|-------|
| Entre seções | 40px |
| Após títulos H1 | 20px |
| Após títulos H2 | 15px |
| Parágrafos | 15px (bottom) |

### Gap (Grid/Flex)

| Contexto | Valor |
|----------|-------|
| Cards em grid | 30px |
| Botões | 15px |
| Links de navegação | 25px |

---

## Sombras

```css
/* Sombra sutil (botões, cards flutuantes) */
box-shadow: 0 2px 5px rgba(0,0,0,0.2);
```

---

## Transições

```css
transition: all 0.2s;
transition: color 0.2s;
transition: background-color 0.2s;
```

---

## Breakpoints Responsivos

| Breakpoint | Uso |
|------------|-----|
| max-width: 900px | Tablets, grids 2 colunas |
| max-width: 768px | Mobile, grids 1 coluna |

---

## Arquivos de Referência

- **Landing page**: `templates/landing.html`
- **Manual do usuário**: `docs/manual_usuario.html`
- **CSS global (Bootstrap)**: CDN Bootstrap 5.3.3
- **Ícones**: Bootstrap Icons 1.11.3

---

## Tom Visual

- **Profissional e institucional**
- **Clean, com bastante espaço em branco**
- **Cores discretas e sóbrias**
- **Sem animações exageradas**
- **Sem marketing agressivo**
