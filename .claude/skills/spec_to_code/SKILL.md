---
name: "spec-to-implementation"
description: "Convert Spec-Kit markdown specifications into working code without manual coding. Enforces spec-driven development."
version: "1.0.0"
---

# Spec to Implementation Skill

## When to Use This Skill
- User asks to implement a feature
- A spec file exists under /specs
- Hackathon phase requires no manual coding

## How This Skill Works
1. Read the referenced spec completely
2. Identify acceptance criteria and constraints
3. Generate an implementation plan
4. Generate code ONLY based on spec
5. Verify implementation matches spec line-by-line

## Rules
- Do NOT invent features not in spec
- Do NOT skip edge cases defined in spec
- If spec is unclear, request clarification before coding

## Output Format
- 📋 Plan
- 🧩 Files to be created/updated
- 🧠 Implementation notes
- 💻 Generated code

## Quality Criteria
- Every spec requirement implemented
- No hardcoded values
- Clean, readable structure
