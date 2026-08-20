# DIRECTIVA DE QUALIDADE — CRIVO DE TESTES VISUAIS E REGRESSÃO DE COMPONENTES UI

**Data:** 13 de Agosto de 2026  
**Solicitante:** Diretoria Executiva / Selena (Liderança do Time)  
**Destinatário:** Quinn (Diretor de QA Harness & Testes)  

---

### 1. Diagnóstico do Problema Identificado
Identificamos uma falha no crivo de qualidade referente ao alternador de visões do componente de **Agenda & Calendário Operacional** (`01_SDR_Prototype/index.html`).

* **Sintoma:** Os seletores de visão **Semana**, **Dia** e **Lista** apresentavam exatamente o mesmo layout em lista, sem nenhuma alternância estrutural de interface.
* **Causa Raiz:** Ausência de renderização dedicada nos contêineres Alpine.js para as chaves `calendarViewMode === 'week'` e `calendarViewMode === 'day'`.

---

### 2. Ação Corretiva Aplicada na Interface
A interface do protótipo foi atualizada com 4 layouts completamente distintos e responsivos:

1. **Visão Mês (`calendarViewMode === 'month'`):** Grid mensal (Agosto 2026) destacando dia atual (13★) e eventos agregados.
2. **Visão Semana (`calendarViewMode === 'week'`):** Grid de 7 colunas (Segunda a Domingo) com cartões de reuniões alocados por dia (ex.: Quinta-feira 13/08 em destaque primário).
3. **Visão Dia (`calendarViewMode === 'day'`):** Linha do tempo hora a hora (08:00 às 18:00) mapeando compromissos com badges de status, hosts e atalhos diretos de videoconferência.
4. **Visão Lista (`calendarViewMode === 'agenda'`):** Stream em lista cronológica com filtros ativos de Host e Status.

---

### 3. Novas Diretrizes Obrigatórias para a Equipe de Qualidade (QA)

A partir deste sprint, o time de Qualidade liderado por Quinn deverá reforçar o crivo de validação:

- [x] **Crivo de Comportamento Dinâmico (UI State Matrix):** Todo seletor ou aba (`tabs`, `viewModes`, `filters`) deve passar por teste unitário/visual em todos os seus estados (`Mês`, `Semana`, `Dia`, `Lista`) antes de ser aprovado.
- [x] **Auditoria de Componentes IDênticos:** É proibido aprovar componentes onde seletores de estado diferente renderizam layouts idênticos sem alteração funcional ou visual legível.
- [x] **Suíte de Teste de Regressão Visual (`T6.5`):** Incluída no backlog a validação automatizada dos seletores de visão.

---

*Assinado:*  
**Selena & Equipe Antigravity (SDR Software Team)**
