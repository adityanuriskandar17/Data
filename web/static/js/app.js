// ==========================================
// FRONTEND — Data Engineering Learning Hub
// ==========================================

let progressData = {};
let currentPath = null;
let fileList = []; // flattened ordered list of file paths

// ==========================================
// INIT
// ==========================================

document.addEventListener("DOMContentLoaded", async () => {
  await loadProgress();
  const tree = await fetchJSON("/api/tree");
  fileList = [];
  flattenFiles(tree);
  renderTree(tree, document.getElementById("file-tree"));
  renderStats();
});

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ==========================================
// FLATTEN FILE TREE (ordered list of paths)
// ==========================================

function flattenFiles(node) {
  if (!node) return;
  if (node.type === "file") {
    fileList.push(node.path);
    return;
  }
  if (node.children) {
    node.children.forEach(c => flattenFiles(c));
  }
}

// ==========================================
// FILE TREE RENDER
// ==========================================

function renderTree(node, parentEl, level = 0) {
  if (!node || node.type === "file") {
    if (node) renderFileNode(node, parentEl, level);
    return;
  }
  if (node.name === "latihan_de" && level === 0) {
    (node.children || []).forEach(child => renderTree(child, parentEl, level));
    return;
  }

  const container = document.createElement("div");
  container.className = "tree-node";

  const header = document.createElement("div");
  header.className = "tree-node-content";
  header.style.paddingLeft = `${16 + level * 12}px`;

  const hasChildren = node.children && node.children.length > 0;
  header.innerHTML = `
    <span class="arrow ${hasChildren ? "" : "hidden"}">▶</span>
    <span class="icon">📁</span>
    <span class="name">${escapeHtml(node.name)}</span>
  `;

  const childrenContainer = document.createElement("div");
  childrenContainer.className = "tree-children hidden";

  if (hasChildren) {
    header.addEventListener("click", (e) => {
      e.stopPropagation();
      childrenContainer.classList.toggle("hidden");
      header.querySelector(".arrow").classList.toggle("open");
    });
    node.children.forEach(child => renderTree(child, childrenContainer, level + 1));
  }

  container.appendChild(header);
  container.appendChild(childrenContainer);
  parentEl.appendChild(container);
}

function renderFileNode(node, parentEl, level) {
  const item = document.createElement("div");
  item.className = "tree-node";

  const content = document.createElement("div");
  content.className = "tree-node-content";
  content.style.paddingLeft = `${16 + level * 12}px`;
  content.dataset.path = node.path;

  const icons = {
    markdown: "📝", sql: "🗄️", py: "🐍", sh: "⚡",
    js: "🟨", yml: "⚙️", yaml: "⚙️", tf: "🏗️", css: "🎨",
    html: "🌐", json: "📋", code: "📄"
  };
  const icon = icons[node.ext] || icons[node.file_type] || "📄";
  const isDone = progressData[node.path] === true;

  content.innerHTML = `
    <span class="arrow hidden">▶</span>
    <span class="icon">${icon}</span>
    <span class="name">${escapeHtml(node.name)}</span>
    <span class="progress-dot ${isDone ? 'done' : ''}"></span>
  `;

  content.addEventListener("click", () => openFile(node.path, content));
  item.appendChild(content);
  parentEl.appendChild(item);
}

// ==========================================
// OPEN FILE
// ==========================================

function deriveExplanationPath(path) {
  // From "01_Programming_Fundamentals/python/basic_python.py"
  // -> try "01_Programming_Fundamentals/python/penjelasan.md"
  // -> fallback "01_Programming_Fundamentals/penjelasan.md"
  const parts = path.split("/");
  if (parts.length < 2) return null;
  const filename = parts.pop(); // remove filename
  const fileExt = filename.includes(".") ? filename.split(".").pop() : "";
  // Only pair code files with explanations
  const codeExts = ["py", "sql", "sh", "js", "yml", "yaml", "tf", "css", "html", "json"];
  if (!codeExts.includes(fileExt)) return null;
  const dir = parts.join("/");
  // Try same directory
  const sameDir = dir + "/penjelasan.md";
  // Try parent directory
  const parentParts = [...parts];
  parentParts.pop();
  const parentDir = parentParts.length > 0 ? parentParts.join("/") + "/penjelasan.md" : null;
  // We'll try both on the frontend by fetching
  return { sameDir, parentDir };
}

async function openFile(path, el) {
  currentPath = path;

  document.querySelectorAll(".tree-node-content.active").forEach(e => e.classList.remove("active"));
  if (el) el.classList.add("active");

  document.getElementById("welcome").classList.add("hidden");
  const contentDiv = document.getElementById("file-content");
  contentDiv.classList.remove("hidden");
  contentDiv.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-dim)">Memuat...</div>';

  try {
    const data = await fetchJSON(`/api/file?path=${encodeURIComponent(path)}`);
    const isDone = progressData[path] === true;
    const idx = fileList.indexOf(path);
    const prevPath = idx > 0 ? fileList[idx - 1] : null;
    const nextPath = idx < fileList.length - 1 ? fileList[idx + 1] : null;

    // Find explanation
    let explanationHtml = null;
    let explanationPath = null;
    const explPaths = deriveExplanationPath(path);
    if (explPaths) {
      try {
        const explData = await fetchJSON(`/api/file?path=${encodeURIComponent(explPaths.sameDir)}`);
        explanationHtml = explData.content;
        explanationPath = explPaths.sameDir;
      } catch (e) {
        // Try parent dir
        if (explPaths.parentDir) {
          try {
            const explData2 = await fetchJSON(`/api/file?path=${encodeURIComponent(explPaths.parentDir)}`);
            explanationHtml = explData2.content;
            explanationPath = explPaths.parentDir;
          } catch (e2) {}
        }
      }
    }

    let bodyHtml = "";
    const isCode = data.type === "code";

    if (isCode && explanationHtml) {
      // === SPLIT LAYOUT: code left, explanation right ===
      contentDiv.innerHTML = `
        <div class="file-header">
          <span class="path">${escapeHtml(path)}</span>
          <button class="toggle-progress ${isDone ? "done" : ""}" onclick="toggleProgress('${escapeHtml(path)}')">
            ${isDone ? "✅ Selesai" : "☐ Tandai Selesai"}
          </button>
        </div>
        <div class="split-layout">
          <div class="code-panel">
            <div class="panel-header">
              <span>${escapeHtml(path)}</span>
              <span class="lang-tag">${data.language || "text"}</span>
            </div>
            <pre><code class="language-${data.language || "text"}">${escapeHtml(data.content)}</code></pre>
          </div>
          <div class="explanation-panel">
            <div class="panel-header">
              <span>📝 ${escapeHtml(explanationPath)}</span>
            </div>
            <div class="panel-body">${explanationHtml}</div>
          </div>
        </div>
        <div class="nav-buttons">
          ${prevPath ? `
            <button class="nav-btn" onclick="openFile('${escapeHtml(prevPath)}')">
              <span>←</span>
              <span class="nav-right">
                <div class="nav-label">Sebelumnya</div>
                <div class="nav-name">${escapeHtml(prevPath.split("/").pop())}</div>
              </span>
            </button>
          ` : '<div></div>'}
          <span class="nav-spacer">${idx + 1} / ${fileList.length}</span>
          ${nextPath ? `
            <button class="nav-btn" onclick="openFile('${escapeHtml(nextPath)}')">
              <span class="nav-right">
                <div class="nav-label">Selanjutnya</div>
                <div class="nav-name">${escapeHtml(nextPath.split("/").pop())}</div>
              </span>
              <span>→</span>
            </button>
          ` : '<div></div>'}
        </div>
      `;
      // Highlight code
      contentDiv.querySelectorAll(".code-panel pre code").forEach(block => hljs.highlightElement(block));
    } else {
      // === FULL WIDTH: markdown file or code without explanation ===
      if (data.type === "markdown") {
        bodyHtml = `<div class="content-body">${data.content}</div>`;
      } else {
        bodyHtml = `
          <div class="code-header">
            <span class="lang-tag">${data.language || "text"}</span>
          </div>
          <pre class="code-block"><code class="language-${data.language || "text"}">${escapeHtml(data.content)}</code></pre>
        `;
      }

      contentDiv.innerHTML = `
        <div class="file-header">
          <span class="path">${escapeHtml(path)}</span>
          <button class="toggle-progress ${isDone ? "done" : ""}" onclick="toggleProgress('${escapeHtml(path)}')">
            ${isDone ? "✅ Selesai" : "☐ Tandai Selesai"}
          </button>
        </div>
        ${bodyHtml}
        <div class="nav-buttons">
          ${prevPath ? `
            <button class="nav-btn" onclick="openFile('${escapeHtml(prevPath)}')">
              <span>←</span>
              <span class="nav-right">
                <div class="nav-label">Sebelumnya</div>
                <div class="nav-name">${escapeHtml(prevPath.split("/").pop())}</div>
              </span>
            </button>
          ` : '<div></div>'}
          <span class="nav-spacer">${idx + 1} / ${fileList.length}</span>
          ${nextPath ? `
            <button class="nav-btn" onclick="openFile('${escapeHtml(nextPath)}')">
              <span class="nav-right">
                <div class="nav-label">Selanjutnya</div>
                <div class="nav-name">${escapeHtml(nextPath.split("/").pop())}</div>
              </span>
              <span>→</span>
            </button>
          ` : '<div></div>'}
        </div>
      `;
      // Highlight code if needed
      if (data.type === "code") {
        contentDiv.querySelectorAll("pre code").forEach(block => hljs.highlightElement(block));
      }
    }
  } catch (err) {
    contentDiv.innerHTML = `<div style="padding:40px;color:#f85149">Gagal memuat: ${err.message}</div>`;
  }
}

// ==========================================
// PROGRESS
// ==========================================

async function loadProgress() {
  try {
    const resp = await fetch("/api/progress");
    progressData = await resp.json();
  } catch (e) {
    progressData = {};
  }
}

async function toggleProgress(path) {
  try {
    const resp = await fetch(`/api/progress/toggle?file_path=${encodeURIComponent(path)}`);
    const result = await resp.json();
    progressData[path] = result.completed;

    document.querySelectorAll(".tree-node-content").forEach(el => {
      if (el.dataset.path === path) {
        const dot = el.querySelector(".progress-dot");
        if (dot) dot.classList.toggle("done", result.completed);
      }
    });

    const btn = document.querySelector(".toggle-progress");
    if (btn) {
      btn.textContent = result.completed ? "✅ Selesai" : "☐ Tandai Selesai";
      btn.classList.toggle("done", result.completed);
    }

    renderStats();
  } catch (e) {
    console.error("Progress error:", e);
  }
}

// ==========================================
// SEARCH
// ==========================================

let searchTimeout = null;

async function handleSearch(q) {
  clearTimeout(searchTimeout);
  const resultsDiv = document.getElementById("search-results");

  if (q.length < 2) {
    resultsDiv.classList.add("hidden");
    return;
  }

  searchTimeout = setTimeout(async () => {
    try {
      const data = await fetchJSON(`/api/search?q=${encodeURIComponent(q)}`);
      resultsDiv.innerHTML = "";

      if (data.total === 0) {
        resultsDiv.innerHTML = '<div id="search-status">Tidak ditemukan</div>';
      } else {
        data.results.forEach(r => {
          const item = document.createElement("div");
          item.className = "search-result-item";
          item.innerHTML = `
            <span>${escapeHtml(r.name)}</span>
            <span class="match-tag">${r.match}</span>
          `;
          item.addEventListener("click", () => {
            resultsDiv.classList.add("hidden");
            document.getElementById("search-input").value = "";
            const treeEl = document.querySelector(`.tree-node-content[data-path="${r.path}"]`);
            openFile(r.path, treeEl);
          });
          resultsDiv.appendChild(item);
        });
      }
      resultsDiv.classList.remove("hidden");
    } catch (e) {
      resultsDiv.innerHTML = '<div id="search-status">Error mencari</div>';
      resultsDiv.classList.remove("hidden");
    }
  }, 300);
}

document.addEventListener("click", (e) => {
  const searchBox = document.querySelector(".search-box");
  if (!searchBox.contains(e.target)) {
    document.getElementById("search-results").classList.add("hidden");
  }
});

// ==========================================
// STATS — Clean minimal card
// ==========================================

async function renderStats() {
  try {
    const totalFiles = fileList.length;
    const doneFiles = Object.values(progressData).filter(v => v).length;
    const pct = totalFiles > 0 ? Math.round((doneFiles / totalFiles) * 100) : 0;

    document.getElementById("stats").innerHTML = `
      <div class="stats-card">
        <div class="stats-main">
          <div class="stat-circle">
            <span class="pct">${pct}%</span>
          </div>
          <div class="stats-detail">
            <div class="stat-detail-item">
              <span class="num">${totalFiles}</span>
              <span class="lbl">Total File</span>
            </div>
            <div class="stat-detail-item">
              <span class="num">${doneFiles}</span>
              <span class="lbl">Selesai</span>
            </div>
            <div class="stat-detail-item">
              <span class="num">${totalFiles - doneFiles}</span>
              <span class="lbl">Tersisa</span>
            </div>
          </div>
        </div>
        <div class="progress-bar-wrap">
          <div class="progress-bar-fill" style="width: ${pct}%"></div>
        </div>
      </div>
      <div class="welcome-sub">Pilih materi dari sidebar untuk mulai belajar</div>
    `;
  } catch (e) {}
}

// ==========================================
// HELPERS
// ==========================================

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
