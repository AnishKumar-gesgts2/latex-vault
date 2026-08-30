const { Plugin, Notice } = require('obsidian');
const { execFile } = require('child_process');

class GitSyncPlugin extends Plugin {
  running = false;

  async onload() {
    this.addCommand({
      id: 'pull-latest-vault-changes',
      name: 'Git: Pull latest vault changes',
      callback: () => this.pullLatest()
    });

    this.addCommand({
      id: 'commit-and-push-vault-changes',
      name: 'Git: Commit and push vault changes',
      callback: () => this.commitAndPush()
    });
  }

  vaultPath() {
    const adapter = this.app.vault.adapter;
    const basePath = typeof adapter.getBasePath === 'function' ? adapter.getBasePath() : adapter.basePath;
    if (!basePath) {
      throw new Error('Obsidian did not expose the local vault path.');
    }
    return basePath;
  }

  runGit(args) {
    return new Promise((resolve, reject) => {
      execFile('git', args, {
        cwd: this.vaultPath(),
        windowsHide: true,
        env: { ...process.env, GIT_TERMINAL_PROMPT: '0' },
        maxBuffer: 10 * 1024 * 1024
      }, (error, stdout, stderr) => {
        if (error) {
          const details = (stderr || stdout || error.message).trim();
          reject(new Error(details));
          return;
        }
        resolve((stdout || '').trim());
      });
    });
  }

  async pullLatest() {
    if (this.running) {
      new Notice('A Git operation is already running.');
      return;
    }
    this.running = true;
    try {
      new Notice('Pulling the latest vault changes from GitHub...');
      const branch = (await this.runGit(['branch', '--show-current'])) || 'main';
      const output = await this.runGit(['pull', '--ff-only', 'origin', branch]);
      new Notice(output || 'Vault is already up to date.');
    } catch (error) {
      new Notice(`Git pull failed: ${error instanceof Error ? error.message : String(error)}`, 10000);
    } finally {
      this.running = false;
    }
  }

  async commitAndPush() {
    if (this.running) {
      new Notice('A Git operation is already running.');
      return;
    }
    this.running = true;
    try {
      const status = await this.runGit(['status', '--porcelain']);
      if (!status) {
        new Notice('No local vault changes to push.');
        return;
      }

      new Notice('Committing and pushing vault changes to GitHub...');
      await this.runGit(['add', '--all']);
      const stamp = new Date().toISOString().replace('T', ' ').replace(/\.\d{3}Z$/, ' UTC');
      await this.runGit(['commit', '-m', `Update vault: ${stamp}`]);
      const branch = (await this.runGit(['branch', '--show-current'])) || 'main';
      const output = await this.runGit(['push', 'origin', branch]);
      new Notice(output || 'Vault changes pushed to GitHub.');
    } catch (error) {
      new Notice(`Git push failed: ${error instanceof Error ? error.message : String(error)}`, 10000);
    } finally {
      this.running = false;
    }
  }
}

module.exports = GitSyncPlugin;
