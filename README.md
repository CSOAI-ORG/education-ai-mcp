# Education AI MCP

> EdTech tools for teachers - lesson plans, quizzes, student progress, learning paths, rubric generation

Built by **MEOK AI Labs** | [meok.ai](https://meok.ai)

## Features

| Tool | Description |
|------|-------------|
| `generate_lesson_plan` | See tool docstring for details |
| `create_quiz` | See tool docstring for details |
| `analyze_student_progress` | See tool docstring for details |
| `recommend_learning_path` | See tool docstring for details |
| `generate_rubric` | See tool docstring for details |

## Installation

```bash
pip install mcp
```

## Usage

### As an MCP Server

```bash
python server.py
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "education-ai-mcp": {
      "command": "python",
      "args": ["/path/to/education-ai-mcp/server.py"]
    }
  }
}
```

## Rate Limits

Free tier includes **30-50 calls per tool per day**. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with FastMCP by MEOK AI Labs
