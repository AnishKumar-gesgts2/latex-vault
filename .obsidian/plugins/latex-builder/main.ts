import { App, Modal, Notice, Plugin, PluginSettingTab, Setting, TFile } from "obsidian";
import { execFile } from "child_process";

interface LatexBuilderSettings {
	compiler: string;
	arguments: string;
}

const DEFAULT_SETTINGS: LatexBuilderSettings = {
	compiler: "pdflatex",
	arguments: "-interaction=nonstopmode -halt-on-error {file}"
};

export default class LatexBuilderPlugin extends Plugin {
	settings: LatexBuilderSettings = DEFAULT_SETTINGS;

	async onload(): Promise<void> {
		await this.loadSettings();
		this.addCommand({
			id: "build-current-latex-file",
			name: "LaTeX: Build current file",
			checkCallback: (checking) => {
				const file = this.app.workspace.getActiveFile();
				const available = file?.extension.toLowerCase() === "tex";
				if (!checking && available) this.build(file as TFile);
				return available;
			}
		});
		this.addCommand({
			id: "choose-latex-file-to-build",
			name: "LaTeX: Choose file to build",
			callback: () => new LatexFileModal(this.app, this.settings, (file) => this.build(file)).open()
		});
		this.addSettingTab(new LatexBuilderSettingTab(this.app, this));
	}

	async loadSettings(): Promise<void> {
		this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
	}

	async saveSettings(): Promise<void> {
		await this.saveData(this.settings);
	}

	private build(file: TFile): void {
		const args = this.tokenize(this.settings.arguments.replace(/\{file\}/g, file.name));
		const command = `${this.settings.compiler} ${args.join(" ")}`;
		new Notice(`Building ${file.name}...`);
		const basePath = this.getVaultPath();
		const workingDirectory = file.parent?.path ? `${basePath}\\${file.parent.path.replace(/\//g, "\\")}` : basePath;
		execFile(this.settings.compiler, args, { cwd: workingDirectory, timeout: 120000, windowsHide: true }, (error, stdout, stderr) => {
			if (error) {
				new BuildOutputModal(this.app, `Build failed\n\n${command}\n\n${stderr || stdout || error.message}`).open();
				return;
			}
			new Notice(`Built ${file.basename}.pdf`);
			new BuildOutputModal(this.app, `Build succeeded\n\n${command}\n\n${stdout || "No compiler output."}`).open();
		});
	}

	private tokenize(value: string): string[] {
		const tokens = value.match(/(?:[^\s"]+|"[^"]*")+/g) || [];
		return tokens.map((token) => token.replace(/^"|"$/g, "")).filter(Boolean);
	}

	private getVaultPath(): string {
		const adapter = this.app.vault.adapter as { getBasePath?: () => string; basePath?: string };
		const basePath = adapter.getBasePath?.() || adapter.basePath;
		if (!basePath) throw new Error("Obsidian did not expose the local vault path.");
		return basePath;
	}
}

class LatexFileModal extends Modal {
	private readonly settings: LatexBuilderSettings;
	private readonly onChoose: (file: TFile) => void;

	constructor(app: App, settings: LatexBuilderSettings, onChoose: (file: TFile) => void) {
		super(app);
		this.settings = settings;
		this.onChoose = onChoose;
	}

	onOpen(): void {
		this.titleEl.setText("Build a LaTeX file");
		this.contentEl.createEl("p", { text: `Compiler: ${this.settings.compiler}` });
		const texFiles = this.app.vault.getFiles().filter((file) => file.extension.toLowerCase() === "tex");
		if (texFiles.length === 0) {
			this.contentEl.createEl("p", { text: "No .tex files were found in this vault." });
			return;
		}
		for (const file of texFiles.sort((a, b) => a.path.localeCompare(b.path))) {
			new Setting(this.contentEl).setName(file.path).addButton((button) => button.setButtonText("Build").setCta().onClick(() => {
				this.close();
				this.onChoose(file);
			}));
		}
	}
}

class BuildOutputModal extends Modal {
	constructor(app: App, private readonly output: string) { super(app); }
	onOpen(): void {
		this.titleEl.setText("LaTeX build output");
		this.contentEl.createEl("pre", { text: this.output });
	}
}

class LatexBuilderSettingTab extends PluginSettingTab {
	constructor(app: App, private readonly plugin: LatexBuilderPlugin) { super(app, plugin); }

	display(): void {
		const { containerEl } = this;
		containerEl.empty();
		new Setting(containerEl).setName("Compiler").setDesc("Executable available on PATH, usually pdflatex or xelatex.").addText((text) => text.setValue(this.plugin.settings.compiler).onChange(async (value) => {
			this.plugin.settings.compiler = value.trim() || DEFAULT_SETTINGS.compiler;
			await this.plugin.saveSettings();
		}));
		new Setting(containerEl).setName("Arguments").setDesc("Use {file} where the selected .tex filename should go.").addText((text) => text.setValue(this.plugin.settings.arguments).onChange(async (value) => {
			this.plugin.settings.arguments = value;
			await this.plugin.saveSettings();
		}));
	}
}
