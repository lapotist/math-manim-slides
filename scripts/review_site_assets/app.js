"use strict";

const STATUS_LABELS = {
  not_started: "尚未檢閱",
  in_progress: "檢閱中",
  issue: "有待修正",
  ready: "全部通過",
  stale: "檢閱已失效",
};

const VERDICT_LABELS = {
  pending: "未判定",
  pass: "通過",
  issue: "需修改",
};

const SEGMENT_CRITERIA_LABELS = {
  legibility: "數字、符號與中文字形清楚",
  layout: "無重疊、裁切或版面跳動",
  motion: "動作只支持當前推理",
  settled: "片段落點完整且可閱讀",
  loop: "循環首尾銜接自然",
};

const LESSON_CRITERIA_LABELS = {
  contact_sheet: "已檢查完整定格聯絡表",
  transition_sweep: "已檢查完整轉場掃描表",
  narration: "畫面順序與講稿一致",
  mathematics: "推理正確、清楚而不冗長",
  answer: "答案已由獨立檢查確認",
};

const ISSUE_TAG_LABELS = {
  glyph: "字形",
  overlap: "重疊",
  clipping: "裁切",
  timing: "節奏",
  motion: "動作",
  loop: "循環",
  mathematics: "數學",
  script: "講稿",
};

const state = {
  catalog: null,
  summaries: new Map(),
  lesson: null,
  review: null,
  stale: false,
  activeBeat: null,
  evidenceTab: "video",
  pendingSeek: null,
  saveTimer: null,
  saveSequence: 0,
};

const elements = Object.fromEntries(
  [
    "back-button",
    "save-state",
    "list-view",
    "generated-at",
    "metrics",
    "search-input",
    "collection-filter",
    "status-filter",
    "result-count",
    "lesson-rows",
    "empty-state",
    "blocked-panel",
    "blocked-summary",
    "blocked-list",
    "review-view",
    "review-collection",
    "review-title",
    "review-id",
    "review-summary",
    "overview-button",
    "segment-list",
    "segment-heading",
    "evidence-tabs",
    "evidence-stage",
    "evidence-meta",
    "script-panel",
    "segment-actions",
    "review-panel",
    "lightbox",
    "lightbox-close",
    "lightbox-image",
  ].map((id) => [id, document.getElementById(id)])
);

function make(tagName, options = {}, children = []) {
  const node = document.createElement(tagName);
  if (options.className) node.className = options.className;
  if (options.text !== undefined) node.textContent = options.text;
  if (options.type) node.type = options.type;
  if (options.title) node.title = options.title;
  if (options.ariaLabel) node.setAttribute("aria-label", options.ariaLabel);
  if (options.dataset) Object.assign(node.dataset, options.dataset);
  if (options.attrs) {
    for (const [name, value] of Object.entries(options.attrs)) {
      node.setAttribute(name, String(value));
    }
  }
  for (const child of children) {
    if (child !== null && child !== undefined) node.append(child);
  }
  return node;
}

function clear(node) {
  node.replaceChildren();
}

async function requestJSON(url, options = {}) {
  const response = await fetch(url, {
    cache: "no-store",
    ...options,
    headers: {
      Accept: "application/json",
      ...(options.headers || {}),
    },
  });
  let payload = null;
  try {
    payload = await response.json();
  } catch (_error) {
    payload = null;
  }
  if (!response.ok) {
    throw new Error(payload?.error || `HTTP ${response.status}`);
  }
  return payload;
}

function formatDate(value) {
  if (!value) return "尚未儲存";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-TW", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function formatDuration(seconds) {
  if (!Number.isFinite(seconds)) return "";
  return `${seconds.toFixed(seconds < 10 ? 1 : 0)} 秒`;
}

function statusPill(status) {
  const safeStatus = STATUS_LABELS[status] ? status : "not_started";
  return make("span", {
    className: `status-pill status-${safeStatus}`,
    text: STATUS_LABELS[safeStatus],
  });
}

function summaryFor(lessonId) {
  return (
    state.summaries.get(lessonId) || {
      lesson_id: lessonId,
      status: "not_started",
      passed_segments: 0,
      issue_segments: 0,
      segment_count: 0,
      ready: false,
      updated_at: null,
    }
  );
}

function computeLocalSummary() {
  const segments = Object.values(state.review.segments);
  const passed = segments.filter((item) => item.verdict === "pass").length;
  const issues = segments.filter((item) => item.verdict === "issue").length;
  const allSegmentsPass = state.lesson.segments.every((segment) => {
    const result = state.review.segments[segment.beat_id];
    return result.verdict === "pass" && Object.values(result.criteria).every(Boolean);
  });
  const ready =
    allSegmentsPass && Object.values(state.review.lesson_criteria).every(Boolean);
  let status = "not_started";
  if (state.stale) status = "stale";
  else if (ready) status = "ready";
  else if (issues) status = "issue";
  else if (passed) status = "in_progress";
  return {
    lesson_id: state.lesson.id,
    status,
    passed_segments: passed,
    issue_segments: issues,
    segment_count: segments.length,
    updated_at: state.review.updated_at,
    ready,
  };
}

function renderMetrics() {
  const summaries = [...state.summaries.values()];
  const metrics = [
    [state.catalog.summary.reviewable, "可檢閱課程"],
    [state.catalog.summary.segments, "教學片段"],
    [summaries.filter((item) => item.status === "ready").length, "全部通過"],
    [summaries.filter((item) => item.status === "issue").length, "有待修正"],
    [state.catalog.summary.blocked, "證據未就緒"],
  ];
  clear(elements.metrics);
  for (const [value, label] of metrics) {
    elements.metrics.append(
      make("div", { className: "metric" }, [
        make("strong", { text: value }),
        make("span", { text: label }),
      ])
    );
  }
}

function renderBlocked() {
  const blocked = state.catalog.blocked;
  elements["blocked-panel"].hidden = blocked.length === 0;
  elements["blocked-summary"].textContent = `${blocked.length} 個課程缺少可驗證證據`;
  clear(elements["blocked-list"]);
  for (const item of blocked) {
    elements["blocked-list"].append(
      make("div", { className: "blocked-row" }, [
        make("div", {}, [
          make("div", { className: "row-title", text: item.title }),
          make("div", { className: "row-id", text: item.id }),
        ]),
        make("div", { className: "blocked-reason", text: item.reason }),
      ])
    );
  }
}

function populateCollectionFilter() {
  const titles = [...new Set(state.catalog.lessons.map((lesson) => lesson.collection_title))]
    .sort((a, b) => a.localeCompare(b, "zh-Hant"));
  elements["collection-filter"].replaceChildren(
    make("option", { text: "全部題目集合", attrs: { value: "" } })
  );
  for (const title of titles) {
    elements["collection-filter"].append(
      make("option", { text: title, attrs: { value: title } })
    );
  }
}

function renderLessonRows() {
  const query = elements["search-input"].value.trim().toLocaleLowerCase("zh-Hant");
  const collection = elements["collection-filter"].value;
  const status = elements["status-filter"].value;
  const lessons = state.catalog.lessons.filter((lesson) => {
    const summary = summaryFor(lesson.id);
    const haystack = [
      lesson.id,
      lesson.title,
      lesson.collection_title,
      ...(lesson.tags || []),
    ]
      .join(" ")
      .toLocaleLowerCase("zh-Hant");
    return (
      (!query || haystack.includes(query)) &&
      (!collection || lesson.collection_title === collection) &&
      (!status || summary.status === status)
    );
  });

  clear(elements["lesson-rows"]);
  elements["empty-state"].hidden = lessons.length !== 0;
  elements["result-count"].textContent = `顯示 ${lessons.length} / ${state.catalog.lessons.length} 個可檢閱課程`;
  for (const lesson of lessons) {
    const summary = summaryFor(lesson.id);
    const button = make("button", {
      className: "open-review",
      text: "檢閱",
      type: "button",
      ariaLabel: `檢閱 ${lesson.title}`,
    });
    button.addEventListener("click", () => openLesson(lesson.id));
    const qaText = `產生於 ${formatDate(lesson.qa_generated_at)}`;
    elements["lesson-rows"].append(
      make("tr", {}, [
        make("td", {}, [statusPill(summary.status)]),
        make("td", {}, [
          make("div", { text: lesson.collection_title }),
          make("div", { className: "row-detail", text: lesson.production_state }),
        ]),
        make("td", {}, [
          make("p", { className: "row-title", text: lesson.title }),
          make("div", { className: "row-id", text: lesson.id }),
        ]),
        make("td", {}, [
          make("div", { text: `${summary.passed_segments} / ${lesson.segments.length} 通過` }),
          make("div", {
            className: "row-detail",
            text: summary.issue_segments ? `${summary.issue_segments} 個待修正` : "無待修正標記",
          }),
        ]),
        make("td", {}, [make("div", { className: "row-detail", text: qaText })]),
        make("td", {}, [button]),
      ])
    );
  }
}

function renderList() {
  renderMetrics();
  renderLessonRows();
  renderBlocked();
}

function showList({ historyMode = "push" } = {}) {
  if (state.saveTimer) {
    clearTimeout(state.saveTimer);
    state.saveTimer = null;
    saveReview();
  }
  state.lesson = null;
  state.review = null;
  state.activeBeat = null;
  elements["list-view"].hidden = false;
  elements["review-view"].hidden = true;
  elements["back-button"].hidden = true;
  elements["save-state"].textContent = "";
  if (historyMode !== "none") {
    const method = historyMode === "replace" ? "replaceState" : "pushState";
    history[method]({}, "", "/");
  }
  renderList();
}

function setReviewLocation({ replace = false } = {}) {
  const params = new URLSearchParams({ lesson: state.lesson.id });
  if (state.activeBeat) params.set("beat", state.activeBeat);
  const method = replace ? "replaceState" : "pushState";
  history[method]({}, "", `/?${params}`);
}

async function openLesson(lessonId, { beat = null, historyMode = "push" } = {}) {
  const lesson = state.catalog.lessons.find((item) => item.id === lessonId);
  if (!lesson) {
    showList({ historyMode: "replace" });
    return;
  }
  elements["save-state"].textContent = "載入中";
  try {
    const payload = await requestJSON(`/api/reviews/${encodeURIComponent(lessonId)}`);
    state.lesson = lesson;
    state.review = payload.review;
    state.stale = Boolean(payload.stale);
    state.activeBeat = lesson.segments.some((item) => item.beat_id === beat) ? beat : null;
    state.evidenceTab = "video";
    state.pendingSeek = null;
    elements["list-view"].hidden = true;
    elements["review-view"].hidden = false;
    elements["back-button"].hidden = false;
    elements["save-state"].textContent = state.stale ? "舊檢閱已失效" : "";
    if (historyMode !== "none") setReviewLocation({ replace: historyMode === "replace" });
    renderReviewWorkspace();
  } catch (error) {
    elements["save-state"].textContent = "載入失敗";
    window.alert(`無法開啟檢閱：${error.message}`);
  }
}

function activeSegment() {
  return state.lesson.segments.find((item) => item.beat_id === state.activeBeat) || null;
}

function selectBeat(beatId) {
  if (state.activeBeat === beatId) return;
  state.activeBeat = beatId;
  state.evidenceTab = "video";
  state.pendingSeek = null;
  setReviewLocation();
  renderReviewWorkspace();
}

function renderReviewHeader() {
  elements["review-collection"].textContent = state.lesson.collection_title;
  elements["review-title"].textContent = state.lesson.title;
  elements["review-id"].textContent = state.lesson.id;
  clear(elements["review-summary"]);
  const summary = computeLocalSummary();
  elements["review-summary"].append(
    statusPill(summary.status),
    make("span", {
      className: "subtle",
      text: `${summary.passed_segments} / ${summary.segment_count} 片段通過`,
    })
  );
}

function renderSegmentNav() {
  const overviewActive = state.activeBeat === null;
  elements["overview-button"].classList.toggle("active", overviewActive);
  elements["overview-button"].setAttribute("aria-current", overviewActive ? "page" : "false");
  elements["overview-button"].onclick = () => selectBeat(null);
  clear(elements["segment-list"]);
  for (const segment of state.lesson.segments) {
    const result = state.review.segments[segment.beat_id];
    const active = state.activeBeat === segment.beat_id;
    const button = make("button", {
      className: `segment-item${active ? " active" : ""}`,
      type: "button",
      attrs: { "aria-current": active ? "page" : "false" },
    });
    const dot = make("span", {
      className: `segment-state ${result.verdict}`,
      attrs: { "aria-hidden": "true" },
    });
    button.append(
      dot,
      make("span", { className: "segment-number", text: String(segment.number).padStart(2, "0") }),
      document.createTextNode(segment.script.title),
      make("span", { className: "segment-name", text: segment.beat_id })
    );
    button.addEventListener("click", () => selectBeat(segment.beat_id));
    elements["segment-list"].append(button);
    if (active) {
      requestAnimationFrame(() =>
        button.scrollIntoView({ block: "nearest", inline: "center" })
      );
    }
  }
}

function imageButton(url, alt, className = "image-button") {
  const image = make("img", { attrs: { src: url, alt, loading: "lazy" } });
  const button = make("button", {
    className,
    type: "button",
    ariaLabel: `放大查看：${alt}`,
  }, [image]);
  button.addEventListener("click", () => openLightbox(url, alt));
  return button;
}

function renderOverviewEvidence() {
  clear(elements["segment-heading"]);
  elements["segment-heading"].append(make("h2", { text: "整體檢閱" }));
  clear(elements["evidence-tabs"]);
  elements["evidence-tabs"].hidden = true;
  clear(elements["evidence-stage"]);
  const figures = [
    [state.lesson.contact_sheet_url, "每個片段的定格聯絡表"],
    [state.lesson.transition_sweep_url, "完整轉場掃描表"],
  ];
  const grid = make("div", { className: "overview-grid" });
  for (const [url, label] of figures) {
    grid.append(
      make("figure", { className: "overview-figure" }, [
        imageButton(url, label),
        make("figcaption", { text: label }),
      ])
    );
  }
  elements["evidence-stage"].append(grid);
  elements["evidence-meta"].replaceChildren(
    make("span", { text: `${state.lesson.segments.length} 個片段` }),
    make("span", { text: `QA：${formatDate(state.lesson.qa_generated_at)}` })
  );
  clear(elements["script-panel"]);
  elements["script-panel"].append(
    make("h3", { text: "預期答案" }),
    make("p", {
      className: "math-check",
      text: state.lesson.expected_answer || "未提供",
    }),
    make("div", { className: "review-section" }, [
      make("h3", { text: "獨立數學檢查" }),
      make("p", {
        className: "math-check",
        text: state.lesson.independent_check || "未提供",
      }),
    ])
  );
  renderSegmentActions(null);
}

function renderEvidenceTabs(segment) {
  elements["evidence-tabs"].hidden = false;
  clear(elements["evidence-tabs"]);
  const tabs = [
    ["video", "播放"],
    ["settled", "定格"],
    ["sweep", `轉場 ${segment.sweeps.length}`],
  ];
  for (const [id, label] of tabs) {
    const button = make("button", {
      className: "tab-button",
      type: "button",
      text: label,
      attrs: {
        role: "tab",
        "aria-selected": state.evidenceTab === id ? "true" : "false",
      },
    });
    button.addEventListener("click", () => {
      state.evidenceTab = id;
      state.pendingSeek = null;
      renderSegmentEvidence(segment);
    });
    elements["evidence-tabs"].append(button);
  }
}

function seekVideo(video, seconds) {
  const apply = () => {
    video.pause();
    video.currentTime = Math.min(seconds, Math.max(video.duration - 0.02, 0));
  };
  if (video.readyState >= 1) apply();
  else video.addEventListener("loadedmetadata", apply, { once: true });
}

function renderSegmentStage(segment) {
  clear(elements["evidence-stage"]);
  if (state.evidenceTab === "video") {
    const video = make("video", {
      attrs: {
        src: segment.video_url,
        poster: segment.preview_url,
        controls: "",
        preload: "metadata",
        playsinline: "",
      },
    });
    if (state.pendingSeek !== null) {
      seekVideo(video, state.pendingSeek);
      state.pendingSeek = null;
    }
    elements["evidence-stage"].append(video);
    return;
  }
  if (state.evidenceTab === "settled") {
    elements["evidence-stage"].append(
      imageButton(segment.preview_url, `${segment.script.title} 定格畫面`)
    );
    return;
  }
  const grid = make("div", { className: "sweep-grid" });
  for (const sweep of segment.sweeps) {
    const button = make("button", {
      className: "sweep-frame",
      type: "button",
      ariaLabel: `跳到 ${sweep.at_seconds.toFixed(2)} 秒`,
    }, [
      make("img", {
        attrs: {
          src: sweep.url,
          alt: `${segment.script.title} ${sweep.at_seconds.toFixed(2)} 秒`,
          loading: "lazy",
        },
      }),
      make("span", { text: `${sweep.at_seconds.toFixed(2)} s` }),
    ]);
    button.addEventListener("click", () => {
      state.pendingSeek = sweep.at_seconds;
      state.evidenceTab = "video";
      renderSegmentEvidence(segment);
    });
    grid.append(button);
  }
  elements["evidence-stage"].append(grid);
}

function renderSegmentEvidence(segment) {
  renderEvidenceTabs(segment);
  renderSegmentStage(segment);
}

function renderSegmentActions(segment) {
  clear(elements["segment-actions"]);
  const index = segment
    ? state.lesson.segments.findIndex((item) => item.beat_id === segment.beat_id)
    : -1;
  const previousBeat = index > 0 ? state.lesson.segments[index - 1].beat_id : null;
  const nextBeat = index < state.lesson.segments.length - 1
    ? state.lesson.segments[index + 1].beat_id
    : null;
  const previous = make("button", {
    className: "secondary-button",
    type: "button",
    text: index === 0 ? "← 整體檢閱" : "← 上一片段",
  });
  previous.disabled = segment === null;
  previous.addEventListener("click", () => selectBeat(previousBeat));
  const next = make("button", {
    className: "secondary-button",
    type: "button",
    text: segment === null ? "第一片段 →" : "下一片段 →",
  });
  next.disabled = Boolean(segment) && nextBeat === null;
  next.addEventListener("click", () =>
    selectBeat(segment === null ? state.lesson.segments[0].beat_id : nextBeat)
  );
  elements["segment-actions"].append(previous, next);
}

function renderBeatEvidence(segment) {
  elements["segment-heading"].replaceChildren(
    make("h2", { text: `${String(segment.number).padStart(2, "0")}　${segment.script.title}` }),
    make("span", { className: "beat-id", text: segment.beat_id })
  );
  renderSegmentEvidence(segment);
  const meta = [
    formatDuration(segment.duration),
    `${segment.resolution[0]}×${segment.resolution[1]}`,
    segment.loop ? "循環片段" : "一般片段",
  ];
  if (segment.loop && Number.isFinite(segment.loop_endpoint_difference)) {
    meta.push(`首尾差 ${segment.loop_endpoint_difference.toFixed(2)}`);
  }
  elements["evidence-meta"].replaceChildren(
    ...meta.map((item) => make("span", { text: item }))
  );
  elements["script-panel"].replaceChildren(
    make("h3", { text: "對應講稿" }),
    make("pre", { className: "script-text", text: segment.script.body })
  );
  renderSegmentActions(segment);
}

function verdictControl(result) {
  const control = make("div", { className: "verdict-control" });
  for (const verdict of ["pending", "pass", "issue"]) {
    const button = make("button", {
      className: `verdict-button ${verdict}${result.verdict === verdict ? " active" : ""}`,
      type: "button",
      text: VERDICT_LABELS[verdict],
      attrs: { "aria-pressed": result.verdict === verdict ? "true" : "false" },
    });
    button.addEventListener("click", () => {
      result.verdict = verdict;
      reviewChanged();
      renderReviewWorkspace();
    });
    control.append(button);
  }
  return control;
}

function checklist(criteria, labels) {
  const list = make("div", { className: "checklist" });
  for (const [criterion, checked] of Object.entries(criteria)) {
    const input = make("input", {
      type: "checkbox",
      attrs: { id: `criterion-${criterion}` },
    });
    input.checked = checked;
    input.addEventListener("change", () => {
      criteria[criterion] = input.checked;
      reviewChanged();
      renderReviewHeader();
      renderSegmentNav();
      renderReadiness();
    });
    const label = make("label", {
      className: "check-row",
      attrs: { for: `criterion-${criterion}` },
    }, [input, make("span", { text: labels[criterion] || criterion })]);
    list.append(label);
  }
  return list;
}

function issueTagControls(result) {
  const container = make("div", { className: "issue-tags" });
  for (const [tag, labelText] of Object.entries(ISSUE_TAG_LABELS)) {
    const input = make("input", { type: "checkbox" });
    input.checked = result.issue_tags.includes(tag);
    input.addEventListener("change", () => {
      const tags = new Set(result.issue_tags);
      if (input.checked) tags.add(tag);
      else tags.delete(tag);
      result.issue_tags = [...tags];
      reviewChanged();
    });
    container.append(
      make("label", { className: "tag-toggle" }, [
        input,
        make("span", { text: labelText }),
      ])
    );
  }
  return container;
}

function notesArea(value, onInput, labelText) {
  const id = `notes-${state.activeBeat || "lesson"}`;
  const textarea = make("textarea", {
    attrs: { id, maxlength: state.activeBeat ? 4000 : 8000 },
  });
  textarea.value = value;
  textarea.addEventListener("input", () => onInput(textarea.value));
  return make("div", { className: "review-section" }, [
    make("label", { className: "notes-label", text: labelText, attrs: { for: id } }),
    textarea,
  ]);
}

function renderReadiness() {
  const existing = elements["review-panel"].querySelector(".readiness");
  if (existing) existing.remove();
  const summary = computeLocalSummary();
  const box = make("div", { className: `readiness${summary.ready ? " ready" : ""}` }, [
    make("strong", { text: summary.ready ? "本機檢閱條件已完成" : "尚未完成檢閱" }),
    make("span", {
      text: summary.ready
        ? "所有片段與整體檢查均已明確通過。"
        : `${summary.passed_segments} / ${summary.segment_count} 個片段通過；整體條件需全部勾選。`,
    }),
  ]);
  elements["review-panel"].append(box);
}

function renderReviewPanel() {
  clear(elements["review-panel"]);
  const segment = activeSegment();
  if (segment) {
    const result = state.review.segments[segment.beat_id];
    elements["review-panel"].append(
      make("h2", { text: "片段判定" }),
      verdictControl(result),
      checklist(result.criteria, SEGMENT_CRITERIA_LABELS),
      make("div", { className: "review-section" }, [
        make("h3", { text: "問題類型" }),
        issueTagControls(result),
      ]),
      notesArea(
        result.notes,
        (value) => {
          result.notes = value;
          reviewChanged();
        },
        "片段備註"
      )
    );
  } else {
    elements["review-panel"].append(
      make("h2", { text: "整體判定" }),
      checklist(state.review.lesson_criteria, LESSON_CRITERIA_LABELS),
      notesArea(
        state.review.notes,
        (value) => {
          state.review.notes = value;
          reviewChanged();
        },
        "整體備註"
      )
    );
  }
  renderReadiness();
}

function renderReviewWorkspace() {
  renderReviewHeader();
  renderSegmentNav();
  const segment = activeSegment();
  if (segment) renderBeatEvidence(segment);
  else renderOverviewEvidence();
  renderReviewPanel();
}

function reviewChanged() {
  state.review.ready = computeLocalSummary().ready;
  state.summaries.set(state.lesson.id, computeLocalSummary());
  elements["save-state"].textContent = "尚未儲存";
  if (state.saveTimer) clearTimeout(state.saveTimer);
  state.saveTimer = setTimeout(saveReview, 450);
}

async function saveReview() {
  if (!state.lesson || !state.review) return;
  state.saveTimer = null;
  const sequence = ++state.saveSequence;
  elements["save-state"].textContent = "儲存中";
  try {
    const payload = await requestJSON(`/api/reviews/${encodeURIComponent(state.lesson.id)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state.review),
    });
    if (sequence !== state.saveSequence || !state.lesson) return;
    state.review = payload.review;
    state.stale = false;
    state.summaries.set(state.lesson.id, payload.summary);
    elements["save-state"].textContent = "已儲存";
    renderReviewHeader();
    renderSegmentNav();
    renderReadiness();
  } catch (error) {
    if (sequence !== state.saveSequence) return;
    elements["save-state"].textContent = `儲存失敗：${error.message}`;
  }
}

function openLightbox(url, alt) {
  elements["lightbox-image"].src = url;
  elements["lightbox-image"].alt = alt;
  elements.lightbox.showModal();
}

function closeLightbox() {
  elements.lightbox.close();
  elements["lightbox-image"].removeAttribute("src");
}

async function routeFromLocation({ replace = false } = {}) {
  const params = new URLSearchParams(location.search);
  const lessonId = params.get("lesson");
  if (lessonId) {
    await openLesson(lessonId, {
      beat: params.get("beat"),
      historyMode: replace ? "replace" : "none",
    });
  } else {
    showList({ historyMode: replace ? "replace" : "none" });
  }
}

async function initialize() {
  try {
    const [catalog, reviewPayload] = await Promise.all([
      requestJSON("/catalog.json"),
      requestJSON("/api/reviews"),
    ]);
    state.catalog = catalog;
    for (const summary of reviewPayload.reviews) {
      state.summaries.set(summary.lesson_id, summary);
    }
    elements["generated-at"].textContent = `證據索引更新：${formatDate(catalog.generated_at)}`;
    populateCollectionFilter();
    renderList();
    await routeFromLocation({ replace: true });
  } catch (error) {
    document.querySelector("main").replaceChildren(
      make("section", { className: "empty-state" }, [
        make("h1", { text: "無法載入本機檢閱站" }),
        make("p", { text: error.message }),
      ])
    );
  }
}

elements["search-input"].addEventListener("input", renderLessonRows);
elements["collection-filter"].addEventListener("change", renderLessonRows);
elements["status-filter"].addEventListener("change", renderLessonRows);
elements["back-button"].addEventListener("click", () => showList());
elements["lightbox-close"].addEventListener("click", closeLightbox);
elements.lightbox.addEventListener("click", (event) => {
  if (event.target === elements.lightbox) closeLightbox();
});
window.addEventListener("popstate", () => routeFromLocation());

initialize();
