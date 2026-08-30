# GitHub vault sync

The vault is connected to the private repository:

<https://github.com/AnishKumar-gesgts2/latex-vault>

After enabling or reloading the **Git Sync** community plugin in Obsidian, use the command palette (`Ctrl+P`) to run:

- **Git: Pull latest vault changes** - downloads and fast-forwards to the latest `main` branch changes.
- **Git: Commit and push vault changes** - stages all local vault changes, creates a dated commit, and pushes it to GitHub. If there are no changes, it does nothing.

The plugin uses the GitHub authentication already configured for Git on this computer. Pull uses `--ff-only`, so it will stop safely if the local and remote histories have diverged instead of overwriting work.
