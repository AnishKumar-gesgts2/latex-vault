var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// main.ts
var main_exports = {};
__export(main_exports, {
  default: () => LatexBuilderPlugin
});
module.exports = __toCommonJS(main_exports);
var import_obsidian = require("obsidian");
var import_child_process = require("child_process");
var DEFAULT_SETTINGS = {
  compiler: "pdflatex",
  arguments: "-interaction=nonstopmode -halt-on-error {file}"
};
var LatexBuilderPlugin = class extends import_obsidian.Plugin {
  constructor() {
    super(...arguments);
    this.settings = DEFAULT_SETTINGS;
  }
  async onload() {
    await this.loadSettings();
    this.addCommand({
      id: "build-current-latex-file",
      name: "LaTeX: Build current file",
      checkCallback: (checking) => {
        const file = this.app.workspace.getActiveFile();
        const available = (file == null ? void 0 : file.extension.toLowerCase()) === "tex";
        if (!checking && available) this.build(file);
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
  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  build(file) {
    var _a;
    const args = this.tokenize(this.settings.arguments.replace(/\{file\}/g, file.name));
    const command = `${this.settings.compiler} ${args.join(" ")}`;
    new import_obsidian.Notice(`Building ${file.name}...`);
    const basePath = this.getVaultPath();
    const workingDirectory = ((_a = file.parent) == null ? void 0 : _a.path) ? `${basePath}\\${file.parent.path.replace(/\//g, "\\")}` : basePath;
    (0, import_child_process.execFile)(this.settings.compiler, args, { cwd: workingDirectory, timeout: 12e4, windowsHide: true }, (error, stdout, stderr) => {
      if (error) {
        new BuildOutputModal(this.app, `Build failed

${command}

${stderr || stdout || error.message}`).open();
        return;
      }
      new import_obsidian.Notice(`Built ${file.basename}.pdf`);
      new BuildOutputModal(this.app, `Build succeeded

${command}

${stdout || "No compiler output."}`).open();
    });
  }
  tokenize(value) {
    const tokens = value.match(/(?:[^\s"]+|"[^"]*")+/g) || [];
    return tokens.map((token) => token.replace(/^"|"$/g, "")).filter(Boolean);
  }
  getVaultPath() {
    var _a;
    const adapter = this.app.vault.adapter;
    const basePath = ((_a = adapter.getBasePath) == null ? void 0 : _a.call(adapter)) || adapter.basePath;
    if (!basePath) throw new Error("Obsidian did not expose the local vault path.");
    return basePath;
  }
};
var LatexFileModal = class extends import_obsidian.Modal {
  constructor(app, settings, onChoose) {
    super(app);
    this.settings = settings;
    this.onChoose = onChoose;
  }
  onOpen() {
    this.titleEl.setText("Build a LaTeX file");
    this.contentEl.createEl("p", { text: `Compiler: ${this.settings.compiler}` });
    const texFiles = this.app.vault.getFiles().filter((file) => file.extension.toLowerCase() === "tex");
    if (texFiles.length === 0) {
      this.contentEl.createEl("p", { text: "No .tex files were found in this vault." });
      return;
    }
    for (const file of texFiles.sort((a, b) => a.path.localeCompare(b.path))) {
      new import_obsidian.Setting(this.contentEl).setName(file.path).addButton((button) => button.setButtonText("Build").setCta().onClick(() => {
        this.close();
        this.onChoose(file);
      }));
    }
  }
};
var BuildOutputModal = class extends import_obsidian.Modal {
  constructor(app, output) {
    super(app);
    this.output = output;
  }
  onOpen() {
    this.titleEl.setText("LaTeX build output");
    this.contentEl.createEl("pre", { text: this.output });
  }
};
var LatexBuilderSettingTab = class extends import_obsidian.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    new import_obsidian.Setting(containerEl).setName("Compiler").setDesc("Executable available on PATH, usually pdflatex or xelatex.").addText((text) => text.setValue(this.plugin.settings.compiler).onChange(async (value) => {
      this.plugin.settings.compiler = value.trim() || DEFAULT_SETTINGS.compiler;
      await this.plugin.saveSettings();
    }));
    new import_obsidian.Setting(containerEl).setName("Arguments").setDesc("Use {file} where the selected .tex filename should go.").addText((text) => text.setValue(this.plugin.settings.arguments).onChange(async (value) => {
      this.plugin.settings.arguments = value;
      await this.plugin.saveSettings();
    }));
  }
};
