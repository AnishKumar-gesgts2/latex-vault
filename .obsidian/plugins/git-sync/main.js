const { Plugin, Notice } = require('obsidian');
const { execFile } = require('child_process');

class GitSyncPlugin extends Plugin {
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
    const basePath = this.app.vault.adapter.basePath;
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
    try {
      new Notice('Pulling the latest vault changes from GitHub...');
      const output = await this.runGit(['pull', '--ff-only']);
      new Notice(output || 'Vault is already up to date.');
    } catch (error) {
      new Notice(`Git pull failed: ${error.message}`, 10000);
    }
  }

  async commitAndPush() {
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
      const output = await this.runGit(['push']);
      new Notice(output || 'Vault changes pushed to GitHub.');
    } catch (error) {
      new Notice(`Git push failed: ${error.message}`, 10000);
    }
  }
}

module.exports = GitSyncPlugin;
