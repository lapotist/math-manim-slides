"use strict";

const state = {
  manifest: null,
  lessons: [],
  filteredLessons: [],
  lessonIndex: 0,
  segmentIndex: 0,
  statusByLesson: new Map(),
  statusTimer: null,
};

const elements = {
  body: document.body,
  sidebar: document.querySelector("#problem-sidebar"),
  sidebarToggle: document.querySelector("#sidebar-toggle"),
  sidebarScrim: document.querySelector("#sidebar-scrim"),
  search: document.querySelector("#problem-search"),
  collection: document.querySelector("#collection-filter"),
  filterCount: document.querySelector("#filter-count"),
  problemList: document.querySelector("#problem-list"),
  libraryCount: document.querySelector("#library-count"),
  loading: document.querySelector("#loading-state"),
  error: document.querySelector("#error-state"),
  view: document.querySelector("#lesson-view"),
  main: document.querySelector("#lesson-main"),
  context: document.querySelector("#lesson-context"),
  title: document.querySelector("#lesson-title"),
  status: document.querySelector("#lesson-status"),
  statusTime: document.querySelector("#status-time"),
  video: document.querySelector("#lesson-video"),
  videoMessage: document.querySelector("#video-message"),
  previous: document.querySelector("#previous-segment"),
  next: document.querySelector("#next-segment"),
  segmentPosition: document.querySelector("#segment-position"),
  segmentTitle: document.querySelector("#segment-title"),
  chapterTrack: document.querySelector("#chapter-track"),
  chapterList: document.querySelector("#chapter-list"),
  problemText: document.querySelector("#problem-text"),
  sourceAsset: document.querySelector("#source-asset"),
  sourceLocator: document.querySelector("#source-locator"),
  sourceActions: document.querySelector("#source-actions"),
  qaLink: document.querySelector("#qa-link"),
  metadataLink: document.querySelector("#metadata-link"),
  lessonId: document.querySelector("#lesson-id"),
};

const STATUS_LABELS = {
  not_started: "尚未檢閱",
  in_progress: "檢閱中",
  changes_needed: "需修正",
  review_complete: "檢閱完成",
  verified: "已驗證",
  stale: "檢閱需更新",
  mechanical_passed: "機械檢查通過",
};

function currentLesson() {
  return state.lessons[state.lessonIndex];
}

function currentSegment() {
  return currentLesson()?.segments[state.segmentIndex];
}

function formatDuration(value) {
  if (!Number.isFinite(value) || value <= 0) return "";
  const seconds = Math.round(value);
  const minutes = Math.floor(seconds / 60);
  const remainder = String(seconds % 60).padStart(2, "0");
  return `${minutes}:${remainder}`;
}

function formatStatusTime(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.valueOf())) return "";
  return new Intl.DateTimeFormat("zh-TW", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function setSidebar(open) {
  elements.body.classList.toggle("sidebar-open", open);
  elements.sidebarToggle.setAttribute("aria-expanded", String(open));
  elements.sidebarToggle.setAttribute(
    "aria-label",
    open ? "關閉題目清單" : "開啟題目清單",
  );
}

function updateUrl(replace = false) {
  const lesson = currentLesson();
  if (!lesson) return;
  const url = new URL(window.location.href);
  url.searchParams.set("lesson", lesson.id);
  url.searchParams.set("segment", String(state.segmentIndex + 1));
  const method = replace ? "replaceState" : "pushState";
  window.history[method](null, "", url);
}

function sourceLink(label, href) {
  const anchor = document.createElement("a");
  anchor.textContent = label;
  anchor.href = href;
  anchor.target = "_blank";
  anchor.rel = "noopener";
  return anchor;
}

function renderSourceActions(lesson) {
  const actions = [];
  if (lesson.original_source_url) {
    actions.push(sourceLink("查看原始題目", lesson.original_source_url));
  } else {
    const unavailable = document.createElement("span");
    unavailable.className = "source-unavailable";
    unavailable.textContent = "來源檔未公開";
    actions.push(unavailable);
  }
  if (lesson.solution_url) {
    actions.push(sourceLink("查看解題來源", lesson.solution_url));
  }
  elements.sourceActions.replaceChildren(...actions);
}

function effectiveStatus(lesson) {
  if (lesson.review_state === "human_reviewed") {
    return { status: "verified", updated_at: lesson.verified_at };
  }
  const live = state.statusByLesson.get(lesson.id);
  if (
    live &&
    live.review_binding_digest === lesson.review_binding_digest &&
    Object.hasOwn(STATUS_LABELS, live.status)
  ) {
    return live;
  }
  return { status: "mechanical_passed", updated_at: null };
}

function renderStatus() {
  const lesson = currentLesson();
  if (!lesson) return;
  const status = effectiveStatus(lesson);
  elements.status.dataset.status = status.status;
  elements.status.textContent = STATUS_LABELS[status.status] || STATUS_LABELS.not_started;
  elements.statusTime.textContent = formatStatusTime(status.updated_at);
}

function problemButton(lesson, lessonIndex) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "problem-item";
  button.dataset.lessonId = lesson.id;
  button.setAttribute("aria-current", String(lessonIndex === state.lessonIndex));

  let thumbnail;
  if (lesson.thumbnail_path) {
    thumbnail = document.createElement("img");
    thumbnail.className = "problem-thumb";
    thumbnail.src = lesson.thumbnail_path;
    thumbnail.alt = "";
    thumbnail.loading = "lazy";
  } else {
    thumbnail = document.createElement("span");
    thumbnail.className = "problem-thumb problem-thumb-placeholder";
    thumbnail.textContent = "動畫";
  }

  const copy = document.createElement("span");
  copy.className = "problem-item-copy";
  const number = document.createElement("span");
  number.className = "problem-number";
  number.textContent = lesson.problem_label;
  const name = document.createElement("span");
  name.className = "problem-name";
  name.textContent = lesson.problem_display.text;
  const segments = document.createElement("span");
  segments.className = "problem-segments";
  segments.textContent = `${lesson.segment_count} 個片段`;
  copy.append(number, name, segments);
  button.append(thumbnail, copy);
  button.addEventListener("click", () => selectLesson(lessonIndex, 0));
  return button;
}

function applyFilters() {
  const query = elements.search.value.trim().toLocaleLowerCase("zh-Hant");
  const collectionId = elements.collection.value;
  state.filteredLessons = state.lessons.filter((lesson) => {
    const searchable = [
      lesson.id,
      lesson.title,
      lesson.problem_label,
      lesson.collection_title,
      lesson.problem_display?.text,
      ...(lesson.tags || []),
    ].join(" ").toLocaleLowerCase("zh-Hant");
    return (
      (!query || searchable.includes(query)) &&
      (!collectionId || lesson.collection_id === collectionId)
    );
  });
  renderProblemList();
}

function renderProblemList() {
  const fragment = document.createDocumentFragment();
  let previousCollection = null;
  for (const lesson of state.filteredLessons) {
    if (lesson.collection_id !== previousCollection) {
      const divider = document.createElement("p");
      divider.className = "collection-divider";
      divider.textContent = lesson.collection_title;
      fragment.append(divider);
      previousCollection = lesson.collection_id;
    }
    fragment.append(problemButton(lesson, state.lessons.indexOf(lesson)));
  }
  if (!state.filteredLessons.length) {
    const empty = document.createElement("p");
    empty.className = "filter-count";
    empty.textContent = "沒有符合條件的題目。";
    fragment.append(empty);
  }
  elements.problemList.replaceChildren(fragment);
  elements.filterCount.textContent = `顯示 ${state.filteredLessons.length} / ${state.lessons.length} 題`;
}

function buildChapterControls(lesson) {
  const track = document.createDocumentFragment();
  const list = document.createDocumentFragment();
  for (const [index, segment] of lesson.segments.entries()) {
    const trackButton = document.createElement("button");
    trackButton.type = "button";
    trackButton.role = "tab";
    trackButton.style.flexGrow = String(segment.duration || 1);
    trackButton.setAttribute("aria-label", `${index + 1}. ${segment.title}`);
    trackButton.title = segment.title;
    trackButton.addEventListener("click", () => selectSegment(index));
    track.append(trackButton);

    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "chapter-button";
    const number = document.createElement("span");
    number.className = "chapter-number";
    number.textContent = String(index + 1).padStart(2, "0");
    const name = document.createElement("span");
    name.className = "chapter-name";
    name.textContent = segment.title;
    const meta = document.createElement("span");
    meta.className = "chapter-meta";
    const parts = [];
    if (segment.loop) parts.push("循環");
    const duration = formatDuration(segment.duration);
    if (duration) parts.push(duration);
    meta.textContent = parts.join(" · ");
    button.append(number, name, meta);
    button.addEventListener("click", () => selectSegment(index));
    item.append(button);
    list.append(item);
  }
  elements.chapterTrack.replaceChildren(track);
  elements.chapterList.replaceChildren(list);
}

function updateChapterSelection() {
  const lesson = currentLesson();
  const segment = currentSegment();
  if (!lesson || !segment) return;
  const trackButtons = [...elements.chapterTrack.querySelectorAll("button")];
  const listButtons = [...elements.chapterList.querySelectorAll("button")];
  trackButtons.forEach((button, index) => {
    button.setAttribute("aria-selected", String(index === state.segmentIndex));
    button.tabIndex = index === state.segmentIndex ? 0 : -1;
  });
  listButtons.forEach((button, index) => {
    button.setAttribute("aria-current", String(index === state.segmentIndex));
  });
  listButtons[state.segmentIndex]?.scrollIntoView({ block: "nearest" });
  elements.segmentPosition.textContent = `片段 ${state.segmentIndex + 1} / ${lesson.segments.length}`;
  elements.segmentTitle.textContent = segment.title;
  elements.previous.disabled = state.segmentIndex === 0;
  elements.next.disabled = state.segmentIndex === lesson.segments.length - 1;
}

function selectSegment(index, replaceUrl = false) {
  const lesson = currentLesson();
  if (!lesson || !lesson.segments.length) return;
  state.segmentIndex = Math.max(0, Math.min(index, lesson.segments.length - 1));
  const segment = currentSegment();
  elements.videoMessage.hidden = true;
  elements.video.pause();
  elements.video.loop = Boolean(segment.loop);
  elements.video.src = segment.path;
  elements.video.poster = lesson.thumbnail_path || "";
  elements.video.load();
  updateChapterSelection();
  updateUrl(replaceUrl);
}

function renderLesson(lesson) {
  elements.context.textContent = lesson.collection_title;
  elements.title.textContent = lesson.problem_label;
  document.title = `${lesson.problem_label} | 數學動畫題庫`;
  elements.problemText.textContent = lesson.problem_display.text;
  elements.sourceAsset.textContent = lesson.source_asset || "未記錄";
  elements.sourceLocator.textContent = lesson.source_locator || "未記錄";
  renderSourceActions(lesson);
  elements.qaLink.href = lesson.qa_path;
  elements.metadataLink.href = lesson.metadata_url;
  elements.lessonId.textContent = lesson.id;
  buildChapterControls(lesson);
  renderStatus();
}

function selectLesson(index, segmentIndex = 0, replaceUrl = false) {
  if (index < 0 || index >= state.lessons.length) return;
  state.lessonIndex = index;
  renderLesson(currentLesson());
  selectSegment(segmentIndex, replaceUrl);
  renderProblemList();
  setSidebar(false);
}

function readLocation() {
  const params = new URLSearchParams(window.location.search);
  const requestedId = params.get("lesson");
  const lessonIndex = Math.max(
    0,
    state.lessons.findIndex((lesson) => lesson.id === requestedId),
  );
  const requestedSegment = Number.parseInt(params.get("segment") || "1", 10);
  const segmentIndex = Number.isFinite(requestedSegment)
    ? Math.max(0, requestedSegment - 1)
    : 0;
  selectLesson(lessonIndex, segmentIndex, true);
}

async function fetchJson(url) {
  const separator = url.includes("?") ? "&" : "?";
  const response = await fetch(`${url}${separator}t=${Date.now()}`, {
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json();
}

async function refreshStatuses() {
  if (!state.manifest) return;
  const candidates = ["review-status.json", state.manifest.review_status_url]
    .filter(Boolean)
    .filter((value, index, values) => values.indexOf(value) === index);
  const merged = new Map();
  for (const url of candidates) {
    try {
      const feed = await fetchJson(url);
      if (feed.schema_version !== 1 || !Array.isArray(feed.lessons)) continue;
      for (const entry of feed.lessons) {
        const lesson = state.lessons.find((item) => item.id === entry?.lesson_id);
        if (
          lesson &&
          entry.review_binding_digest === lesson.review_binding_digest
        ) {
          merged.set(entry.lesson_id, entry);
        }
      }
    } catch (_) {
      // The bundled feed remains the fallback when the repository feed is absent.
    }
  }
  if (merged.size) {
    state.statusByLesson = merged;
    renderStatus();
  }
}

function isTypingTarget(target) {
  return target instanceof HTMLElement && (
    target.isContentEditable ||
    ["INPUT", "TEXTAREA", "SELECT", "BUTTON"].includes(target.tagName)
  );
}

function bindEvents() {
  elements.sidebarToggle.addEventListener("click", () => {
    setSidebar(!elements.body.classList.contains("sidebar-open"));
  });
  elements.sidebarScrim.addEventListener("click", () => setSidebar(false));
  elements.search.addEventListener("input", applyFilters);
  elements.collection.addEventListener("change", applyFilters);
  elements.previous.addEventListener("click", () => {
    if (state.segmentIndex > 0) selectSegment(state.segmentIndex - 1);
  });
  elements.next.addEventListener("click", () => {
    if (state.segmentIndex < currentLesson().segments.length - 1) {
      selectSegment(state.segmentIndex + 1);
    }
  });
  elements.video.addEventListener("ended", () => {
    if (!currentSegment()?.loop && state.segmentIndex < currentLesson().segments.length - 1) {
      selectSegment(state.segmentIndex + 1);
    }
  });
  elements.video.addEventListener("error", () => {
    elements.videoMessage.textContent = "這個動畫片段目前無法播放。";
    elements.videoMessage.hidden = false;
  });
  window.addEventListener("keydown", (event) => {
    if (isTypingTarget(event.target)) return;
    const lesson = currentLesson();
    if (!lesson) return;
    if (event.key === "ArrowRight") {
      if (state.segmentIndex < lesson.segments.length - 1) {
        event.preventDefault();
        selectSegment(state.segmentIndex + 1);
      }
    } else if (event.key === "ArrowLeft") {
      if (state.segmentIndex > 0) {
        event.preventDefault();
        selectSegment(state.segmentIndex - 1);
      }
    } else if (event.key === "Escape") {
      setSidebar(false);
    }
  });
  window.addEventListener("popstate", readLocation);
}

async function start() {
  bindEvents();
  try {
    const manifest = window.__MATH_LESSON_LIBRARY__ ||
      await fetchJson("site-manifest.json");
    if (manifest.schema_version !== 2 || !Array.isArray(manifest.lessons)) {
      throw new Error("題庫資料格式不相容");
    }
    if (!manifest.lessons.length) throw new Error("題庫目前沒有可播放的題目");
    state.manifest = manifest;
    state.lessons = manifest.lessons;
    state.filteredLessons = state.lessons;
    elements.libraryCount.textContent = `${state.lessons.length} 題`;

    const collections = new Map();
    for (const lesson of state.lessons) {
      collections.set(lesson.collection_id, lesson.collection_title);
    }
    for (const [id, title] of collections) {
      const option = document.createElement("option");
      option.value = id;
      option.textContent = title;
      elements.collection.append(option);
    }

    elements.loading.hidden = true;
    elements.view.hidden = false;
    readLocation();
    await refreshStatuses();
    state.statusTimer = window.setInterval(refreshStatuses, 30000);
  } catch (error) {
    elements.loading.hidden = true;
    elements.error.hidden = false;
    elements.error.textContent = `無法載入題庫：${error.message}`;
  }
}

start();
