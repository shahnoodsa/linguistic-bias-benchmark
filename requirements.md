# Requirements

## Goal
Build a tool that evaluates linguistic bias in LLM responses to legal scenario prompts,
comparing English and German outputs for the same scenarios.

## User Stories
- As a researcher, I want to test whether AI describes legal actors differently in English vs German.
- As a student, I want to compare tone, framing, and assumed guilt across language conditions.
- As a developer, I want simple paired outputs that make cross-language differences visible.

## Features
- Input prompts in both English and German (paired — same scenario, both languages)
- Generate responses for each prompt via Ollama (tinyllama)
- Save outputs as labelled .txt files
- Provide a structured analysis template for qualitative comparison

## Prompt Design
- Category A: Neutral legal actor descriptions (suspect, defendant, victim, judge)
- Category B: Demographic variation (gender, nationality, name)
- Category C: High-stakes framing (accused of serious crime)
- Each prompt exists in both English and German versions

## Acceptance Criteria
- Tool runs 24 prompts (12 scenarios × 2 languages)
- Each response saved with language tag in filename
- Summary file lists all prompt pairs
- Analysis template covers: tone, assumed guilt, social framing, language register, empathy level