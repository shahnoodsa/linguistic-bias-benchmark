# run_benchmark.py
# Linguistic Bias Benchmark — AI in Law & Criminal Justice
# Author: SHAHNOOD SAEED
# Course: Gender, Diversity & AI — University of Klagenfurt, SS2026
#
# USAGE:
#   1. Install Ollama from https://ollama.com
#   2. Open Command Prompt and run:  ollama pull tinyllama
#   3. Open Command Prompt and run:  ollama serve
#   4. Open a NEW Command Prompt, navigate to this folder, and run:
#        python run_benchmark.py
#
#   No API key needed. Completely free. All data stays on your computer.
#
# WHAT THIS SCRIPT DOES:
#   - Reads 24 paired prompts (12 scenarios × English + German) from prompts.py
#   - Sends each prompt to tinyllama running locally via Ollama
#   - Saves each response as a labelled .txt file in the outputs/ folder
#   - Generates a summary index and a structured analysis template
#   - Pairs EN/DE responses in the template so cross-language comparison is easy

import os
import json
import urllib.request
from datetime import datetime
from prompts import PROMPTS

# ── Settings ──────────────────────────────────────────────────────────────────

OLLAMA_URL  = "http://localhost:11434/api/generate"
MODEL_NAME  = "llama3"
OUTPUT_DIR  = "outputs"

# ── Setup ─────────────────────────────────────────────────────────────────────

os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print()
print("=" * 60)
print("  Linguistic Bias Benchmark — AI in Law & Criminal Justice")
print("=" * 60)
print(f"  Started : {timestamp}")
print(f"  Model   : {MODEL_NAME} via Ollama (free, local)")
print(f"  Prompts : {len(PROMPTS)} total ({len(PROMPTS)//2} EN + {len(PROMPTS)//2} DE pairs)")
print("=" * 60)
print()

# ── Helper ────────────────────────────────────────────────────────────────────

def ask_ollama(prompt_text: str) -> str:
    """Send a single prompt to Ollama and return the response as a string."""
    payload = json.dumps({
        "model":  MODEL_NAME,
        "prompt": prompt_text,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["response"].strip()
    except urllib.error.URLError:
        raise ConnectionError(
            "Cannot reach Ollama. Make sure it is running:\n"
            "  Open Command Prompt and type:  ollama serve"
        )

# ── Run prompts ───────────────────────────────────────────────────────────────

results = []

for i, (label, prompt_text) in enumerate(PROMPTS, start=1):
    filename = f"{label}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Detect language from label suffix for display
    lang_tag = "🇬🇧 EN" if label.endswith("_EN") else "🇩🇪 DE"
    print(f"  [{i:02d}/{len(PROMPTS)}] {lang_tag}  {label}")

    try:
        response_text = ask_ollama(prompt_text)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"LABEL   : {label}\n")
            f.write(f"LANGUAGE: {'English' if label.endswith('_EN') else 'German'}\n")
            f.write(f"PROMPT  : {prompt_text}\n")
            f.write(f"MODEL   : {MODEL_NAME}\n")
            f.write(f"DATE    : {timestamp}\n")
            f.write("-" * 60 + "\n\n")
            f.write(response_text)

        results.append({
            "label":    label,
            "lang":     "EN" if label.endswith("_EN") else "DE",
            "prompt":   prompt_text,
            "filename": filename,
            "status":   "OK",
            "preview":  response_text[:100].replace("\n", " ") + "..."
        })
        print(f"           ✓  Saved → {OUTPUT_DIR}/{filename}")

    except ConnectionError as e:
        print(f"\n  ERROR: {e}\n")
        results.append({
            "label":    label,
            "lang":     "EN" if label.endswith("_EN") else "DE",
            "prompt":   prompt_text,
            "filename": filename,
            "status":   "ERROR — Ollama not reachable",
            "preview":  ""
        })

    except Exception as e:
        print(f"           ✗  Error: {e}")
        results.append({
            "label":    label,
            "lang":     "EN" if label.endswith("_EN") else "DE",
            "prompt":   prompt_text,
            "filename": filename,
            "status":   f"ERROR: {e}",
            "preview":  ""
        })

# ── Summary file ──────────────────────────────────────────────────────────────

summary_path = os.path.join(OUTPUT_DIR, "summary.txt")

with open(summary_path, "w", encoding="utf-8") as f:
    f.write("LINGUISTIC BIAS BENCHMARK — SUMMARY\n")
    f.write(f"Run at : {timestamp}\n")
    f.write(f"Model  : {MODEL_NAME}\n")
    f.write(f"Prompts: {len(PROMPTS)} ({len(PROMPTS)//2} EN + {len(PROMPTS)//2} DE)\n")
    f.write("=" * 60 + "\n\n")

    for r in results:
        f.write(f"[{r['status']}] [{r['lang']}] {r['label']}\n")
        f.write(f"  Prompt  : {r['prompt']}\n")
        f.write(f"  File    : {OUTPUT_DIR}/{r['filename']}\n")
        if r["preview"]:
            f.write(f"  Preview : {r['preview']}\n")
        f.write("\n")

print(f"\n  → {summary_path}")

# ── Analysis template ─────────────────────────────────────────────────────────
# Groups EN/DE pairs together so comparison is immediate.
# One section per PAIR (not per individual prompt).

analysis_path = os.path.join(OUTPUT_DIR, "analysis_template.md")

if not os.path.exists(analysis_path):

    # Build a list of unique base labels (strip _EN / _DE suffix)
    seen = []
    for r in results:
        base = r["label"][:-3]   # remove _EN or _DE
        if base not in seen:
            seen.append(base)

    with open(analysis_path, "w", encoding="utf-8") as f:
        f.write("# Analysis Notes\n")
        f.write("## Linguistic Bias Benchmark — AI in Law & Criminal Justice\n")
        f.write(f"_Author: [Your Name] — started {timestamp}_\n\n")
        f.write("---\n\n")

        f.write("## How to Use This Template\n\n")
        f.write("For each prompt pair below:\n")
        f.write("1. Open the EN .txt file and the DE .txt file side by side\n")
        f.write("2. Read both responses carefully\n")
        f.write("3. Fill in each dimension for both languages\n")
        f.write("4. Write your key observation — what is *different* and what does it mean?\n\n")
        f.write("### Analysis Dimensions\n\n")
        f.write("| Dimension | What to look for |\n")
        f.write("|---|---|\n")
        f.write("| **Tone** | Neutral / sympathetic / accusatory / clinical / paternalistic |\n")
        f.write("| **Assumed guilt** | Does the AI treat the person as guilty before trial? |\n")
        f.write("| **Social framing** | Are family, poverty, migration mentioned? More in one language? |\n")
        f.write("| **Language register** | Formal / legalistic / emotive / simplified / othering |\n")
        f.write("| **Empathy level** | Is compassion shown? More for some identities than others? |\n\n")
        f.write("---\n\n")

        for base in seen:
            # Find EN and DE records for this base
            en = next((r for r in results if r["label"] == base + "_EN"), None)
            de = next((r for r in results if r["label"] == base + "_DE"), None)

            f.write(f"## {base}\n\n")

            if en:
                f.write(f"**EN prompt:** {en['prompt']}\n")
                f.write(f"**EN file:** `outputs/{en['filename']}`\n\n")
            if de:
                f.write(f"**DE prompt:** {de['prompt']}\n")
                f.write(f"**DE file:** `outputs/{de['filename']}`\n\n")

            f.write("### Tone\n")
            f.write("- EN: \n")
            f.write("- DE: \n\n")

            f.write("### Assumed guilt\n")
            f.write("- EN: \n")
            f.write("- DE: \n\n")

            f.write("### Social framing\n")
            f.write("- EN: \n")
            f.write("- DE: \n\n")

            f.write("### Language register\n")
            f.write("- EN: \n")
            f.write("- DE: \n\n")

            f.write("### Empathy level\n")
            f.write("- EN: \n")
            f.write("- DE: \n\n")

            f.write("### Key observation (what is different and what does it mean?)\n\n")
            f.write("> _Write 2–3 sentences connecting the EN/DE difference to theory "
                    "(situated knowledges, gender scripts, intersectionality)._\n\n")
            f.write("---\n\n")

    print(f"  → {analysis_path}")

# ── Done ──────────────────────────────────────────────────────────────────────

ok_count  = sum(1 for r in results if r["status"] == "OK")
err_count = len(results) - ok_count

print()
print("=" * 60)
print(f"  Done!  {ok_count} responses saved,  {err_count} errors.")
print()
print(f"  outputs/summary.txt           — full prompt index")
print(f"  outputs/analysis_template.md  — fill this in for your analysis")
print(f"  outputs/[label].txt           — individual AI responses (24 files)")
print("=" * 60)
print()

if err_count > 0:
    print("  Troubleshooting:")
    print("  • 'Ollama not reachable' → open Command Prompt and type: ollama serve")
    print("  • 'No module named prompts' → make sure you are in the correct folder")
    print("  • 'python not found' → try: py run_benchmark.py")
    print()
