# ADR-038: WHATSAPP ANTI-BAN & BULK SPAM PREVENTION ARCHITECTURE

> **Status**: APPROVED & INVARIANT ENFORCED  
> **Date**: 2026-08-20  
> **Author**: Aria (Principal Enterprise Architect) & Selena (`09_Team_Secretary`)  
> **Target Streams**: Stream 2 (AI Multi-Agent Engine - Atlas), Stream 3 (Async Queue - Bruno), Stream 5 (DevSecOps - Sentinel)  

---

## 1. Context & Problem Statement

Sending identical or static text messages to multiple WhatsApp recipients (leads or test contacts) triggers automated anti-spam heuristic filters on WhatsApp / Meta networks, leading to immediate account flags, temporary bans, or permanent instance blocks (`bulk spam detection`).

To ensure total operational resilience for **APEX Revenue SDR OS**, we must enforce system-level rules and software mechanisms that prevent sending duplicate message content to multiple targets.

---

## 2. Architectural Invariants & Rules

### Rule 1: Zero Duplicate Mass Dispatch (Dynamic Message Variation)
- **Mandatory Content Variation**: It is strictly forbidden to send the exact same text string to more than one phone number.
- **Dynamic Variation Techniques**:
  1. **Lead Personalization**: Inject specific context (`{lead_name}`, `{company_name}`, `{custom_greeting}`).
  2. **LLM Variation Generator / Spintax Jitter**: Automatically rephrase non-essential parts of the message (synonym replacement, clause restructuring, variable opening/closing signatures).
  3. **Randomized Salutations & Closings**: Rotate salutations (`"Olá"`, `"Tudo bem"`, `"Oi"`, `"Como vai"`) and sign-offs (`"Abraços"`, `"Atenciosamente"`, `"Qualquer dúvida me avise"`).

### Rule 2: Anti-Pattern & Jitter Controls
- **Rate Limits**: Maximum 1 message per 3-5 seconds across all tasks.
- **Human Typing Jitter**: Inject randomized `composing` delay ($2\text{s} - 6\text{s}$) prior to message dispatch.
- **24-Hour Window**: Block freeform outreach after 24 hours of user inactivity (enforcing approved HSM templates).

---

## 3. Implementation Blueprint

- **Service Layer**: `ZAPIService` and `app/services/anti_spam.py` implement `apply_dynamic_variation(message: str, lead_name: str) -> str`.
- **Async Queue Workers**: `Taskiq` workers MUST route multi-recipient campaigns through the variation engine before invoking Z-API `send_text`.

---

## 4. Operational Directives for Subagents

- **Atlas (`02_AI_Systems_Engineer`)**: Configure LangGraph prompts to generate uniquely phrased variations for each lead.
- **Bruno (`03_Backend_Async_Engineer`)**: Enforce variation check in Taskiq outreach queues.
- **Quinn (`06_QA_Harness_Director`)**: Add automated QA assertion in `tests/test_whatsapp_inbound_outbound_tester.py` verifying that bulk outbound payloads are 100% unique across recipients.
