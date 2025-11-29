# Math Bank Curator - Video Script

**Total Duration:** ~2:50 (under 3 minutes)

---

## SLIDE 1: Title (0:00 - 0:05)
*Visual: Title slide with emoji*

**NARRATION:**
"Math Bank Curator: An autonomous math problem generator powered by multi-agent AI."

---

## SLIDE 2: Problem Statement (0:05 - 0:17)
*Visual: Problem icons and bullet points*

**NARRATION:**
"Teachers face a critical challenge: creating quality math problems is incredibly time-consuming. Hours are spent researching and drafting each problem, creating practice variations is mentally exhausting, and there's simply no way to scale this process to meet growing student needs."

---

## SLIDE 3: Why Agents? (0:17 - 0:32)
*Visual: Comparison grid*

**NARRATION:**
"Why use agents instead of a single AI model? Because single LLMs struggle to be both creative and rigorous simultaneously, leading to errors and hallucinations. Our multi-agent system uses separation of concerns—just like a professional editorial team. The Generator focuses purely on creativity, the Validator acts as a strict independent critic, and the Scraper gathers real-world context."

---

## SLIDE 4: Architecture (0:32 - 0:47)
*Visual: Architecture diagram*

**NARRATION:**
"Our architecture follows a hierarchical multi-agent control pattern. The Orchestrator coordinates the entire workflow: the Scraper fetches content, the Generator creates variations, the Validator evaluates quality, and only problems scoring 70 or above make it into the Problem Bank. This quality gate ensures consistently high standards."

---

## SLIDE 5: Workflow (0:47 - 0:59)
*Visual: Numbered workflow steps*

**NARRATION:**
"Here's how it works: First, we scrape and parse problems from web pages, PDFs, and images. Second, we generate novel variations using few-shot learning. Third, we apply constitutional validation, scoring each problem on accuracy, correctness, clarity, and educational value. Finally, we curate only the highest quality problems."

---

## SLIDE 6: Demo #1 - Web Scraping (0:59 - 1:14)
*Visual: Demo results from AoPS*

**NARRATION:**
"Let's see it in action. Demo one: Live web scraping from Art of Problem Solving. We extracted sixteen mathematical problems—eight times more than text-only approaches—including complex geometry problems with diagrams. The generator then created a novel Chevron logo problem that scored a perfect 100 out of 100 on validation."

---

## SLIDE 7: Demo #2 - Multimodal PDF (1:14 - 1:27)
*Visual: PDF extraction results*

**NARRATION:**
"Demo two: Multimodal PDF extraction. We processed the official AMC 8 competition paper where problems exist only as scanned images. Using Gemini's vision capabilities, we successfully read diagrams directly from the images and extracted complete problem text. This multimodal boost gave us an eight-times improvement in problem extraction."

---

## SLIDE 8: Demo #3 - Generative UI (1:27 - 1:39)
*Visual: Python code example*

**NARRATION:**
"Demo three: Generative UI. Our system doesn't just generate text—it also produces Python visualization code using Matplotlib. This ensures mathematical precision with exact angles and measurements that pixel-based image generation often misses. The code generates perfect geometric diagrams programmatically."

---

## SLIDE 9: Results (1:39 - 1:49)
*Visual: Success metrics*

**NARRATION:**
"The results? One hundred percent success rate across all scenarios. HTML scraping with images: check. PDF extraction: check. Code generation: check. Every test passed with flying colors."

---

## SLIDE 10: The Build (1:49 - 2:02)
*Visual: Tech stack and features*

**NARRATION:**
"We built this using Google's Agent Development Kit on Python three-point-thirteen, powered by Gemini 3 Pro. Key innovations include constitutional AI validation with an independent critic, multimodal input and output capabilities, strict quality gate enforcement, and autonomous scraping with context awareness."

---

## SLIDE 11: Impact (2:02 - 2:12)
*Visual: Impact categories*

**NARRATION:**
"The impact is transformative. Teachers can turn hours of work into minutes and generate unlimited practice sets. Students get access to diverse, validated problems at adaptive difficulty levels. And education as a whole gains scalable, quality content for everyone."

---

## SLIDE 12: Closing (2:12 - 2:20)
*Visual: Closing slide with GitHub link*

**NARRATION:**
"Math Bank Curator: Empowering education through agents. Check it out on GitHub at github-dot-com-slash-doric9-slash-math-bank-curator. Built for the Agents For Good Kaggle Competition."

---

## PRODUCTION NOTES

### Timing Breakdown
- Title: 5 seconds
- Problem Statement: 12 seconds
- Why Agents: 15 seconds
- Architecture: 15 seconds
- Workflow: 12 seconds
- Demo 1: 15 seconds
- Demo 2: 13 seconds
- Demo 3: 12 seconds
- Results: 10 seconds
- The Build: 13 seconds
- Impact: 10 seconds
- Closing: 8 seconds
**TOTAL: 2 minutes 20 seconds** (leaves 40 seconds buffer)

### Narration Tips
1. **Pace**: Speak clearly at ~150 words per minute
2. **Tone**: Professional but enthusiastic
3. **Emphasis**: Highlight numbers (16 problems, 100%, 8x boost)
4. **Pauses**: Brief pauses between major points
5. **Energy**: Build excitement through demos, peak at results

### Visual Flow
- Each slide auto-advances with proper timing
- Smooth fade transitions
- Consistent color scheme (purple gradient)
- Clear hierarchy with large fonts
- Animations enhance but don't distract

### Audio Recommendations
1. **Background Music**: Subtle, upbeat tech music at 10-15% volume
2. **Voice Over**: Clear, professional narration
3. **Sound Effects**: Optional subtle transitions between major sections
4. **Mixing**: Voice primary, music supportive

### Optional Enhancements
- Add subtle zoom/pan on static slides
- Include screen recording of actual CLI demo
- Show real problem bank JSON files
- Display validation scores in real-time
- Add testimonial quote from educator

---

## ALTERNATIVE: LIVE DEMO VERSION

If you prefer to show actual CLI usage instead of slides, record:

1. **Setup (0:00-0:15)**: Terminal showing project structure
2. **Scrape (0:15-0:45)**: `python main.py scrape --url [URL]`
3. **Generate (0:45-1:30)**: `python main.py generate --seeds scraped_seeds.json`
4. **View (1:30-2:00)**: `python main.py view --show-solutions`
5. **Stats (2:00-2:20)**: `python main.py stats`
6. **Closing (2:20-2:30)**: GitHub repo

This shows the system actually working in real-time!
