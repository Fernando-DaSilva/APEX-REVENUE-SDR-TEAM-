# DESIGN DIRECTIVE — OPERATIONAL COLOR SEMANTICS & FUNCTIONAL UI

> **Mandatory Rule for Design & Frontend Team (Fiona & Stream 4)**  
> **Status**: APPROVED & MANDATORY  
> **Directive Origin**: Fernando / Selena (Human Liaison)  
> **Scope**: `01_SDR_Prototype`, `app/web/`, Design Tokens & UI Components

---

## 1. Core Principle (Mandatory Architectural Invariant)

> **"Cores devem ter significados e uso funcional nos aplicativos."**

Colors must never be used purely as arbitrary decorative elements. In all components, applications, and dashboards of the **Revenue SDR OS**, every visual color coding must represent a clear **Operational Status** that allows users to assess state and intent at a glance without reading text.

---

## 2. Standard Operational Color Mapping Matrix

| Status Operational Category | Semantic Class | Visual Color Code | Operational Meaning | System Trigger Associated |
|---|---|---|---|---|
| **Confirmada / Confirmado** | `success` | 🟢 Emerald / Green | Agendamento confirmado e ativo | Lembrete de 24h & 1h preparado |
| **Reagendada / Reagendado** | `info` | 🔵 Ocean / Blue | Horário alterado / Novo slot reservado | Gatilho de re-confirmação ativado |
| **No-Show / Cancelado** | `error` | 🔴 Crimson / Red | Lead faltou ou cancelou compromisso | Cadência No-Show Recovery disparada |
| **Pendente / A Confirmar** | `warning` | 🟡 Amber / Orange | Aguardando confirmação ou resposta | Alerta de Follow-up pré-reunião |
| **Concluída / Finalizada** | `neutral` | 🩶 Slate / Gray | Reunião realizada com sucesso | Registro de notas & qualificação |

---

## 3. Prototype Implementation Reference (`01_SDR_Prototype`)

In `01_SDR_Prototype/index.html`, the calendar event rendering has been refactored to enforce this standard via Alpine.js reactivity:

```javascript
getEventBadgeStyle(evt) {
  if (!evt) return 'bg-base-200 text-base-content border border-base-300';
  const st = evt.status || '';
  if (st === 'confirmed') return 'bg-success/20 text-success border border-success/30';
  if (st === 'rescheduled') return 'bg-info/20 text-info border border-info/30';
  if (st === 'no_show' || st === 'noshow' || st === 'cancelled') return 'bg-error/20 text-error border border-error/30';
  if (st === 'scheduled' || st === 'pending') return 'bg-warning/20 text-warning border border-warning/30';
  if (st === 'completed') return 'bg-neutral/40 text-base-content/80 border border-base-300';
  return 'bg-primary/20 text-primary border border-primary/30';
}
```

### Dynamic Visual Behaviors:
- **Month View Grid**: Event chips dynamically update color on status change in modal.
- **Week View Grid**: Event blocks reflect exact operational color code (`bg-success/20`, `bg-info/20`, `bg-error/20`).
- **Day View Timeline**: Reunião cards display matching operational borders and background hues.
- **List View**: Left border accent (`border-l-4`) reflects instant status changes.

### 3.1 Top Metrics Banner — Operational Scenario Totals
At the top of the calendar dashboard, a 5-column grid must present totals for **all possible scenarios** with explicit color styles:
- 🟢 **Confirmadas**: `bg-success/20 text-success border border-success/30`
- 🔵 **Reagendadas**: `bg-info/20 text-info border border-info/30`
- 🔴 **No-Show / Canceladas**: `bg-error/20 text-error border border-error/30`
- 🟡 **Pendentes / A Confirmar**: `bg-warning/20 text-warning border border-warning/30`
- 🩶 **Concluídas**: `bg-neutral/40 text-base-content/80 border border-base-300`

---

## 4. Directive Enforcement Checklist for Design & Frontend Engineers

- [x] **No static color assignment**: Event cards and status indicators must bind dynamically to status variables.
- [x] **Top Header Totals**: All 5 operational scenarios must be displayed explicitly at the top of the view with real-time totals and matching color classes.
- [x] **Modal feedback sync**: Altering status in detail modals (e.g. `✅ Confirmar`, `🔄 Reagendar`, `❌ No-Show`) must immediately re-render visual color in parent containers/calendars.
- [x] **Consistency across components**: The same status color matrix applies to Leads Table, Kanban pipeline cards, Calendar events, and Notification badges.
