# Praxis CRM

Sistema CRM para gestão de clientes, oportunidades e interações de vendas.

## Como rodar o projeto

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
python manage.py migrate

# Criar superusuário (admin)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Acesse `http://localhost:8000` no navegador.

## Fluxo do vendedor

1. Fazer login em `/accounts/login/`
2. No dashboard, ver oportunidades abertas e clientes recentes
3. Cadastrar clientes — status inicial é sempre **Provisório**
4. Criar oportunidades vinculadas a clientes
5. Registrar interações (ligação, e-mail, reunião, WhatsApp, visita)
6. Avançar etapas do pipeline: Prospecção → Qualificação → Proposta → Negociação → Fechamento
7. Marcar oportunidades como perdidas quando necessário

O vendedor só visualiza seus próprios clientes e oportunidades.

## Campos do cliente

| Campo | Descrição | Obrigatório |
|---|---|---|
| nome | Nome / Razão social | Sim |
| cnpj_cpf | CNPJ ou CPF | Opcional no cadastro rápido (provisório). **Obrigatório para ativar o cliente.** |
| tipo | B2B (PJ) ou B2C (PF) | Sim |
| telefone | Telefone da empresa | Não |
| email | E-mail da empresa | Não |
| nome_contato_principal | Nome do contato principal | Não |
| telefone_contato | Telefone do contato | Não |
| email_contato | E-mail do contato | Não |

### Regra de validação — CNPJ/CPF

O campo `cnpj_cpf` é opcional durante o cadastro rápido (cliente provisório). Ao tentar **ativar** o cliente (via Admin ou service), o sistema exige que o CNPJ/CPF esteja preenchido. Isso permite que o vendedor registre leads rapidamente sem burocracia e o admin só aprove clientes com documentação completa.

## Fluxo do gestor comercial

O gestor comercial tem acesso **somente leitura** para avaliar leads, pipeline e performance do time.

1. Fazer login em `/accounts/login/`
2. Acessar o menu **Gestão** na barra de navegação
3. Visualizar o **Dashboard** com totais de leads, oportunidades e valores em pipeline
4. Acessar **Leads por Vendedor** para avaliar a performance individual
5. Acessar **Pipeline Geral** para visão consolidada por etapa e por vendedor
6. Acessar o Django Admin (modo leitura) para consultas detalhadas

O gestor visualiza todos os dados mas **não pode** criar, editar ou excluir registros.

## Fluxo do admin

1. Acessar o Django Admin em `/admin/`
2. Ativar ou inativar clientes provisórios
3. Visualizar todos os clientes, oportunidades e interações
4. Gerenciar usuários e perfis
5. Acesso total às telas de gestão

## Perfis e responsabilidades

| Perfil | Responsabilidades | Acessos |
|--------|-------------------|---------|
| **VENDEDOR** | Prospectar leads, criar clientes provisórios, gerenciar oportunidades próprias, registrar interações | Apenas seus próprios clientes e oportunidades |
| **GESTOR** | Avaliar leads e performance, monitorar pipeline, acompanhar conversões | Visualização de todos os dados (somente leitura) |
| **ADMIN** | Ativar/inativar clientes, gerenciar usuários, configurar sistema | Acesso total ao sistema |

## Fluxo de avaliação de leads

```
[VENDEDOR cadastra cliente]
        ↓
[Cliente fica como PROVISÓRIO]
        ↓
[GESTOR avalia leads no Dashboard]
        ├── Leads por Vendedor (performance individual)
        └── Pipeline Geral (visão consolidada)
        ↓
[ADMIN ativa clientes aprovados]
        ↓
[Cliente passa para ATIVO]
        ↓
[Oportunidade pode avançar no pipeline]
```

## Etapas do Pipeline de Vendas

O Paxis CRM utiliza um pipeline simples e sequencial para acompanhar o ciclo completo de vendas. Cada oportunidade sempre se encontra em **uma única etapa**.

### Prospecção
Primeiro contato com o potencial cliente. Ainda não há demanda claramente validada, apenas interesse inicial.

Exemplos:
- Lead frio
- Indicação
- Primeiro contato via WhatsApp ou telefone

---

### Qualificação
O vendedor validou que o lead possui potencial real de compra, perfil adequado e necessidade identificada.

Exemplos:
- Confirmação de volume
- Identificação do decisor
- Pedido de cotação

---

### Proposta
Uma proposta comercial foi apresentada ao cliente.

Exemplos:
- Orçamento enviado
- Proposta formal por e-mail ou WhatsApp

---

### Negociação
Cliente demonstrou intenção de fechar, mas ainda negocia condições comerciais.

Exemplos:
- Ajuste de preço
- Negociação de prazos
- Revisão de quantidades

---

### Fechamento
Venda concluída com sucesso.

Exemplos:
- Pedido confirmado
- Contrato fechado
- Venda registrada no sistema de faturamento

---

### Perdida
Venda não realizada.

Exemplos:
- Cliente desistiu
- Preço não aprovado
- Concorrente venceu

---

## Metas Comerciais (Etapa 3)

O sistema permite definir metas mensais para cada vendedor e acompanhar o desempenho.

### Model MetaComercial

| Campo | Descrição |
|-------|-----------|
| vendedor | Usuário vendedor (FK) |
| mes | Mês da meta (1-12) |
| ano | Ano da meta |
| valor_meta | Valor monetário da meta |
| criado_por | Admin que criou a meta |

**Regra:** Apenas UMA meta por vendedor por mês/ano (constraint unique).

### Regras de Cálculo

**Realizado:**
- Soma de `valor_estimado` das oportunidades com etapa = FECHAMENTO
- Filtrado pelo mês/ano em que a oportunidade foi fechada (`atualizado_em`)

**Pipeline:**
- Soma de `valor_estimado` das oportunidades abertas (etapa != FECHAMENTO e != PERDIDA)
- Filtrado pelo mês/ano de criação da oportunidade

**Status:**
| Status | Condição |
|--------|----------|
| OK | Pipeline >= 1,5x a meta |
| ATENÇÃO | Pipeline >= meta |
| RISCO | Pipeline < meta |

### Quem pode ver o quê

| Perfil | Acesso |
|--------|--------|
| **VENDEDOR** | Apenas sua própria meta (`/sales/minha-meta/`) |
| **GESTOR** | Metas de todos os vendedores (`/sales/metas/`) |
| **ADMIN** | Metas de todos + pode criar/editar metas no Django Admin |

### URLs

- `/sales/minha-meta/` — Vendedor vê sua meta
- `/sales/metas/` — Gestor/Admin vê todas as metas

## Follow-up e Disciplina Comercial (Etapa 4)

O sistema de follow-up garante que nenhuma oportunidade fique esquecida.

### Campos de Follow-up

| Campo | Descrição |
|-------|-----------|
| proxima_acao | Descrição da próxima ação a realizar (CharField, max 200) |
| data_follow_up | Data prevista para o próximo contato (DateField, opcional) |

### Status do Follow-up

| Status | Condição |
|--------|----------|
| EM_DIA | data_follow_up > hoje |
| HOJE | data_follow_up == hoje |
| ATRASADO | data_follow_up < hoje |
| SEM_DATA | data_follow_up é None |

### Funcionalidades

**Minhas Pendências (Vendedor):**
- Lista oportunidades do vendedor com follow-up atrasado ou para hoje
- Ordenado por mais atrasadas primeiro
- Exibe: cliente, etapa, próxima ação, data follow-up, dias em atraso

**Oportunidades sem Follow-up (Gestor/Admin):**
- Lista oportunidades sem data de follow-up OU paradas há X dias
- Parâmetro configurável de dias (default: 7)
- Exibe: cliente, vendedor, etapa, dias sem movimentação

### Permissões

| Ação | Vendedor | Gestor | Admin |
|------|----------|--------|-------|
| Editar follow-up | Sim (suas oportunidades) | Não | Não |
| Ver pendências próprias | Sim | — | — |
| Ver oportunidades sem follow-up | Não | Sim | Sim |

### URLs

- `/sales/minhas-pendencias/` — Vendedor vê suas pendências
- `/sales/oportunidades-sem-followup/` — Gestor/Admin monitora disciplina comercial
- `/sales/oportunidade/<pk>/followup/` — Editar follow-up de uma oportunidade

## Lembretes e Alertas (Etapa 5)

Sistema de lembretes visuais e e-mail para sustentar a disciplina comercial.

### Lembrete Visual (Vendedor)

No dashboard do vendedor, exibe aviso quando há oportunidades com follow-up para hoje.

### E-mail de Lembrete

- Enviado diariamente via management command
- Máximo de 1 e-mail por vendedor por dia
- Apenas quando há follow-up para o dia atual
- Conteúdo simples, sem detalhes comerciais

### Alerta Visual (Gestor)

No dashboard do gestor, exibe alerta quando há:
- Oportunidades sem data_follow_up
- Oportunidades paradas há mais de 7 dias

### Management Command

```bash
# Enviar lembretes de follow-up
python manage.py send_followup_reminders

# Modo simulação (sem enviar e-mails)
python manage.py send_followup_reminders --dry-run
```

Recomenda-se agendar execução diária via cron ou Task Scheduler.

### Configuração de E-mail

Variáveis de ambiente para configurar o envio:

| Variável | Descrição | Default |
|----------|-----------|---------|
| EMAIL_BACKEND | Backend de e-mail | console (dev) |
| EMAIL_HOST | Servidor SMTP | localhost |
| EMAIL_PORT | Porta SMTP | 587 |
| EMAIL_USE_TLS | Usar TLS | True |
| EMAIL_HOST_USER | Usuário SMTP | — |
| EMAIL_HOST_PASSWORD | Senha SMTP | — |
| DEFAULT_FROM_EMAIL | Remetente | Praxis CRM |

### Quem recebe o quê

| Tipo | Vendedor | Gestor | Admin |
|------|----------|--------|-------|
| Lembrete visual | Sim | Não | Não |
| E-mail de follow-up | Sim | Não | Não |
| Alerta de disciplina | Não | Sim | Sim |

## Decisões de arquitetura

- **Settings split**: `config/settings/base.py` com configurações comuns, `dev.py` para desenvolvimento (SQLite), `prod.py` para produção (PostgreSQL via variáveis de ambiente)
- **Perfil como model separado**: `OneToOneField` para `User` com signal `post_save` para criação automática, evitando customizar `AbstractUser`
- **Services.py**: Regras de negócio isoladas em `services.py` por app. Views chamam services, services manipulam models
- **Enums centralizados**: Todos em `apps/core/enums.py` usando `models.TextChoices`
- **Filtro por vendedor**: Implementado nos querysets das views via mixin
- **Bootstrap 5 via CDN**: Sem necessidade de npm/webpack
