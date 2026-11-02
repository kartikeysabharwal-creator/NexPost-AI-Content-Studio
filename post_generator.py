import re
import time
from llm_helper import get_llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 4 concise impactful lines (under 50 words)"
    if length == "Medium":
        return "5 to 9 structured lines with clear spacing (50 to 120 words)"
    if length == "Long":
        return "10 to 15 storytelling lines, formatted with bullet points & headers (120 to 250 words)"
    return "6 to 10 lines"

VARIATION_PERSONAS = {
    "Professional": {
        "title": "Executive & Thought Leadership",
        "description": "Crisp, data-backed insights, polished corporate phrasing, and actionable leadership takeaways.",
        "style_guide": "Maintain authority, cite clear frameworks or logical takeaways, avoid fluff, use structured formatting."
    },
    "Storytelling": {
        "title": "Narrative & Personal Journey",
        "description": "Vulnerable, relatable storytelling that hooks emotionally and shares behind-the-scenes lessons.",
        "style_guide": "Begin with a personal scene or pivot moment, highlight the challenge, reveal the unexpected epiphany, conclude with inspirational wisdom."
    },
    "Engaging": {
        "title": "Viral Hook & Conversation Starter",
        "description": "Punchy lines, contrarian perspectives, curiosity gaps, and debate-provoking questions.",
        "style_guide": "Use a bold contrarian or intriguing first line, short readable paragraphs, and an irresistible comment-triggering question at the end."
    }
}

def generate_variation(variation_type, length, language, tag, tone="Professional", audience="General Tech Community", custom_prompt="", model_name="openai/gpt-oss-120b", temperature=0.7):
    """
    Generates a targeted variation (Professional, Storytelling, or Engaging).
    """
    start_time = time.time()
    llm = get_llm(model_name=model_name, temperature=temperature)
    
    length_str = get_length_str(length)
    persona = VARIATION_PERSONAS.get(variation_type, VARIATION_PERSONAS["Professional"])
    
    language_instruction = (
        "Write in natural Hinglish (a seamless, catchy blend of conversational Hindi words in Latin/English alphabet and English, widely popular on Indian LinkedIn)."
        if language == "Hinglish"
        else "Write in articulate, natural English."
    )

    system_prompt = f"""
You are an elite LinkedIn content architect and viral strategist specializing in: {persona['title']}.
Task: Generate a single LinkedIn post on the given topic adopting the requested style.

[Parameters]
- Topic: {tag}
- Requested Variation Style: {variation_type} ({persona['style_guide']})
- Overall Tone: {tone}
- Target Audience: {audience}
- Length Constraint: {length_str}
- Language: {language_instruction}
{f'- Specific Requirement / Angle: {custom_prompt}' if custom_prompt else ''}

[Structure Requirements]
1. Line 1 Hook: High-impact opening sentence that prevents skipping.
2. Body: Paced with clean line breaks (no monolithic blocks of text).
3. Value / Takeaway: Concrete, memorable insight.
4. Closing: Strong conversation-starting call-to-action (CTA).
5. Hashtags: 3 to 5 targeted hashtags at the very end.
6. Important: Return ONLY the post text. No introductory remarks, labels, or meta commentary.
"""

    examples = few_shot.get_filtered_posts(length, language, tag)
    if examples:
        system_prompt += "\n[Exemplars Conditioned From Top-Performing Content]\n"
        for i, post in enumerate(examples[:2]):
            system_prompt += f"\n--- Exemplar {i+1} ---\n{post.get('text', '')}\n"

    response = llm.invoke(system_prompt)
    content = response.content.strip()
    
    if content.startswith("```markdown"):
        content = content[11:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    latency = round(time.time() - start_time, 2)
    metrics = evaluate_content_quality(content)
    metrics["latency"] = latency
    
    return {
        "variation_type": variation_type,
        "content": content,
        "metrics": metrics,
        "model_name": model_name
    }

def generate_all_variations(length, language, tag, tone="Professional", audience="General Tech Community", custom_prompt="", model_name="openai/gpt-oss-120b", temperature=0.7):
    """Generates all 3 post variations (Professional, Storytelling, Engaging)."""
    results = {}
    for var_type in ["Professional", "Storytelling", "Engaging"]:
        results[var_type] = generate_variation(
            variation_type=var_type,
            length=length,
            language=language,
            tag=tag,
            tone=tone,
            audience=audience,
            custom_prompt=custom_prompt,
            model_name=model_name,
            temperature=temperature
        )
    return results

def rewrite_content(original_text, rewrite_goal, custom_instruction="", model_name="openai/gpt-oss-120b", temperature=0.6):
    """
    AI Content Rewriter to upgrade grammar, viral hooks, hashtags, readability, or audience resonance.
    """
    start_time = time.time()
    llm = get_llm(model_name=model_name, temperature=temperature)
    
    goal_directives = {
        "Sharpen Opening Hook": "Transform the first 1-2 lines into an irresistible scroll-stopper that sparks immense curiosity.",
        "Fix Grammar & Flow": "Correct all grammatical subtleties, refine cadence, and elevate vocabulary while preserving the original voice.",
        "Optimize for Viral Engagement": "Reformat with whitespace, conversational cadence, bullet points, and an explicit comment-driving question.",
        "Condense & Make Punchy": "Cut wordiness by 40%, remove passive phrasing, and make every sentence deliver punchy impact.",
        "Enhance Hashtags & SEO": "Append the most strategic, high-relevance hashtags and keyword phrases for LinkedIn algorithm indexing.",
        "Translate to Natural Hinglish": "Rewrite the post into engaging conversational Hinglish (Hindi phrases in Roman script + English) popular among Indian tech professionals."
    }
    
    directive = goal_directives.get(rewrite_goal, "Improve the clarity and engagement of the post.")
    
    prompt = f"""
You are an expert LinkedIn copy editor and growth engineer.
Rewrite the following LinkedIn post according to the specified objective.

[Rewriting Objective]: {rewrite_goal}
{directive}
{f'[Custom User Note]: {custom_instruction}' if custom_instruction else ''}

[Original Post]:
\"\"\"{original_text}\"\"\"

[Strict Rule]: Return ONLY the rewritten post ready for publishing. Do not explain your changes or add meta-text.
"""
    response = llm.invoke(prompt)
    rewritten = response.content.strip()
    
    if rewritten.startswith("```markdown"):
        rewritten = rewritten[11:]
    elif rewritten.startswith("```"):
        rewritten = rewritten[3:]
    if rewritten.endswith("```"):
        rewritten = rewritten[:-3]
    rewritten = rewritten.strip()
    
    latency = round(time.time() - start_time, 2)
    return rewritten, latency

def evaluate_content_quality(text):
    """
    Transparent, multi-dimensional Content Quality Score (0-100)
    Breakdown:
    1. Hook Strength (25%): Opening line brevity, intrigue, numbers, questions.
    2. Readability & Structure (30%): Line distribution, white space, clean breaks.
    3. Call-to-Action (CTA) (25%): Question marks, explicit invitation to reply/comment.
    4. Keyword & Hashtag Optimization (20%): Relevant hashtags and keyword presence.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    line_count = len(lines)
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    char_count = len(text)
    
    # 1. Hook Score (out of 100)
    hook_score = 65
    if lines:
        first_line = lines[0]
        first_line_words = len(re.findall(r'\b\w+\b', first_line))
        if 4 <= first_line_words <= 18:
            hook_score += 15
        if any(c in first_line for c in ["?", "!", "—", ":"]):
            hook_score += 10
        if any(w in first_line.lower() for w in ["how", "why", "stop", "never", "secret", "lessons", "step", "hack", "mistake", "truth"]):
            hook_score += 10
    hook_score = min(hook_score, 98)
    
    # 2. Readability Score (out of 100)
    readability_score = 70
    if 4 <= line_count <= 18:
        readability_score += 15
    if 40 <= word_count <= 250:
        readability_score += 10
    # Average words per line (avoid massive unbroken blocks)
    avg_words_per_line = word_count / max(line_count, 1)
    if avg_words_per_line <= 18:
        readability_score += 5
    readability_score = min(readability_score, 98)
    
    # 3. Call To Action (CTA) Score (out of 100)
    cta_score = 60
    if "?" in text:
        cta_score += 15
    if any(phrase in text.lower() for phrase in ["comment", "share your", "what do you think", "thoughts?", "agree?", "let me know", "drop a"]):
        cta_score += 20
    cta_score = min(cta_score, 99)
    
    # 4. Hashtag / Discoverability Score (out of 100)
    hashtag_count = text.count("#")
    if 2 <= hashtag_count <= 6:
        hashtag_score = 95
    elif hashtag_count == 1:
        hashtag_score = 75
    elif hashtag_count > 6:
        hashtag_score = 70 # over-tagged
    else:
        hashtag_score = 40 # missing hashtags
        
    overall_score = round(
        (hook_score * 0.25) +
        (readability_score * 0.30) +
        (cta_score * 0.25) +
        (hashtag_score * 0.20)
    )
    
    read_time_sec = max(round((word_count / 210) * 60), 6)
    
    return {
        "overall_score": overall_score,
        "hook_score": hook_score,
        "readability_score": readability_score,
        "cta_score": cta_score,
        "hashtag_score": hashtag_score,
        "words": word_count,
        "characters": char_count,
        "lines": line_count,
        "hashtags": hashtag_count,
        "read_time_seconds": read_time_sec
    }
