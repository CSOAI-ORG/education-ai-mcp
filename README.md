[![education-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/education-ai-mcp/badges/score.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/education-ai-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/education-ai-mcp)](https://pypi.org/project/education-ai-mcp/)

[![education-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/education-ai-mcp/badges/card.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/education-ai-mcp)

<div align="center">

# Education Ai MCP

**Education AI MCP Server**

[![PyPI](https://img.shields.io/pypi/v/meok-education-ai-mcp)](https://pypi.org/project/meok-education-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Education AI MCP Server
EdTech tools for teachers and educators powered by MEOK AI Labs.

## Tools

| Tool | Description |
|------|-------------|
| `generate_lesson_plan` | Generate a structured lesson plan with objectives, activities, and assessment. |
| `create_quiz` | Create a quiz with various question types aligned to Bloom's taxonomy. |
| `analyze_student_progress` | Analyze student performance trends and generate progress report. |
| `recommend_learning_path` | Recommend a personalized learning path based on student profile. |
| `generate_rubric` | Generate an assessment rubric with detailed criteria and descriptors. |

## Installation

```bash
pip install meok-education-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "education-ai": {
      "command": "python",
      "args": ["-m", "meok_education_ai_mcp.server"]
    }
  }
}
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
<!-- mcp-name: io.github.CSOAI-ORG/education-ai-mcp -->
