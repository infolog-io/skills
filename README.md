# Information Logistics Skills

Public Claude Code plugin marketplace for Information Logistics skills.

## Install

In Claude Code, add this marketplace once:

```
/plugin marketplace add infolog-io/skills
```

Then install any plugin from it:

```
/plugin install <plugin-name>@infolog-io
```

List what is available:

```
/plugin marketplace list infolog-io
```

## Available plugins

| Plugin | Description | Install |
|--------|-------------|---------|
| `claude-pip` | Performance Improvement Plan for Claude. Type `CLAUDE PIP` to lock in a behavioral discipline (TDD, plan mode, sub-agents, adversarial review) as a deterministic rule. | `/plugin install claude-pip@infolog-io` |
| `tufte-love` | Tufte-style audits, redesigns, and reviews for data visualizations and dashboards. | `/plugin install tufte-love@infolog-io` |

New plugins land via PRs that follow [CONTRIBUTING.md](CONTRIBUTING.md).

## Repo layout

```
infolog-io/skills/
├── .claude-plugin/
│   └── marketplace.json     # marketplace manifest
├── plugins/                 # one directory per plugin
├── README.md                # this file
├── CONTRIBUTING.md          # how to add a plugin
└── LICENSE                  # MIT
```

## License

[MIT](LICENSE).
