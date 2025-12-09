# David Knott Voice - Claude Code Plugin

Write blog posts and articles in David Knott's distinctive voice: a senior technology architect who combines intellectual authority with genuine humility.

## Installation

### Method 1: Add as Marketplace (Recommended)

This allows you to receive updates automatically:

```
/plugin marketplace add chrisns/opendk
/plugin install david-knott-voice@david-knott-marketplace
```

### Method 2: Team Distribution

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "david-knott-marketplace": {
      "source": {
        "source": "github",
        "repo": "chrisns/opendk"
      }
    }
  },
  "enabledPlugins": {
    "david-knott-voice@david-knott-marketplace": true
  }
}
```

When team members trust the repository folder, the plugin installs automatically.

### Method 3: Manual Download

Download the `.skill` file from [Releases](https://github.com/chrisns/opendk/releases) and place it in:
- Personal: `~/.claude/skills/`
- Project: `.claude/skills/`

## Usage

Once installed, Claude will automatically detect when to use this skill. Trigger phrases include:

- "Write a blog post like David Knott"
- "In DK's style..."
- "Create a technology leadership article"
- "Write a LinkedIn newsletter post"

## What's Included

The skill captures David's distinctive voice patterns:

| Element | Pattern |
|---------|---------|
| **Hedging ratio** | 8:1 (hedges to assertions) |
| **Pronoun flow** | I → we → you |
| **Target length** | 850 words (750-1,000) |
| **Metaphor domains** | Space, food, classical philosophy, computing history |
| **British spelling** | 100% (organisation, behaviour, realise) |
| **Signature phrases** | "And yet...", "However, I believe...", "It seems to me that..." |

## Updates

To receive updates:

1. The marketplace automatically pulls the latest version when you run `/plugin`
2. For release notifications, watch the repository on GitHub
3. Check the [Releases](https://github.com/chrisns/opendk/releases) page for `.skill` file downloads

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

To suggest improvements to the voice model:
1. Open an issue at [github.com/chrisns/opendk/issues](https://github.com/chrisns/opendk/issues)
2. Reference specific blog posts for patterns you've noticed
3. Submit a PR with updates to `SKILL.md` or `references/style-guide.md`

## License

MIT License - see [LICENSE](LICENSE)
