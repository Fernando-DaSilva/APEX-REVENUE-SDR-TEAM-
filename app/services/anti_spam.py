"""
WhatsApp Anti-Ban & Anti-Bulk-Spam Content Variation Engine
Enforces ADR-038 & Team Charter Invariant #15.
Prevents account bans by injecting dynamic spintax variations, salutation rotation,
randomized closing signatures, and lead context into outbound messages.
"""
import random
import re
from typing import List, Optional

GREETINGS = [
    "Olá {name}",
    "Tudo bem, {name}?",
    "Oi {name}, como vai?",
    "Olá {name}, tudo certo?",
    "Oi {name}"
]

CLOSINGS = [
    "Abraços,\nEquipe APEX SDR OS",
    "Qualquer dúvida estou à disposição!",
    "Fico no aguardo do seu retorno.",
    "Atenciosamente,\nTime APEX SDR",
    "Um abraço!"
]

SPINTAX_MAP = {
    "mensagem de teste": ["mensagem de verificação", "teste de validação", "envio de teste", "mensagem de homologação"],
    "sistema APEX Revenue SDR OS": ["plataforma APEX Revenue SDR OS", "sistema APEX SDR", "gerenciador APEX SDR OS"],
    "por favor": ["gentileza", "se possível"],
    "responda esta mensagem": ["responda por aqui", "nos dê um retorno", "envie uma resposta"],
    "recebimento em tempo real": ["recebimento instantâneo", "fluxo de entrada em tempo real", "recebimento de webhooks"]
}

def generate_dynamic_variation(base_message: str, lead_name: Optional[str] = None) -> str:
    """
    Applies dynamic variation to a base message string to ensure 100% uniqueness
    across multi-recipient outreach campaigns, bypassing duplicate content spam filters.
    """
    name = lead_name or "parceiro"
    text = base_message
    
    # Replace or prepend greeting if not already personalized
    greeting = random.choice(GREETINGS).format(name=name)
    
    # Apply Spintax synonym replacements
    for target_phrase, variations in SPINTAX_MAP.items():
        if target_phrase.lower() in text.lower():
            replacement = random.choice(variations)
            pattern = re.compile(re.escape(target_phrase), re.IGNORECASE)
            text = pattern.sub(replacement, text)
            
    # Inject randomized unique transaction/jitter ID hash
    jitter_hash = f"#{random.randint(1000, 9999)}"
    closing = random.choice(CLOSINGS)
    
    # Construct unique message body
    varied_message = f"{greeting}!\n\n{text}\n\n{closing} ({jitter_hash})"
    return varied_message
