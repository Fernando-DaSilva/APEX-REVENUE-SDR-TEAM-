# CONVERSATION RECORD 19 — WHATSAPP ANTI-BAN & BULK SPAM PREVENTION RULE

> **Date**: 2026-08-20  
> **Originator**: Fernando (Executive Leader / Admin)  
> **Liaison**: Selena (`09_Team_Secretary`)  
> **Recipients**: All Subagents (Aria `01`, Atlas `02`, Bruno `03`, Fiona `04`, Sentinel `05`, Quinn `06`, Silas `07`, Pax `08`, Helena `10`)  
> **Status**: RULE ENACTED & ARCHITECTURAL INVARIANT UPDATED  

---

## 1. Directive Description

Fernando alerted the team regarding WhatsApp account flagging:
> *"Selena, The account is blocked as considered a bulk spam. We need to find ways to avoid this, for instance, when sending a message to more than one person, change the message text, or it will be considered spam. Add this knowledge to our Team and tell them to add this Rule/Alert in out architecture documents."*

---

## 2. Team Architectural Updates

1. **Team Charter Rule Update**:
   - Updated Invariant #15 in `TEAM_CHARTER.md`:
     > **15. Meta WhatsApp 24h Window & Anti-Ban/Anti-Bulk-Spam Compliance**: Freeform messages blocked after 24h window (forcing approved HSM templates). Outbound rate limits (1 msg/3-5s) with human jitter (2s-6s) and `composing` status. **STRICT BULK SPAM RULE**: Identical message text sent to multiple leads is strictly forbidden to prevent WhatsApp account spam blocks. All multi-recipient dispatches MUST apply dynamic content variation (LLM spintax/synonym jitter, lead name personalization, and randomized opening/closing phrases).

2. **Architecture Decision Record Created**:
   - Authored `01_Enterprise_Architect/ADR_038_WHATSAPP_ANTI_BAN_BULK_SPAM_PROTECTION.md` (Aria & Selena).
   - Mandatory rules established:
     - Zero static duplicate blasts across multiple targets.
     - Automated Spintax synonym replacement & LLM message rephrasing.
     - Lead context personalization (`{name}`, `{company}`).
     - Randomized opening greetings and closing signatures.

3. **Software Engine Implementation**:
   - Implemented `app/services/anti_spam.py` (`generate_dynamic_variation`) for dynamic content variation.

4. **QA Test Gate Verification**:
   - Added `test_anti_bulk_spam_dynamic_content_variation` in `tests/test_whatsapp_inbound_outbound_tester.py` (Quinn - QA Director).
   - Test suite executing 13/13 tests passing 100% OK.
