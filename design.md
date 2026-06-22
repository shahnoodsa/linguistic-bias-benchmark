# Design

## Overview
The system runs paired prompts — English and German versions of the same legal scenario —
through tinyllama via Ollama, saves outputs, and enables qualitative cross-language comparison.

## Architecture
Prompt pairs (EN + DE) → Ollama API → Response → Save to outputs/ → Analysis template

## Tools
- Python 3
- Ollama (local, free, no API key)
- tinyllama model
- Standard library only (urllib, json, os)

## Process
1. Define prompt pairs in prompts.py (English + German, same scenario)
2. Run each through tinyllama
3. Save as labelled .txt files (e.g. A01_suspect_EN.txt / A01_suspect_DE.txt)
4. Compare paired outputs using analysis_template.md

## Design Decisions
- Same model for both languages: isolates language as the variable
- Paired structure: every English prompt has an exact German equivalent
- Simple implementation: no external libraries beyond Ollama
- Qualitative focus: depth of interpretation over statistical measurement