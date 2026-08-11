# SHARED SKILL: Hypermedia UI Design & Zap Copilot Integration

## Core Principles

- **Tech Stack**: Jinja2 HTML templates + HTMX (partial DOM updates) + Alpine.js (local reactive client state). Vendored assets (no CDN dependency).
- **White-Label Theme Engine**: 5 curated themes (`Obsidian Night`, `Emerald Garden`, `Ocean Breeze`, `Sakura Bloom`, `Amber Warmth`) configured dynamically per organization.
- **Zap Web Copilot Integration**:
  - Desconstructed from `02_ZAP_Prototype`.
  - 3-Column Layout: Column 1 (Lead List & Filter), Column 2 (Chat Stream & Mode Switcher), Column 3 (DHS Sentiment Gauge via Chart.js + RAG AI Suggestions).
  - Chart.js Fix: Proper canvas destruction on DOM swap to eliminate memory leaks.
