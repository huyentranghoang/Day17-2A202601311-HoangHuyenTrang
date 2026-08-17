"""Bonus mini-product UI — Lab 17 memory agent demo (STUDENT).

Checklist +10 (LAB.md §4.8 / §5.3):

1. Load test cases from `data/sessions.json` (golden optional).
2. Pick a case → show query, expected layer, user_id, thread_id.
3. Run student retrieval → per-layer evidence + merged context.
4. Chat tiếp trên đúng user/thread: history + retrieve lại.

Run:

    docker compose run --rm --service-ports app \\
      streamlit run src/demo_ui.py --server.address 0.0.0.0 --server.port 8501
"""

from __future__ import annotations

import html
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

from src.config import settings
from src.llm import gemini_available, generate_reply
from src.memory_student import StudentMemory
from src.short_term import ShortTermMemory
from src.utils import GOLDEN_PATH, load_dataset, load_json
from src.zep_common import get_zep_client

LAYER_COLORS = {
    "short_term": "#0f766e",
    "long_term": "#047857",
    "episodic": "#b45309",
    "semantic": "#1d4ed8",
    "mixed": "#334155",
}

LAYER_LABELS = {
    "short_term": "Short-term",
    "long_term": "Long-term",
    "episodic": "Episodic",
    "semantic": "Semantic",
    "mixed": "Mixed",
}

# Be Vietnam Pro: đọc tiếng Việt rõ; IBM Plex Sans fallback.
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, .stText, .stCaption, button, input, textarea {
  font-family: "Be Vietnam Pro", "IBM Plex Sans", "Segoe UI", sans-serif !important;
}
.block-container {
  padding-top: .8rem;
  padding-bottom: 2rem;
  max-width: 860px;
}
[data-testid="stAppViewContainer"] {
  background: #f7f8f6;
}
/* Sidebar tối — chữ sáng; ô trắng → chữ đen */
[data-testid="stSidebar"] {
  background: #14242b;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: #e8eef0 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
  background: #ffffff !important;
  border-color: #d0d7db !important;
  color: #111827 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] *,
[data-testid="stSidebar"] div[data-baseweb="popover"] * {
  color: #111827 !important;
}
/* Nút case trắng → chữ đen (override màu sáng của sidebar) */
[data-testid="stSidebar"] button,
[data-testid="stSidebar"] button p,
[data-testid="stSidebar"] button span,
[data-testid="stSidebar"] button div,
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button * {
  background: #ffffff !important;
  color: #111827 !important;
  border: 1px solid #d0d7db !important;
  fill: #111827 !important;
}
[data-testid="stSidebar"] .stButton > button {
  text-align: left !important;
  justify-content: flex-start !important;
  white-space: normal !important;
  height: auto !important;
  min-height: 2.2rem;
  padding: .45rem .65rem !important;
  font-size: .82rem !important;
  line-height: 1.35 !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton > button:hover * {
  background: #f3f4f6 !important;
  color: #000000 !important;
  border-color: #9ca3af !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 10px;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary,
[data-testid="stSidebar"] [data-testid="stExpander"] summary *,
[data-testid="stSidebar"] .streamlit-expanderHeader,
[data-testid="stSidebar"] .streamlit-expanderHeader * {
  color: #f8fafc !important;
}
.hero {
  margin: -.4rem 0 1rem;
  padding: 1rem 0 .2rem;
}
.hero-brand {
  font-size: 1.55rem;
  font-weight: 700;
  color: #14242b;
  margin: 0 0 .25rem;
  letter-spacing: -.01em;
}
.hero-sub {
  margin: 0 0 .85rem;
  color: #4b5c63;
  font-size: .92rem;
  line-height: 1.45;
}
.steps {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: .45rem;
}
@media (max-width: 800px) {
  .steps { grid-template-columns: 1fr 1fr; }
}
.step {
  background: #fff;
  border: 1px solid #dde3e6;
  border-radius: 10px;
  padding: .5rem .55rem;
  font-size: .78rem;
  color: #334155;
  line-height: 1.35;
}
.step b {
  display: block;
  font-size: .7rem;
  letter-spacing: .03em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: .12rem;
}
.meta {
  font-size: .84rem;
  color: #475569;
  margin: 0 0 .75rem;
  line-height: 1.45;
}
.meta b { color: #0f172a; }
.answer-box {
  background: #fff;
  border: 1px solid #dde3e6;
  border-radius: 12px;
  padding: .9rem 1rem;
  margin: .55rem 0 .85rem;
  color: #0f172a;
  font-size: .98rem;
  line-height: 1.5;
}
.lab-badge {
  display: inline-block;
  padding: .15rem .5rem;
  border-radius: 999px;
  color: #fff;
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .03em;
  text-transform: uppercase;
  margin-right: .35rem;
}
.evidence-box {
  white-space: pre-wrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: .78rem;
  line-height: 1.4;
  background: #0f1f24;
  color: #d7ebea;
  border-radius: 8px;
  padding: .75rem .85rem;
  max-height: 260px;
  overflow: auto;
}
.layer-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: .45rem;
}
.budget-card {
  border-radius: 8px;
  padding: .5rem .6rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-top: 3px solid var(--accent, #0f766e);
}
.budget-card .lbl { font-size: .7rem; color: #64748b; text-transform: uppercase; }
.budget-card .val { font-size: 1.05rem; font-weight: 700; color: #0f172a; }
.budget-card .sub { font-size: .7rem; color: #94a3b8; }
div[data-testid="stChatMessage"] {
  background: #fff;
  border: 1px solid #dde3e6;
  border-radius: 12px;
}
.chat-hint {
  font-size: .82rem;
  color: #64748b;
  margin: 0 0 .55rem;
}
"""


def load_cases(source: str) -> list[dict[str, Any]]:
    """Load practice, golden, or both. Golden prefers data/golden_eval.json."""
    if source == "practice":
        return list(load_dataset()["evaluations"])

    golden: list[dict[str, Any]] = []
    if GOLDEN_PATH.exists():
        try:
            golden = list(load_json(GOLDEN_PATH).get("evaluations") or [])
        except Exception:
            golden = []
    # Fallback: root golden_eval.json (local copy before instructor path)
    root_golden = _ROOT / "golden_eval.json"
    if not golden and root_golden.exists():
        try:
            golden = list(load_json(root_golden).get("evaluations") or [])
        except Exception:
            golden = []

    if source == "golden":
        return golden
    return list(load_dataset()["evaluations"]) + golden


def layer_badge(layer: str) -> str:
    color = LAYER_COLORS.get(layer, "#475569")
    label = LAYER_LABELS.get(layer, layer)
    return f'<span class="lab-badge" style="background:{color}">{html.escape(label)}</span>'


def _thread_messages(dataset: dict[str, Any], user_id: str, thread_id: str) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for user in dataset.get("users", []):
        if user.get("user_id") != user_id:
            continue
        for session in user.get("sessions", []):
            if session.get("thread_id") != thread_id:
                continue
            for msg in session.get("messages", []):
                content = msg.get("content", "")
                if content:
                    messages.append({"role": msg.get("role", "user"), "content": content})
    return messages


def retrieve_for_case(
    memory: StudentMemory,
    case: dict[str, Any],
    extra_messages: list[dict[str, str]],
) -> dict[str, Any]:
    dataset = load_dataset()
    query = case.get("query", "")
    user_id = case["user_id"]
    thread_id = case["thread_id"]
    expected = case.get("expected_layer", "mixed")

    if expected == "mixed":
        wanted = list(case.get("retrieve_layers") or ["long_term", "semantic"])
    elif expected == "short_term":
        wanted = ["short_term"]
    else:
        wanted = ["short_term", expected]

    layers = {
        "short_term": "",
        "long_term": "",
        "episodic": "",
        "semantic": "",
    }

    if "short_term" in wanted:
        stm = ShortTermMemory(max_recent_messages=6)
        base = case.get("fixture_messages") or _thread_messages(dataset, user_id, thread_id)
        for msg in list(base) + list(extra_messages or []):
            stm.add(msg.get("role", "user"), msg.get("content", ""))
        layers["short_term"] = stm.render()

    if "long_term" in wanted:
        layers["long_term"] = memory.retrieve_long_term(user_id, thread_id, query)
    if "episodic" in wanted:
        layers["episodic"] = memory.retrieve_episodic(user_id, query)
    if "semantic" in wanted:
        layers["semantic"] = memory.retrieve_semantic(settings.semantic_graph_id, query)

    merged, budget = memory.assemble_context(layers)
    return {"merged_context": merged, "layers": layers, "budget": budget}


def _short_fallback_reply(case: dict[str, Any], context: str) -> str:
    markers = case.get("must_contain_all") or []
    found = [m for m in markers if m.casefold() in (context or "").casefold()]
    if found:
        return "Dựa trên memory: " + ", ".join(f"`{m}`" for m in found[:3]) + "."
    layer = LAYER_LABELS.get(case.get("expected_layer", ""), case.get("expected_layer", "?"))
    return f"Đã retrieve từ {layer}, nhưng chưa khớp đủ marker cần thiết."


def _answer(case: dict[str, Any], prompt: str) -> tuple[str, dict[str, Any]]:
    memory = StudentMemory(get_zep_client())
    history = list(st.session_state.get("chat") or [])
    # chat đã có lượt user hiện tại → bỏ ra khi gọi LLM (tránh lặp)
    prior = history[:-1] if history and history[-1].get("role") == "user" else history
    follow = retrieve_for_case(memory, {**case, "query": prompt}, history)
    context = follow.get("merged_context", "")
    if gemini_available():
        reply = generate_reply(context, prior, prompt)
    else:
        reply = _short_fallback_reply(case, context)
    return reply, follow


def _run_turn(case: dict[str, Any], prompt: str) -> None:
    prompt = (prompt or "").strip()
    if not prompt:
        return
    st.session_state.chat.append({"role": "user", "content": prompt})
    try:
        reply, result = _answer(case, prompt)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.session_state.last_result = result
    except Exception as exc:  # noqa: BLE001
        st.session_state.chat.append({"role": "assistant", "content": f"Lỗi: {exc}"})


def _select_case(case: dict[str, Any], *, send_query: bool = False) -> None:
    if st.session_state.get("case_id") != case["id"]:
        st.session_state.case_id = case["id"]
        st.session_state.chat = []
        st.session_state.pop("last_result", None)
    # Nạp câu hỏi vào ô chat (gửi ở vòng render sau)
    st.session_state.pending_prompt = case.get("query", "")
    if send_query:
        st.session_state.auto_send = True


def _render_evidence(result: dict[str, Any]) -> None:
    active = [k for k, v in result["layers"].items() if v.strip()]
    st.markdown(
        " ".join(layer_badge(k) for k in active) or "_(trống)_",
        unsafe_allow_html=True,
    )

    with st.expander("Token budget", expanded=False):
        if result.get("budget"):
            cards = []
            for layer in ("short_term", "long_term", "episodic", "semantic"):
                b = result["budget"].get(layer, {})
                accent = LAYER_COLORS.get(layer, "#0f766e")
                cards.append(
                    f'<div class="budget-card" style="--accent:{accent}">'
                    f'<div class="lbl">{html.escape(LAYER_LABELS[layer])}</div>'
                    f'<div class="val">{int(b.get("used_tokens", 0))} tok</div>'
                    f'<div class="sub">limit {int(b.get("limit_tokens", 0))}</div>'
                    f"</div>"
                )
            st.markdown(f'<div class="layer-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

    with st.expander("Merged context", expanded=False):
        st.markdown(
            f'<div class="evidence-box">{html.escape(result.get("merged_context") or "(empty)")}</div>',
            unsafe_allow_html=True,
        )
    for name, text in result["layers"].items():
        if text.strip():
            with st.expander(f"{LAYER_LABELS.get(name, name)}", expanded=False):
                st.markdown(
                    f'<div class="evidence-box">{html.escape(text)}</div>',
                    unsafe_allow_html=True,
                )


def main() -> None:
    st.set_page_config(page_title="Memora · Lab 17", page_icon="🧬", layout="wide")
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero">
          <p class="hero-brand">Memora</p>
          <p class="hero-sub">Chọn case → chat nhiều lượt → Enter để gửi → mở evidence khi cần.</p>
          <div class="steps">
            <div class="step"><b>Bước 1</b>Load case (practice / golden)</div>
            <div class="step"><b>Bước 2</b>Xem layer · user · thread</div>
            <div class="step"><b>Bước 3</b>Chat hội thoại · Enter gửi</div>
            <div class="step"><b>Bước 4</b>Mở rộng xem evidence</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### Bộ câu hỏi")
        source = st.radio(
            "Nguồn",
            options=["golden", "practice", "all"],
            format_func=lambda x: {
                "golden": "Golden set",
                "practice": "Practice E01–E11",
                "all": "Cả hai",
            }[x],
            index=0,
            label_visibility="collapsed",
        )
        cases = load_cases(source)
        if not cases:
            st.error(
                "Chưa có golden. Copy file vào `data/golden_eval.json` "
                "(hoặc để `golden_eval.json` ở root)."
            )
            return

        st.caption(f"{len(cases)} case")

        with st.expander("Danh sách case (bấm mở)", expanded=True):
            for c in cases:
                layer = LAYER_LABELS.get(c["expected_layer"], c["expected_layer"])
                label = f"{c['id']} · {layer}"
                if st.button(label, key=f"pick-{c['id']}", use_container_width=True):
                    # Chọn case + nạp query vào hội thoại (gửi ngay như mở chat)
                    _select_case(c, send_query=True)
                    st.rerun()

        current_id = st.session_state.get("case_id") or cases[0]["id"]
        case = next((c for c in cases if c["id"] == current_id), cases[0])
        st.session_state.case_id = case["id"]

        with st.expander("Câu hỏi của case này", expanded=False):
            q = case.get("query", "")
            st.caption(q[:280] + ("…" if len(q) > 280 else ""))
            if st.button("Gửi lại query case", key=f"send-q-{case['id']}", use_container_width=True):
                st.session_state.pending_prompt = q
                st.session_state.auto_send = True
                st.rerun()

    if "chat" not in st.session_state:
        st.session_state.chat = []

    st.markdown(
        f"""
        <p class="meta">
          {layer_badge(case.get("expected_layer", "?"))}
          <b>{html.escape(case["id"])}</b>
          · user <b>{html.escape(str(case.get("user_id", "-")))}</b>
          · thread <b>{html.escape(str(case.get("thread_id", "-")))}</b>
        </p>
        """,
        unsafe_allow_html=True,
    )

    clear_col, _ = st.columns([1, 3])
    if clear_col.button("Xóa hội thoại", use_container_width=True):
        st.session_state.chat = []
        st.session_state.pop("last_result", None)
        st.session_state.pop("pending_prompt", None)
        st.session_state.pop("auto_send", None)
        st.rerun()

    st.markdown(
        '<p class="chat-hint">Hội thoại chatbot — bấm case bên trái để hỏi query đó; '
        "rồi hỏi tiếp nhiều lượt, Enter để gửi.</p>",
        unsafe_allow_html=True,
    )

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Case click → gửi query vào hội thoại
    pending = st.session_state.pop("pending_prompt", None)
    auto_send = st.session_state.pop("auto_send", False)
    if auto_send and pending:
        with st.spinner("Đang trả lời…"):
            _run_turn(case, pending)
        st.rerun()

    prompt = st.chat_input("Nhập câu hỏi rồi Enter…")
    if prompt:
        with st.spinner("Đang trả lời…"):
            _run_turn(case, prompt)
        st.rerun()

    result = st.session_state.get("last_result")
    if result:
        with st.expander("Xem chi tiết kết quả (evidence)", expanded=False):
            _render_evidence(result)


if __name__ == "__main__":
    main()
