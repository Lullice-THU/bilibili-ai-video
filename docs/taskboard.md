# Bilibili AI Video - Task Board

## Project Phases

### M1: Data Collection (Completed ✓)
- [x] M1.1: Project initialization
- [x] M1.2: Bilibili collector implementation
- [x] M1.3: Heat calculator

### M2: Prompt Generation (In Progress)
- [x] M2.1: LLM API integration
  - [x] DeepSeek client
  - [x] Anthropic client (backup)
  - [x] Configuration management
- [x] M2.2: Prompt generation service
  - [x] PromptGenerator class
  - [x] Three template types (HOT_INTERPRET, KNOWLEDGE, ROUNDUP)
- [x] M2.3: Prompt template design
  - [x] Title suggestions (3)
  - [x] Core viewpoints (3-5)
  - [x] Video structure (opening, body, ending)
  - [x] Ending interaction
  - [x] Estimated duration
- [x] M2.4: Quality evaluation
  - [x] Basic quality scoring logic
  - [x] Prompt completeness check

### M3: Video Generation (Pending)
- [ ] M3.1: Video generation service
- [ ] M3.2: Audio/TTS integration
- [ ] M3.3: Video rendering

### M4: Publishing (Pending)
- [ ] M4.1: Bilibili upload API
- [ ] M4.2: Scheduling system

---

## Development Log

### 2026-03-02

**M2 Development - Prompt Generation Service**

Implemented the following modules:

1. **LLM Client** (`src/prompt/client.py`)
   - DeepSeekClient: Primary LLM provider
   - AnthropicClient: Backup provider
   - Unified interface via LLMClient abstract class

2. **Configuration** (`src/prompt/config.py`)
   - LLMConfig with environment variable support
   - Supported vars: LLM_PROVIDER, DEEPSEEK_API_KEY, ANTHROPIC_API_KEY, etc.

3. **Data Models** (`src/prompt/models.py`)
   - TemplateType enum (HOT_INTERPRET, KNOWLEDGE, ROUNDUP)
   - GeneratedPrompt with all required fields

4. **Templates** (`src/prompt/templates.py`)
   - Three template types with Chinese prompts
   - Format template with topic data

5. **Generator** (`src/prompt/generator.py`)
   - PromptGenerator class
   - Auto-selection of template type based on weights (60/25/15)
   - Quality scoring (0-1)
   - JSON parsing from LLM response

6. **Tests** (`tests/test_prompt.py`)
   - 12 unit tests passing
   - Coverage: config, templates, generation, validation

**Next Steps:**
- Run actual LLM API test with real API keys
- Consider adding more template variations
- Implement retry logic for API failures
