"""
Field Shift - Crop Rotation Helper
NASA Space Apps Challenge
"""

import re
import streamlit as st
import scoring as sc
from scoring import TALUK_KN, SOIL_KN, PRIORITY, SEASON, ZONE_FACTS

st.set_page_config(
    page_title="Field Shift — Crop Rotation Helper",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =====================================================================
# CSS Design System — Field Shift
# Warm off-white canvas, forest-green accents, card-based layouts
# =====================================================================
st.markdown(
    """
<style>
/* ── Color System: Variables ── */
:root {
    --forest-green:       #2A5C2A;
    --forest-green-dark:  #1B3D1B;
    --forest-green-mid:   #3A6E3A;
    --sage-green:         #6B8F5E;
    --sage-light:         #9BBD8D;
    --sage-pale:          #C8DFBC;
    --sage-ultra-pale:    #EBF3E6;
    --warm-white:         #F8F6F1;
    --off-white:          #F2EDE5;
    --card-white:         #FFFFFF;
    --text-primary:       #182818;
    --text-secondary:     #3D5240;
    --text-muted:         #4A6052;
    --text-light:         #526E59;
    --border-light:       #DDE8D7;
    --border-mid:         #C4D9BB;
    --warning-bg:         #FFFBEE;
    --warning-border:     #D4A017;
    --warning-text:       #6B4F00;
    --success-bg:         #EBF5EC;
    --success-border:     #3D9A42;
    --info-bg:            #E8F2FC;
    --info-border:        #3A87CC;
    --shadow-xs:          0 1px 2px rgba(0,0,0,0.05);
    --shadow-sm:          0 2px 6px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:          0 4px 14px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
    --shadow-lg:          0 8px 24px rgba(0,0,0,0.10), 0 3px 8px rgba(0,0,0,0.05);
    --shadow-green:       0 4px 16px rgba(42,92,42,0.22);
    --radius-sm:          8px;
    --radius-md:          12px;
    --radius-lg:          16px;
    --radius-xl:          20px;
    --transition:         all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── App canvas background ── */
.stApp {
    background-color: var(--warm-white) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: var(--warm-white); }
::-webkit-scrollbar-thumb {
    background: var(--sage-light);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: var(--sage-green); }

/* ── Hide Streamlit chrome ── */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
div[data-testid="stReportProgress"] {
    display: none !important;
    visibility: hidden !important;
}

/* ── Page container constraints ── */
.block-container {
    max-width: 740px !important;
    padding: 0.5rem 1.1rem 4rem 1.1rem !important;
}

/* ── Typography scale: dark forest green headings by default ── */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6,
[data-testid="stHeadingWithActionElements"] h1,
[data-testid="stHeadingWithActionElements"] h2,
[data-testid="stHeadingWithActionElements"] h3 {
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif !important;
    color: var(--forest-green-dark) !important;
    letter-spacing: -0.01em;
}

/* ── Headings and text inside white cards and containers must be dark and clearly readable ── */
div[style*="background: #FFFFFF"] h1,
div[style*="background: #FFFFFF"] h2,
div[style*="background: #FFFFFF"] h3,
div[style*="background: #FFFFFF"] h4,
div[style*="background:#FFFFFF"] h1,
div[style*="background:#FFFFFF"] h2,
div[style*="background:#FFFFFF"] h3,
div[style*="background:#FFFFFF"] h4,
div[style*="background: #ffffff"] h1,
div[style*="background: #ffffff"] h2,
div[style*="background: #ffffff"] h3,
div[style*="background: #ffffff"] h4,
div[style*="background: var(--card-white)"] h1,
div[style*="background: var(--card-white)"] h2,
div[style*="background: var(--card-white)"] h3,
div[style*="background-color: var(--card-white)"] h1,
div[style*="background-color: var(--card-white)"] h2,
div[style*="background-color: var(--card-white)"] h3,
.stExpander h1, .stExpander h2, .stExpander h3,
[data-testid="stExpander"] h1, [data-testid="stExpander"] h2, [data-testid="stExpander"] h3 {
    color: var(--forest-green-dark) !important;
}

/* ── Paragraph and label base styling with high contrast ── */
p, li, label,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif !important;
    color: var(--text-primary);
}

span:not([data-testid="stIconMaterial"]):not([class*="material"]),
div:not([data-testid="stIconMaterial"]):not([class*="material"]) {
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif;
}

/* ── Header titles on dark green backgrounds must stay pure white ── */
.dark-header-card,
.dark-header-card h1,
.dark-header-card h2,
.dark-header-card h3,
.dark-header-card p,
.dark-header-card div,
.dark-header-card span,
.dark-header-card [data-testid="stMarkdownContainer"] h1,
.dark-header-card [data-testid="stMarkdownContainer"] h2,
.dark-header-card [data-testid="stMarkdownContainer"] h3,
.dark-header-card [data-testid="stMarkdownContainer"] p,
.dark-header-card [data-testid="stMarkdownContainer"] span {
    color: #FFFFFF !important;
}

/* ── Language bar: sticky at top ── */
div[data-testid="stRadio"]:first-of-type {
    position: sticky;
    top: 0;
    z-index: 100;
    background: var(--warm-white);
    padding: 0.5rem 0 0.4rem 0;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 0.6rem !important;
}

div[data-testid="stRadio"] > div {
    gap: 0.45rem !important;
    flex-wrap: wrap !important;
}

div[data-testid="stRadio"] label {
    font-size: 0.93rem !important;
    padding: 0.45rem 1.1rem !important;
    border-radius: 100px !important;
    border: 2px solid var(--border-mid) !important;
    background: var(--card-white) !important;
    transition: var(--transition) !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    cursor: pointer;
    box-shadow: var(--shadow-xs) !important;
}

div[data-testid="stRadio"] label:hover {
    border-color: var(--sage-green) !important;
    background: var(--sage-ultra-pale) !important;
}

div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--forest-green) !important;
    color: #FFFFFF !important;
    border-color: var(--forest-green) !important;
    box-shadow: 0 2px 8px rgba(42,92,42,0.3) !important;
}

/* Radio label text in Streamlit */
div[data-testid="stRadio"] label p {
    font-size: inherit !important;
    font-weight: inherit !important;
    color: inherit !important;
    margin: 0 !important;
}

/* ── Selectbox styling ── */
div[data-testid="stSelectbox"] {
    margin-bottom: 0.6rem !important;
}

/* Dropdown box container */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stSelectbox"] [data-testid="stSelectbox"] > div {
    border-radius: var(--radius-md) !important;
    border: 2px solid var(--border-light) !important;
    background: var(--card-white) !important;
    min-height: 50px !important;
    font-size: 1rem !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-xs) !important;
}

/* Dropdown focus border */
div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stSelectbox"] [data-focus-within] {
    border-color: #245B32 !important;
    box-shadow: 0 0 0 3px rgba(36,91,50,0.15) !important;
}

/* Dropdown label */
div[data-testid="stSelectbox"] label {
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
    margin-bottom: 0.25rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}

/* ── Selected value text inside closed selectbox ── */
div[data-testid="stSelectbox"] input,
div[data-testid="stSelectbox"] input.react-aria-Input,
div[data-testid="stSelectbox"] input[type="text"] {
    color: #245B32 !important;
    -webkit-text-fill-color: #245B32 !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif !important;
    background: transparent !important;
}

/* Support for BaseWeb / wrapper structures if present */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
div[data-testid="stSelectbox"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stSelectbox"] [data-testid="stSelectboxItem"] {
    color: #245B32 !important;
    -webkit-text-fill-color: #245B32 !important;
    font-weight: 600 !important;
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif !important;
}

/* Placeholder text (before any selection) */
div[data-testid="stSelectbox"] input::placeholder,
div[data-testid="stSelectbox"] [data-testid="stSelectboxPlaceholder"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] input::placeholder {
    color: #4A5D4A !important;
    -webkit-text-fill-color: #4A5D4A !important;
    font-weight: 400 !important;
    opacity: 1 !important;
}

/* Caret / arrow icon */
div[data-testid="stSelectbox"] button svg,
div[data-testid="stSelectbox"] svg {
    fill: #245B32 !important;
    color: #245B32 !important;
}

/* ── Dropdown open menu (Floating popover) ── */
[data-testid="stSelectboxVirtualDropdown"],
div[data-testid="stSelectboxVirtualDropdown"],
ul[data-testid="stSelectboxVirtualDropdown"],
div.react-aria-Popover[data-testid="stSelectboxVirtualDropdown"],
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background-color: var(--card-white) !important;
    border: 1.5px solid var(--border-mid) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-md) !important;
    padding: 6px !important;
    z-index: 999999 !important;
}

/* List container */
[data-testid="stSelectboxVirtualDropdown"] [role="listbox"],
[data-testid="stSelectboxVirtualDropdown"] .react-aria-ListBox,
[data-testid="stSelectboxVirtualDropdown"] ul {
    background-color: var(--card-white) !important;
    padding: 0 !important;
}

/* Individual option items */
[data-testid="stSelectboxVirtualDropdown"] [role="option"],
[data-testid="stSelectboxVirtualDropdown"] .react-aria-ListBoxItem,
[data-testid="stSelectboxVirtualDropdown"] li,
div[data-baseweb="popover"] li,
div[data-baseweb="menu"] li {
    background-color: var(--card-white) !important;
    color: #182818 !important;
    font-size: 0.96rem !important;
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif !important;
    padding: 0.55rem 0.85rem !important;
    margin: 2px 0 !important;
    border-radius: var(--radius-sm) !important;
    cursor: pointer !important;
    transition: var(--transition) !important;
}

/* Option text content */
[data-testid="stSelectboxVirtualDropdown"] [role="option"] *,
[data-testid="stSelectboxVirtualDropdown"] .react-aria-ListBoxItem *,
[data-testid="stSelectboxVirtualDropdown"] [data-item-hl],
div[data-baseweb="popover"] li *,
div[data-baseweb="menu"] li * {
    color: #182818 !important;
    -webkit-text-fill-color: #182818 !important;
    font-family: 'Inter', 'Noto Sans Kannada', sans-serif !important;
}

/* Hovered / Focused option */
[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover,
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"],
[data-testid="stSelectboxVirtualDropdown"] .react-aria-ListBoxItem[data-hovered],
[data-testid="stSelectboxVirtualDropdown"] .react-aria-ListBoxItem[data-focused],
[data-testid="stSelectboxVirtualDropdown"] li:hover,
div[data-baseweb="popover"] li:hover {
    background-color: var(--sage-ultra-pale) !important;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover *,
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"] *,
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"] *,
[data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-hovered="true"] [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-focused="true"] [data-item-hl],
div[data-baseweb="popover"] li:hover * {
    color: #245B32 !important;
    -webkit-text-fill-color: #245B32 !important;
    background-color: transparent !important;
}

/* Currently selected option in the open dropdown */
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
[data-testid="stSelectboxVirtualDropdown"] .react-aria-ListBoxItem[data-selected="true"],
[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"],
div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #EBF3E6 !important;
    font-weight: 700 !important;
}

[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"] *,
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] *,
[data-testid="stSelectboxVirtualDropdown"] [role="option"][data-selected="true"] [data-item-hl],
[data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"] [data-item-hl],
div[data-baseweb="popover"] li[aria-selected="true"] * {
    color: #245B32 !important;
    -webkit-text-fill-color: #245B32 !important;
    font-weight: 700 !important;
    background-color: transparent !important;
}

/* ── Stacked radio (priority, season, irrigation) ── */
div[data-testid="stRadio"] > label {
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 0.3rem !important;
}

/* ── Primary button ── */
button[kind="primary"],
.stButton > button[kind="primary"],
button[kind="primary"] p,
.stButton > button[kind="primary"] p,
button[kind="primary"] span,
.stButton > button[kind="primary"] span {
    background: linear-gradient(160deg, var(--forest-green-mid) 0%, var(--forest-green-dark) 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.9rem 2.2rem !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    box-shadow: var(--shadow-green) !important;
    transition: var(--transition) !important;
    min-height: 54px !important;
}

button[kind="primary"] p,
.stButton > button[kind="primary"] p,
button[kind="primary"] span,
.stButton > button[kind="primary"] span {
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 10px 28px rgba(42,92,42,0.32) !important;
    transform: translateY(-2px) !important;
    filter: brightness(1.07) !important;
}

button[kind="primary"]:active,
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
    box-shadow: var(--shadow-md) !important;
}

/* ── Secondary / ghost button ── */
.stButton > button,
.stButton > button p,
.stButton > button span {
    color: var(--text-primary) !important;
    border-radius: var(--radius-md) !important;
    min-height: 46px !important;
    font-size: 0.97rem !important;
    font-weight: 600 !important;
    border: 2px solid var(--border-mid) !important;
    transition: var(--transition) !important;
}

.stButton > button:hover {
    border-color: var(--sage-green) !important;
    background: var(--sage-ultra-pale) !important;
}

/* ── Strategy Expanders & General Expander Styling ── */
.stExpander details,
[data-testid="stExpander"] details {
    border: 1.5px solid var(--border-light) !important;
    border-radius: var(--radius-md) !important;
    background: var(--card-white) !important;
    margin-bottom: 0.75rem !important;
    box-shadow: var(--shadow-xs) !important;
    transition: var(--transition) !important;
    overflow: hidden !important;
}

.stExpander details:hover,
[data-testid="stExpander"] details:hover {
    border-color: var(--border-mid) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stExpander details[open],
[data-testid="stExpander"] details[open] {
    border-color: var(--sage-green) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Suppress broken Material icon ligature text in expander headers */
[data-testid="stExpander"] summary span[data-testid="stIconMaterial"],
details summary span[data-testid="stIconMaterial"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
    font-size: 0 !important;
    line-height: 0 !important;
}

/* Expander Header (Summary) */
[data-testid="stExpander"] details > summary,
[data-testid="stExpander"] summary,
details > summary,
.streamlit-expanderHeader {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    justify-content: flex-start !important;
    background: var(--card-white) !important;
    font-weight: 600 !important;
    font-size: 0.96rem !important;
    padding: 0.95rem 1.25rem !important;
    color: var(--text-primary) !important;
    cursor: pointer !important;
    user-select: none !important;
    border: none !important;
    outline: none !important;
    min-height: 52px !important;
    box-sizing: border-box !important;
    gap: 0.5rem !important;
    transition: background 0.15s ease !important;
}

/* Clean CSS-drawn chevron arrow indicator */
details[data-testid="stExpander"] > summary::before,
.stExpander details > summary::before,
details > summary::before {
    content: "" !important;
    display: inline-block !important;
    width: 8px !important;
    height: 8px !important;
    min-width: 8px !important;
    min-height: 8px !important;
    border-right: 2.5px solid var(--forest-green) !important;
    border-bottom: 2.5px solid var(--forest-green) !important;
    transform: rotate(-45deg) !important;
    transition: transform 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin-right: 0.4rem !important;
    margin-left: 0.1rem !important;
    flex-shrink: 0 !important;
}

/* Rotate chevron downward when expander is open */
details[data-testid="stExpander"][open] > summary::before,
.stExpander details[open] > summary::before,
details[open] > summary::before {
    transform: rotate(45deg) !important;
}

[data-testid="stExpander"] details > summary:hover,
[data-testid="stExpander"] summary:hover,
details > summary:hover {
    background: var(--sage-ultra-pale) !important;
}

/* Header title text container - prevent overlap & ensure alignment */
[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"],
[data-testid="stExpander"] summary p,
details > summary [data-testid="stMarkdownContainer"],
details > summary p {
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    line-height: 1.4 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: inline-block !important;
    word-break: break-word !important;
    flex: 1 1 auto !important;
}

/* Expander Details (Opened Content) */
[data-testid="stExpanderDetails"],
details > div {
    padding: 1.15rem 1.35rem !important;
    border-top: 1px solid var(--border-light) !important;
    background: #FCFBF9 !important;
}

[data-testid="stExpanderDetails"] p,
[data-testid="stExpanderDetails"] li {
    font-size: 0.9rem !important;
    line-height: 1.55 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.35rem !important;
}

[data-testid="stExpanderDetails"] strong {
    color: var(--forest-green) !important;
    font-weight: 700 !important;
}

[data-testid="stExpanderDetails"] ul {
    margin-top: 0.2rem !important;
    margin-bottom: 0.6rem !important;
    padding-left: 1.2rem !important;
}

/* ── Streamlit alert boxes ── */
div[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    font-size: 0.91rem !important;
    padding: 0.9rem 1.1rem !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1.5px solid var(--border-light) !important;
    margin: 1.8rem 0 !important;
}

/* ── Caption ── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    line-height: 1.6 !important;
}

/* ── Tooltip/helper text in forms ── */
small, .stTextInput .instructions {
    color: var(--text-light) !important;
    font-size: 0.78rem !important;
}

/* ── Mobile responsive ── */
@media (max-width: 768px) {
    .block-container {
        padding: 0.25rem 0.65rem 3rem 0.65rem !important;
    }

    h1 { font-size: 1.55rem !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.1rem !important; }

    div[data-testid="stSelectbox"] > div > div {
        min-height: 44px !important;
    }

    button[kind="primary"],
    .stButton > button[kind="primary"] {
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        min-height: 48px !important;
    }

    div[data-testid="stRadio"] label {
        padding: 0.35rem 0.8rem !important;
        font-size: 0.87rem !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================================
# UI Text Translations (T dictionary)
# =====================================================================
T = {
    # Landing page
    "hero_title": ("Field Shift", "ಫೀಲ್ಡ್ ಶಿಫ್ಟ್"),
    "hero_subtitle": (
        "Smart crop rotation suggestions based on your soil, season, and NASA satellite weather data.",
        "ನಿಮ್ಮ ಮಣ್ಣು, ಋತು ಮತ್ತು ನಾಸಾ ಉಪಗ್ರಹ ಹವಾಮಾನ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಸೂಕ್ತ ಬೆಳೆ ಸರದಿ ಸಲಹೆಗಳು.",
    ),
    "how_title": ("How it works", "ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ"),
    "how_1": (
        "Tell us your location, soil type, and current season",
        "ನಿಮ್ಮ ತಾಲೂಕು, ಮಣ್ಣಿನ ಪ್ರಕಾರ ಮತ್ತು ಋತುವನ್ನು ತಿಳಿಸಿ",
    ),
    "how_2": (
        "Share what you grew last so we can protect your soil",
        "ಮಣ್ಣಿನ ರಕ್ಷಣೆಗಾಗಿ ಈ ಹಿಂದೆ ಬೆಳೆದ ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    ),
    "how_3": (
        "Get 3 scored alternatives ranked for your field's conditions",
        "ನಿಮ್ಮ ಜಮೀನಿನ ಸ್ಥಿತಿಗೆ ಸೂಕ್ತವಾದ 3 ಪರ್ಯಾಯ ಬೆಳೆಗಳ ಅಂಕಗಳನ್ನು ಪಡೆಯಿರಿ",
    ),
    "benefits_title": ("Benefits for farmers", "ರೈತರಿಗೆ ಪ್ರಯೋಜನಗಳು"),
    "ben_1": (
        "Break pest and disease cycles naturally",
        "ಕೀಟ ಮತ್ತು ರೋಗ ಬಾಧೆಯನ್ನು ನೈಸರ್ಗಿಕವಾಗಿ ನಿಯಂತ್ರಿಸಿ",
    ),
    "ben_2": (
        "Replenish soil nitrogen with legume rotations",
        "ದ್ವಿದಳ ಧಾನ್ಯಗಳ ಸರದಿಯಿಂದ ಮಣ್ಣಿನ ಸಾರಜನಕ ಹೆಚ್ಚಿಸಿ",
    ),
    "ben_3": (
        "Match crop water demand to seasonal rainfall patterns",
        "ಮಳೆಗಾಲದ ಲಭ್ಯ ನೀರಿಗೆ ತಕ್ಕಂತೆ ಸೂಕ್ತ ಬೆಳೆಗಳನ್ನು ಆರಿಸಿ",
    ),
    "ben_4": (
        "Compare trade-offs between income stability and resource conservation",
        "ಆದಾಯ ಭದ್ರತೆ ಮತ್ತು ಸಂಪನ್ಮೂಲ ಸಂರಕ್ಷಣೆಯ ನಡುವಿನ ಸಮತೋಲನ ಪರಿಶೀಲಿಸಿ",
    ),
    "nasa_title": ("Powered by NASA satellite data", "ನಾಸಾ ಮಾಹಿತಿಯಿಂದ ಚಾಲಿತ"),
    "nasa_desc": (
        "Uses 30-year historical climate patterns from NASA POWER satellite observations "
        "(rainfall volume, dry spell risks, and monsoon intensity) calibrated for Belagavi district.",
        "ಬೆಳಗಾವಿ ಜಿಲ್ಲೆಗೆ ಅನ್ವಯಿಸಲಾದ ನಾಸಾ POWER ಉಪಗ್ರಹದ 30 ವರ್ಷಗಳ ಹವಾಮಾನ ಅಧ್ಯಯನ "
        "(ಮಳೆ ಪ್ರಮಾಣ, ಒಣ ಹವೆಯ ದಿನಗಳು ಮತ್ತು ಮುಂಗಾರಿನ ತೀವ್ರತೆ) ಆಧಾರಿತವಾಗಿದೆ.",
    ),
    "start_btn": ("Start Recommendation", "ಶಿಫಾರಸು ಪ್ರಾರಂಭಿಸಿ"),
    # Form labels
    "details": ("Your details", "ನಿಮ್ಮ ವಿವರಗಳು"),
    "taluk": ("Taluk (Belagavi district)", "ತಾಲೂಕು (ಬೆಳಗಾವಿ ಜಿಲ್ಲೆ)"),
    "soil": ("Soil type", "ಮಣ್ಣಿನ ಪ್ರಕಾರ"),
    "season": ("Season you are planning for", "ಯಾವ ಋತುವಿಗಾಗಿ ಯೋಜನೆ?"),
    "last": ("Crop you just harvested", "ಈಗಷ್ಟೇ ಕೊಯ್ಲು ಮಾಡಿದ ಬೆಳೆ"),
    "prev": (
        "Crop before that (optional, helps check 3-crop patterns)",
        "ಅದಕ್ಕಿಂತ ಹಿಂದಿನ ಬೆಳೆ (ಐಚ್ಛಿಕ, 3-ಬೆಳೆ ಸರದಿ ಪರಿಶೀಲನೆಗಾಗಿ)",
    ),
    "irrigation": ("Do you have irrigation?", "ನೀರಾವರಿ ಇದೆಯೇ?"),
    "irr_no": (
        "I do not (rainfed only)",
        "ಇಲ್ಲ (ಕೇವಲ ಮಳೆ ಆಶ್ರಿತ)",
    ),
    "irr_yes": (
        "I have irrigation (borewell, canal, etc.)",
        "ಹೌದು, ನೀರಾವರಿ ಇದೆ (ಬೋರ್‌ವೆಲ್, ಕಾಲುವೆ, ಇತ್ಯಾದಿ)",
    ),
    "priority": ("What matters most this season?", "ಈ ಋತುವಿನಲ್ಲಿ ನಿಮ್ಮ ಮುಖ್ಯ ಆದ್ಯತೆ ಏನು?"),
    "usual": (
        "Your usual next crop (optional)",
        "ನೀವು ಸಾಮಾನ್ಯವಾಗಿ ಬೆಳೆಯುವ ಬೆಳೆ (ಐಚ್ಛಿಕ)",
    ),
    "usual_help": (
        "If you already have a crop in mind, select it here. Field Shift will show your choice alongside two alternatives.",
        "ನಿಮ್ಮ ಮನಸ್ಸಿನಲ್ಲಿ ಈಗಾಗಲೇ ಒಂದು ಬೆಳೆ ಇದ್ದರೆ, ಅದನ್ನು ಇಲ್ಲಿ ಆಯ್ಕೆಮಾಡಿ. ಫೀಲ್ಡ್ ಶಿಫ್ಟ್ ನಿಮ್ಮ ಆಯ್ಕೆಯೊಂದಿಗೆ ಎರಡು ಪರ್ಯಾಯಗಳನ್ನು ತೋರಿಸುತ್ತದೆ.",
    ),
    "go": ("Get my suggestion", "ಸಲಹೆ ಪಡೆಯಿರಿ"),
    "back": ("← Change inputs", "← ವಿವರ ಬದಲಾಯಿಸಿ"),
    # Form section headers
    "form_location": ("Location & Soil", "ಸ್ಥಳ ಮತ್ತು ಮಣ್ಣು"),
    "form_season_crop": ("Season & Comparison", "ಋತು ಮತ್ತು ಹೋಲಿಕೆ"),
    "form_crop_history": ("Crop History", "ಬೆಳೆ ಇತಿಹಾಸ"),
    "form_preferences": ("Your Preferences", "ನಿಮ್ಮ ಆದ್ಯತೆಗಳು"),
    # Results
    "results_title": ("Your Recommendations", "ನಿಮ್ಮ ಶಿಫಾರಸುಗಳು"),
    "for_conditions": ("For conditions:", "ಈ ಸ್ಥಿತಿಗೆ:"),
    "warning": ("Warning", "ಎಚ್ಚರಿಕೆ"),
    "top_choice": ("Top choice", "ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆ"),
    "equal": ("Equal choice", "ಸಮಾನ ಆಯ್ಕೆ"),
    "place": ("Place", "ಸ್ಥಾನ"),
    "rotation": ("Rotation fit", "ಬೆಳೆ ಸರದಿ ಹೊಂದಾಣಿಕೆ"),
    "soilw": ("Soil fit", "ಮಣ್ಣಿನ ಹೊಂದಾಣಿಕೆ"),
    "climate": ("Climate fit", "ಹವಾಮಾನ ಹೊಂದಾಣಿಕೆ"),
    "water": ("Water use", "ನೀರಿನ ಬಳಕೆ"),
    "nasa_insight": ("NASA Climate Insight", "ನಾಸಾ ಹವಾಮಾನ ಮಾಹಿತಿ"),
    "strategies_title": ("Compare 3 strategies", "3 ತಂತ್ರಗಳನ್ನು ಹೋಲಿಸಿ"),
    "strategies_note": ("", ""),
    "strat_usual": ("Your usual choice", "ನಿಮ್ಮ ಸಾಮಾನ್ಯ ಆಯ್ಕೆ"),
    "strat_alt1": ("Alternative 1", "ಪರ್ಯಾಯ 1"),
    "strat_alt2": ("Alternative 2", "ಪರ್ಯಾಯ 2"),
    "strat_alt3": ("Alternative 3", "ಪರ್ಯಾಯ 3"),
    "why_suggested": ("Why suggested", "ಏಕೆ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ"),
    "evidence": ("Evidence", "ಸಾಕ್ಷ್ಯ"),
    "benefits": ("Benefits", "ಪ್ರಯೋಜನಗಳು"),
    "info_gaps": ("Information gaps", "ಮಾಹಿತಿ ಕೊರತೆಗಳು"),
    "risks": ("Risks to watch", "ಗಮನಿಸಬೇಕಾದ ಅಪಾಯಗಳು"),
    "assumption_title": (
        "If our water assumption is wrong",
        "ನಮ್ಮ ನೀರಿನ ಊಹೆ ತಪ್ಪಾಗಿದ್ದರೆ",
    ),
    "disclaimer_text": (
        "Field Shift is a decision-support prototype built for the NASA Space Apps Challenge. "
        "Recommendations combine agronomic rotation logic with NASA satellite climate data. "
        "Always confirm with your local Raitha Samparka Kendra or agriculture officer before purchasing seeds.",
        "ಫೀಲ್ಡ್ ಶಿಫ್ಟ್ ಎಂಬುದು ನಾಸಾ ಸ್ಪೇಸ್ ಆಪ್ಸ್ ಚಾಲೆಂಜ್‌ಗಾಗಿ ರೂಪಿಸಲಾದ ಒಂದು ಮಾದರಿ ತಂತ್ರಾಂಶವಾಗಿದೆ. "
        "ಶಿಫಾರಸುಗಳು ಕೃಷಿ ವಿಜ್ಞಾನದ ತತ್ವಗಳು ಮತ್ತು ನಾಸಾ ಉಪಗ್ರಹ ಹವಾಮಾನ ಮಾಹಿತಿಯನ್ನು ಆಧರಿಸಿವೆ. "
        "ಬೀಜ ಖರೀದಿಸುವ ಮುನ್ನ ಯಾವಾಗಲೂ ನಿಮ್ಮ ಸ್ಥಳೀಯ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರ ಅಥವಾ ಕೃಷಿ ಅಧಿಕಾರಿಯೊಂದಿಗೆ ಸಮಾಲೋಚಿಸಿ.",
    ),
    "back_to_top": ("New recommendation", "ಹೊಸ ಶಿಫಾರಸು"),
}


# =====================================================================
# Helper Functions
# =====================================================================
def clean_html(html_str):
    """Strip HTML comments and leading indentation so markdown never parses HTML as code blocks."""
    cleaned = re.sub(r"<!--.*?-->", "", html_str, flags=re.DOTALL)
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines)


def score_bar_html(score, max_score, label, detail):
    """Render a horizontal score bar as HTML."""
    pct = int((score / max_score) * 100) if max_score > 0 else 0
    # Color based on percentage
    if pct >= 75:
        bar_color = "#2A5C2A"
        bar_bg = "rgba(42,92,42,0.12)"
        score_color = "#2A5C2A"
    elif pct >= 50:
        bar_color = "#6B8F5E"
        bar_bg = "rgba(107,143,94,0.14)"
        score_color = "#4A6E3D"
    elif pct >= 25:
        bar_color = "#C49A00"
        bar_bg = "rgba(196,154,0,0.14)"
        score_color = "#8A6A00"
    else:
        bar_color = "#C05621"
        bar_bg = "rgba(192,86,33,0.14)"
        score_color = "#C05621"

    return clean_html(f"""
<div style="margin-bottom: 0.65rem;">
<div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 3px;">
<span style="font-size: 0.83rem; font-weight: 600; color: #182818; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">{label}</span>
<span style="font-size: 0.82rem; color: {score_color}; font-weight: 700; font-family: 'Inter', sans-serif; background: {bar_bg}; padding: 1px 7px; border-radius: 20px; white-space: nowrap;">{score}/{max_score}</span>
</div>
<div style="background: #EAF0E5; border-radius: 100px; height: 7px; overflow: hidden; margin-bottom: 5px;">
<div style="width: {pct}%; height: 100%; background: linear-gradient(90deg, {bar_color}CC, {bar_color}); border-radius: 100px;"></div>
</div>
<div style="font-size: 0.77rem; color: #62786A; line-height: 1.45; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; padding-left: 2px;">{detail}</div>
</div>
""")


def crop_card_html(x, is_top, rank_num, t_fn, lang):
    """Render a recommendation card for a crop."""
    crop_name = x["name_kn"] if lang == "kn" else sc.crop_word(lang, x["crop"])
    total = x["total"]
    max_total = x["max_total"]

    # Visual hierarchy: top crop vs runners-up
    if is_top and not x["tied"]:
        badge_text = t_fn("top_choice")
        badge_bg = "linear-gradient(135deg, #1B3D1B, #2A5C2A)"
        badge_fg = "#FFFFFF"
        border_color = "#2A5C2A"
        card_accent = "linear-gradient(180deg, rgba(235,243,230,0.4) 0%, rgba(255,255,255,0) 100%)"
        ring_color = "#2A5C2A"
        ring_track = "#EBF3E6"
    elif x["tied"]:
        badge_text = t_fn("equal")
        badge_bg = "#6B8F5E"
        badge_fg = "#FFFFFF"
        border_color = "#6B8F5E"
        card_accent = "linear-gradient(180deg, rgba(245,249,243,0.35) 0%, rgba(255,255,255,0) 100%)"
        ring_color = "#4A6E3D"
        ring_track = "#F0F6EC"
    else:
        badge_text = f"{t_fn('place')} {rank_num}"
        badge_bg = "#9BBD8D"
        badge_fg = "#182818"
        border_color = "#9BBD8D"
        card_accent = "none"
        ring_color = "#6B8F5E"
        ring_track = "#F5F8F3"

    pct = int((total / max_total) * 100) if max_total > 0 else 0
    if pct >= 80:
        ring_color = "#2A5C2A"
        ring_track = "rgba(42,92,42,0.12)"
    elif pct >= 65:
        ring_color = "#4A6E3D"
        ring_track = "rgba(74,110,61,0.12)"
    else:
        ring_color = "#6B8F5E"
        ring_track = "rgba(107,143,94,0.12)"

    if x["tied"]:
        badge_bg = "linear-gradient(135deg, #B8880A, #D4A017)"
        badge_fg = "#FFFFFF"
        border_color = "#D4A017"
        ring_color = "#B8880A"
        ring_track = "rgba(184,136,10,0.12)"

    left_border = f"border-left: 5px solid {border_color};" if is_top else f"border-left: 3px solid {border_color};"
    top_shadow = "0 6px 20px rgba(0,0,0,0.10), 0 2px 6px rgba(0,0,0,0.06)" if is_top else "0 2px 8px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.04)"

    parts = x["parts"]
    rot = parts["rotation"]
    soil = parts["soil"]
    clim = parts["climate"]
    wat = parts["water_use"]

    bars_html = ""
    bars_html += score_bar_html(rot[0], sc.MAX_PART_POINTS["rotation"], t_fn("rotation"), rot[1])
    bars_html += score_bar_html(soil[0], sc.MAX_PART_POINTS["soil"], t_fn("soilw"), soil[1])
    bars_html += score_bar_html(clim[0], sc.MAX_PART_POINTS["climate"], t_fn("climate"), clim[1])
    bars_html += score_bar_html(wat[0], sc.MAX_PART_POINTS["water_use"], t_fn("water"), wat[1])

    card_html = clean_html(f"""
<div style="background: #FFFFFF; background-image: {card_accent}; border-radius: 16px; {left_border} box-shadow: {top_shadow}; padding: 1.3rem 1.2rem 1.1rem 1.2rem; margin-bottom: 1rem; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; transition: box-shadow 0.22s ease;">
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
<div style="display: flex; align-items: center; gap: 0.65rem; flex-wrap: wrap; flex: 1; min-width: 0;">
<span style="background: {badge_bg}; color: {badge_fg}; font-size: 0.72rem; font-weight: 700; padding: 0.28rem 0.75rem; border-radius: 100px; letter-spacing: 0.04em; text-transform: uppercase; white-space: nowrap; flex-shrink: 0;">{badge_text}</span>
<span style="font-size: 1.18rem; font-weight: 700; color: #182818; line-height: 1.25; word-break: break-word;">{crop_name}</span>
</div>
<div style="text-align: center; flex-shrink: 0;">
<div style="width: 56px; height: 56px; border-radius: 50%; border: 3.5px solid {ring_color}; background: {ring_track}; display: flex; align-items: center; justify-content: center; flex-direction: column;">
<span style="font-size: 1.0rem; font-weight: 800; color: {ring_color}; line-height: 1; font-family: 'Inter', sans-serif;">{total}</span>
<span style="font-size: 0.52rem; color: #62786A; line-height: 1; font-family: 'Inter', sans-serif; letter-spacing: 0.01em;">/{max_total}</span>
</div>
</div>
</div>
<div style="height: 1px; background: linear-gradient(90deg, {border_color}30, transparent); margin-bottom: 1rem; border-radius: 1px;"></div>
{bars_html}
</div>
""")
    return card_html


# =====================================================================
# SECTION: Hero / Landing
# =====================================================================
def render_hero(t_fn, lang):
    """Render the landing hero section."""
    # Top brand bar
    st.markdown(clean_html(f"""
    <div class="dark-header-card" style="
        background: linear-gradient(145deg, #1B3D1B 0%, #2A5C2A 45%, #3A6E3A 80%, #2A5C2A 100%);
        border-radius: 20px;
        padding: 2.4rem 1.8rem 2rem 1.8rem;
        margin-bottom: 1.4rem;
        text-align: center;
        box-shadow: 0 8px 28px rgba(27,61,27,0.28), 0 2px 8px rgba(0,0,0,0.12);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 30% 20%, rgba(155,189,141,0.15) 0%, transparent 60%); pointer-events: none;"></div>
        <div style="font-size: 0.75rem; letter-spacing: 2.5px; color: #FFFFFF !important; text-transform: uppercase; margin-bottom: 0.6rem; font-family: 'Inter', sans-serif; font-weight: 700; opacity: 0.95;">
            NASA Space Apps Challenge
        </div>
        <h1 style="color: #FFFFFF !important; font-size: 2.1rem; font-weight: 800; margin: 0 0 0.6rem 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.15; letter-spacing: -0.02em;">
            {"ಫೀಲ್ಡ್ ಶಿಫ್ಟ್" if lang == "kn" else "Field Shift"}
        </h1>
        <p style="color: #FFFFFF !important; font-size: 0.95rem; margin: 0; line-height: 1.6; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; max-width: 420px; margin: 0 auto; opacity: 0.95;">
            {t_fn("hero_subtitle")}
        </p>
    </div>
    """), unsafe_allow_html=True)

    # How it works
    st.markdown(clean_html(f"""
    <div style="
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.4rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        border: 1.5px solid #DDE8D7;
    ">
        <h3 style="color: #2A5C2A !important; font-size: 1.0rem; font-weight: 700; margin: 0 0 1.1rem 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; letter-spacing: -0.01em; display: flex; align-items: center; gap: 0.5rem;">
            <span style="display: inline-block; width: 4px; height: 1.1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></span>
            {t_fn("how_title")}
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.85rem;">
            <div style="display: flex; align-items: flex-start; gap: 0.9rem;">
                <div style="min-width: 34px; height: 34px; background: linear-gradient(135deg, #2A5C2A, #3A6E3A); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #FFFFFF; font-size: 0.82rem; flex-shrink: 0; box-shadow: 0 2px 6px rgba(42,92,42,0.3);">1</div>
                <span style="font-size: 0.93rem; color: #182818; padding-top: 6px; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.4;">{t_fn("how_1")}</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.9rem;">
                <div style="min-width: 34px; height: 34px; background: linear-gradient(135deg, #2A5C2A, #3A6E3A); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #FFFFFF; font-size: 0.82rem; flex-shrink: 0; box-shadow: 0 2px 6px rgba(42,92,42,0.3);">2</div>
                <span style="font-size: 0.93rem; color: #182818; padding-top: 6px; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.4;">{t_fn("how_2")}</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.9rem;">
                <div style="min-width: 34px; height: 34px; background: linear-gradient(135deg, #2A5C2A, #3A6E3A); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #FFFFFF; font-size: 0.82rem; flex-shrink: 0; box-shadow: 0 2px 6px rgba(42,92,42,0.3);">3</div>
                <span style="font-size: 0.93rem; color: #182818; padding-top: 6px; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.4;">{t_fn("how_3")}</span>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Benefits for farmers
    st.markdown(clean_html(f"""
    <div style="
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.4rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        border: 1.5px solid #DDE8D7;
    ">
        <h3 style="color: #2A5C2A !important; font-size: 1.0rem; font-weight: 700; margin: 0 0 1.1rem 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; letter-spacing: -0.01em; display: flex; align-items: center; gap: 0.5rem;">
            <span style="display: inline-block; width: 4px; height: 1.1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></span>
            {t_fn("benefits_title")}
        </h3>
        <div style="display: flex; flex-direction: column; gap: 0.72rem;">
            <div style="display: flex; align-items: flex-start; gap: 0.8rem;">
                <div style="min-width: 22px; height: 22px; background: #EBF3E6; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <div style="width: 8px; height: 8px; background: #6B8F5E; border-radius: 50%;"></div>
                </div>
                <span style="font-size: 0.91rem; color: #182818; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.45;">{t_fn("ben_1")}</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.8rem;">
                <div style="min-width: 22px; height: 22px; background: #EBF3E6; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <div style="width: 8px; height: 8px; background: #6B8F5E; border-radius: 50%;"></div>
                </div>
                <span style="font-size: 0.91rem; color: #182818; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.45;">{t_fn("ben_2")}</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.8rem;">
                <div style="min-width: 22px; height: 22px; background: #EBF3E6; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <div style="width: 8px; height: 8px; background: #6B8F5E; border-radius: 50%;"></div>
                </div>
                <span style="font-size: 0.91rem; color: #182818; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.45;">{t_fn("ben_3")}</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.8rem;">
                <div style="min-width: 22px; height: 22px; background: #EBF3E6; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <div style="width: 8px; height: 8px; background: #6B8F5E; border-radius: 50%;"></div>
                </div>
                <span style="font-size: 0.91rem; color: #182818; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.45;">{t_fn("ben_4")}</span>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # NASA data section
    st.markdown(clean_html(f"""
    <div style="
        background: linear-gradient(135deg, #EBF3E6 0%, #F2F7EE 100%);
        border-radius: 16px;
        padding: 1.4rem 1.3rem;
        margin-bottom: 1.4rem;
        border: 1.5px solid #C8DFBC;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    ">
        <h3 style="color: #2A5C2A !important; font-size: 1.0rem; font-weight: 700; margin: 0 0 0.75rem 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; letter-spacing: -0.01em; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.1rem;">🛰️</span>
            {t_fn("nasa_title")}
        </h3>
        <p style="font-size: 0.87rem; color: #3D5240; margin: 0; line-height: 1.65; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">
            {t_fn("nasa_desc")}
        </p>
    </div>
    """), unsafe_allow_html=True)


# =====================================================================
# SECTION: Input Form
# =====================================================================
def render_form(lang, i, t_fn):
    """Render the farmer input form and return the inputs + submitted flag."""
    # Section header card
    st.markdown(clean_html(f"""
    <div class="dark-header-card" style="
        background: linear-gradient(135deg, #2A5C2A 0%, #1B3D1B 100%);
        border-radius: 16px 16px 0 0;
        padding: 1.2rem 1.4rem 1rem 1.4rem;
        box-shadow: 0 2px 8px rgba(42,92,42,0.15);
    ">
        <h2 style="color: #FFFFFF !important; font-size: 1.15rem; font-weight: 700; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; letter-spacing: -0.01em;">
            {t_fn("details")}
        </h2>
        <p style="color: #FFFFFF !important; font-size: 0.85rem; margin: 0.3rem 0 0 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; opacity: 0.95;">
            {"Fill in your field details to get personalised crop suggestions." if lang == "en" else "ನಿಮ್ಮ ಹೊಲದ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ ಮತ್ತು ಅನುಕೂಲಕರ ಬೆಳೆ ಸಲಹೆ ಪಡೆಯಿರಿ."}
        </p>
    </div>
    <div style="background: #FFFFFF; border-left: 1.5px solid #DDE8D7; border-right: 1.5px solid #DDE8D7; padding: 1.2rem 0 0 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    </div>
    """), unsafe_allow_html=True)

    # ── Location & Soil ──
    st.markdown(f"""
    <div style="padding: 0 0 0 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.2rem 0 0.5rem 0;">
            <div style="width: 3px; height: 1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></div>
            <p style="font-size: 0.78rem; font-weight: 700; color: #245B32; text-transform: uppercase; letter-spacing: 1.2px; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">
                {t_fn("form_location")}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    v = st.session_state.get("lang_version", 0)

    taluk = st.selectbox(
        t_fn("taluk"),
        list(sc.TALUK_TO_ZONE),
        format_func=lambda x: x if lang == "en" else TALUK_KN[x],
        key=f"taluk_input_{v}",
    )
    soil = st.selectbox(
        t_fn("soil"),
        ["black", "red", "sandy"],
        index=0,
        format_func=lambda x: x if lang == "en" else SOIL_KN[x],
        key=f"soil_input_{v}",
    )

    # ── Season ──
    st.markdown(f"""
    <div style="padding: 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0 0.5rem 0;">
            <div style="width: 3px; height: 1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></div>
            <p style="font-size: 0.78rem; font-weight: 700; color: #245B32; text-transform: uppercase; letter-spacing: 1.2px; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">
                {t_fn("form_season_crop")}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    season = st.radio(
        t_fn("season"),
        ["kharif", "rabi"],
        horizontal=True,
        format_func=lambda x: SEASON[x][i],
        index=0,
        key=f"season_input_{v}",
    )

    # ── Crop History ──
    st.markdown(f"""
    <div style="padding: 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0 0.5rem 0;">
            <div style="width: 3px; height: 1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></div>
            <p style="font-size: 0.78rem; font-weight: 700; color: #245B32; text-transform: uppercase; letter-spacing: 1.2px; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">
                {t_fn("form_crop_history")}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    all_last = list(sc.crop_info) + list(sc.other_info)
    last_crop = st.selectbox(
        t_fn("last"),
        all_last,
        format_func=lambda c: sc.crop_word(lang, c),
        key=f"last_crop_input_{v}",
    )
    prev_label = "Crop before that" if lang == "en" else t_fn("prev")
    prev_crop = st.selectbox(
        prev_label,
        [None] + list(sc.crop_info),
        index=0,
        format_func=lambda c: "-" if c is None else sc.crop_word(lang, c),
        key=f"prev_crop_input_{v}",
    )

    # ── Preferences ──
    st.markdown(f"""
    <div style="padding: 0;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0 0.5rem 0;">
            <div style="width: 3px; height: 1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></div>
            <p style="font-size: 0.78rem; font-weight: 700; color: #245B32; text-transform: uppercase; letter-spacing: 1.2px; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">
                {t_fn("form_preferences")}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    irrigation_key = f"irrigation_input_{v}"

    irrigation = st.radio(
        t_fn("irrigation"),
        [True, False],
        index=1,
        format_func=lambda x: t_fn("irr_yes") if x else t_fn("irr_no"),
        key=irrigation_key,
    )

    priority = st.radio(
        t_fn("priority"),
        list(PRIORITY),
        format_func=lambda x: PRIORITY[x][i],
        key=f"priority_input_{v}",
    )

    # ── Strategy comparison: usual crop ──
    season_crops = [
        c for c, val in sc.crop_info.items() if val["season"] == season
    ]
    usual_crop = st.selectbox(
        t_fn("usual"),
        ["Select"] + season_crops,
        format_func=lambda c: "Select" if c == "Select" else sc.crop_word(lang, c),
        help=t_fn("usual_help"),
        key=f"usual_crop_input_{v}",
    )

    inputs = {
        "taluk": taluk,
        "soil": soil,
        "season": season,
        "last_crop": last_crop,
        "prev_crop": prev_crop,
        "irrigation": irrigation,
        "priority": priority,
        "usual": usual_crop if usual_crop != "Select" else None,
    }

    # Submit button
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    submitted = st.button(t_fn("go"), type="primary", use_container_width=True)

    return inputs, submitted


# =====================================================================
# SECTION: Recommendation Results
# =====================================================================
@st.cache_data(show_spinner=False)
def _compute_results(zone, soil, season, last_crop, prev_crop, irrigation, priority, usual_choice, lang):
    kw = dict(
        zone=zone,
        soil=soil,
        season=season,
        last_crop=last_crop,
        prev_crop=prev_crop,
        irrigation=irrigation,
        priority=priority,
    )
    r = sc.recommend_with_ties(lang=lang, **kw)
    cs = sc.compare_strategies(usual_choice, lang=lang, **kw)
    ac = sc.assumption_check(**kw)
    return r, cs, ac


def render_results(inputs, lang, i, t_fn):
    """Render recommendation results."""
    season_crops = [c for c, val in sc.crop_info.items() if val["season"] == inputs["season"]]
    usual_choice = inputs["usual"] if inputs.get("usual") in season_crops else None
    try:
        zone = sc.zone_for(inputs["taluk"])
        r, cs, ac = _compute_results(
            zone=zone,
            soil=inputs["soil"],
            season=inputs["season"],
            last_crop=inputs["last_crop"],
            prev_crop=inputs["prev_crop"],
            irrigation=inputs["irrigation"],
            priority=inputs["priority"],
            usual_choice=usual_choice,
            lang=lang,
        )
    except ValueError:
        st.warning(f"⚠ {t_fn('warning')}")
        return

    # Results header
    st.markdown(clean_html(f"""
    <div class="dark-header-card" style="
        background: linear-gradient(145deg, #1B3D1B 0%, #2A5C2A 50%, #3A6E3A 100%);
        border-radius: 16px;
        padding: 1.4rem 1.4rem;
        margin: 1.4rem 0 1.1rem 0;
        text-align: center;
        box-shadow: 0 6px 20px rgba(27,61,27,0.25), 0 2px 6px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 70% 30%, rgba(155,189,141,0.12) 0%, transparent 60%); pointer-events: none;"></div>
        <div style="font-size: 0.72rem; letter-spacing: 2px; color: #FFFFFF !important; text-transform: uppercase; margin-bottom: 0.4rem; font-family: 'Inter', sans-serif; font-weight: 700; opacity: 0.95;">✓ {"Analysis complete" if lang == "en" else "ವಿಶ್ಲೇಷಣೆ ಪೂರ್ಣ"}</div>
        <h2 style="color: #FFFFFF !important; font-size: 1.25rem; font-weight: 800; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; letter-spacing: -0.01em;">
            {t_fn("results_title")}
        </h2>
    </div>
    """), unsafe_allow_html=True)

    # Condition chips
    zone_label = f"Belagavi Zone ({zone})" if lang == "en" else f"ಬೆಳಗಾವಿ ವಲಯ ({zone})"
    soil_display = SOIL_KN[inputs["soil"]] if lang == "kn" else inputs["soil"].capitalize()
    season_display = SEASON[inputs["season"]][i]
    irr_display = "Irrigated" if inputs["irrigation"] else "Rainfed"
    if lang == "kn":
        irr_display = "ನೀರಾವರಿ" if inputs["irrigation"] else "ಮಳೆ ಆಶ್ರಿತ"
    last_crop_display = sc.crop_word(lang, inputs["last_crop"])

    st.markdown(clean_html(f"""
    <div style="
        background: #FFFFFF;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 1.1rem;
        border: 1.5px solid #DDE8D7;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        align-items: center;
    ">
        <span style="font-size: 0.75rem; color: #62786A; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 0.2rem;">{t_fn("for_conditions")}</span>
        <span style="background: #EBF3E6; color: #2A5C2A; font-size: 0.8rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 100px;">📍 {inputs["taluk"]} · {zone_label}</span>
        <span style="background: #EBF3E6; color: #2A5C2A; font-size: 0.8rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 100px;">🌱 {soil_display}</span>
        <span style="background: #EBF3E6; color: #2A5C2A; font-size: 0.8rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 100px;">🗓️ {season_display}</span>
        <span style="background: #EBF3E6; color: #2A5C2A; font-size: 0.8rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 100px;">💧 {irr_display}</span>
        <span style="background: #EBF3E6; color: #2A5C2A; font-size: 0.8rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 100px;">🌾 Previous: {last_crop_display}</span>
    </div>
    """), unsafe_allow_html=True)

    # Warnings
    for w in r["warnings"]:
        st.markdown(clean_html(f"""
        <div style="
            background: #FFFBEE;
            border-left: 4px solid #C49A00;
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.65rem;
            font-size: 0.88rem;
            color: #6B4F00;
            font-family: 'Inter', 'Noto Sans Kannada', sans-serif;
            line-height: 1.55;
            box-shadow: 0 1px 4px rgba(196,154,0,0.10);
        ">
            <strong style="color: #8A6300;">⚠ {t_fn("warning")}:</strong> {w}
        </div>
        """), unsafe_allow_html=True)

    # Crop cards
    for idx, x in enumerate(r["ranked"]):
        card_html = crop_card_html(x, idx == 0, idx + 1, t_fn, lang)
        st.markdown(card_html, unsafe_allow_html=True)

    # NASA Climate Fact Box
    nasa_fact_text = ZONE_FACTS[zone][i]
    st.markdown(clean_html(f"""
    <div style="
        background: linear-gradient(135deg, #EBF3E6 0%, #F5F9F2 100%);
        border-radius: 12px;
        padding: 0.95rem 1.1rem;
        margin: 1.1rem 0;
        border: 1.5px solid #C8DFBC;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        font-size: 0.86rem;
        color: #2A5C2A;
        font-family: 'Inter', 'Noto Sans Kannada', sans-serif;
        line-height: 1.55;
    ">
        <strong style="color: #1B3D1B;">🛰️ {t_fn("nasa_insight")} ({inputs["taluk"]} · {zone}):</strong><br/>
        {nasa_fact_text}
    </div>
    """), unsafe_allow_html=True)

    # ── Compare 3 strategies ──
    strat_note = t_fn("strategies_note")
    note_html = f' <span style="font-size: 0.78rem; color: #526E59; font-weight: 500; margin-left: 0.3rem;">{strat_note}</span>' if strat_note else ""
    st.markdown(clean_html(f"""
    <div style="
        background: #FFFFFF;
        border-radius: 16px 16px 0 0;
        padding: 1.1rem 1.3rem 0.6rem 1.3rem;
        margin-top: 1.4rem;
        border-bottom: 2px solid #DDE8D7;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    ">
        <h3 style="color: #2A5C2A !important; font-size: 1.0rem; font-weight: 700; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; letter-spacing: -0.01em; display: flex; align-items: center; gap: 0.5rem;">
            <span style="display: inline-block; width: 4px; height: 1.0rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></span>
            {t_fn("strategies_title")}{note_html}
        </h3>
    </div>
    """), unsafe_allow_html=True)

    if cs:
        strategy_icons = {
            "usual": "🌾",
            "alt_1": "🌱",
            "alt_2": "🌿",
            "alt_3": "🌿",
            "Your usual choice": "🌾",
            "Alternative 1": "🌱",
            "Alternative 2": "🌿",
            "Alternative 3": "🌿",
        }
        for s in cs["strategies"]:
            tag = f" — {t_fn('equal')}" if s["tied_with_another"] else ""
            st_icon = strategy_icons.get(s.get("key"), strategy_icons.get(s.get("label"), "🌱"))
            crop_disp = s["name_kn"] if lang == "kn" else sc.crop_word(lang, s["crop"])
            with st.expander(
                f"{s.get('label_text', s['label'])}: {crop_disp} ({s['total']}/{s['max_total']}){tag}",
                icon=st_icon,
            ):
                # Why suggested
                st.markdown(f"**{t_fn('why_suggested')}**")
                for a in s["why"]:
                    st.markdown(f"- {a}")

                # Evidence
                st.markdown(
                    f"**{t_fn('evidence')}**: {s['evidence']} ({s['evidence_strength']})"
                )

                # Benefits
                st.markdown(f"**{t_fn('benefits')}**")
                for a in s["benefits"]:
                    st.markdown(f"- {a}")

                # Information gaps
                st.markdown(f"**{t_fn('info_gaps')}**")
                for a in s["gaps"]:
                    st.markdown(f"- {a}")

                # Risks
                st.markdown(f"**{t_fn('risks')}**")
                for a in s["risks"]:
                    st.markdown(f"- {a}")

    # ── Assumption / stability check ──
    st.markdown(f"""
    <div style="margin-top: 1.2rem; margin-bottom: 0.4rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 3px; height: 1rem; background: #2A5C2A; border-radius: 2px; flex-shrink: 0;"></div>
            <p style="font-size: 0.78rem; font-weight: 700; color: #245B32; text-transform: uppercase; letter-spacing: 1.2px; margin: 0; font-family: 'Inter', 'Noto Sans Kannada', sans-serif;">
                {t_fn("assumption_title")}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if ac:
        if lang == "kn":
            ac_msg = (
                "ದೃಢಪಡಿಸದ ನೀರಿನ ಅವಶ್ಯಕತೆಗಳು ತಪ್ಪಾಗಿದ್ದರೂ ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆಯು ಬದಲಾಗುವುದಿಲ್ಲ."
                if ac["status"] == "stable"
                else "ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆಯು ಯಾವುದೇ ತಜ್ಞರು ದೃಢಪಡಿಸದ ನೀರಿನ ಅವಶ್ಯಕತೆಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿದೆ. ದಯವಿಟ್ಟು ಸ್ಥಳೀಯ ತಜ್ಞರನ್ನು ಕೇಳಿ."
            )
        else:
            ac_msg = ac["message"]

        if ac["status"] == "stable":
            st.markdown(clean_html(f"""
            <div style="
                background: #EBF5EC;
                border-left: 4px solid #3D9A42;
                border-radius: 10px;
                padding: 0.85rem 1.1rem;
                margin-bottom: 1rem;
                font-size: 0.88rem;
                color: #1B4D20;
                font-family: 'Inter', 'Noto Sans Kannada', sans-serif;
                line-height: 1.55;
            ">
                <strong>✓</strong> {ac_msg}
            </div>
            """), unsafe_allow_html=True)
        else:
            st.markdown(clean_html(f"""
            <div style="
                background: #FFFBEE;
                border-left: 4px solid #D4A017;
                border-radius: 10px;
                padding: 0.85rem 1.1rem;
                margin-bottom: 1rem;
                font-size: 0.88rem;
                color: #6B4F00;
                font-family: 'Inter', 'Noto Sans Kannada', sans-serif;
                line-height: 1.55;
            ">
                <strong>⚠</strong> {ac_msg}
            </div>
            """), unsafe_allow_html=True)


# =====================================================================
# Main Application Flow
# =====================================================================
def main():
    # ── Language selector ──
    lang_param = st.query_params.get("lang", None)
    default_lang_idx = 1 if lang_param == "kn" else 0

    lang_choice = st.radio(
        "Language / ಭಾಷೆ",
        ["English", "ಕನ್ನಡ"],
        index=default_lang_idx,
        horizontal=True,
        label_visibility="collapsed",
    )
    lang = "kn" if lang_choice == "ಕನ್ನಡ" else "en"
    i = 1 if lang == "kn" else 0

    def t(key):
        return T[key][i]

    # Handle language switch cleanly
    if "current_lang" not in st.session_state:
        st.session_state["current_lang"] = lang
        st.session_state["lang_version"] = 0
    elif st.session_state["current_lang"] != lang:
        old_v = st.session_state.get("lang_version", 0)
        new_v = old_v + 1
        st.session_state["lang_version"] = new_v
        st.session_state["current_lang"] = lang
        # Copy input values across language versions
        for field in ["taluk", "soil", "season", "last_crop", "prev_crop", "irrigation", "priority", "usual_crop"]:
            old_key = f"{field}_input_{old_v}"
            new_key = f"{field}_input_{new_v}"
            if old_key in st.session_state:
                st.session_state[new_key] = st.session_state[old_key]
        st.rerun()

    # Track landing page vs form state
    if "started" not in st.session_state:
        st.session_state["started"] = False

    # ── View routing ──
    if not st.session_state["started"] and not st.session_state.get("go"):
        render_hero(t, lang)
        if st.button(t("start_btn"), type="primary", use_container_width=True):
            st.session_state["started"] = True
            st.rerun()
    else:
        inputs, submitted = render_form(lang, i, t)

        if submitted:
            st.session_state["go"] = True
            st.session_state["inputs"] = inputs

        if st.session_state.get("go") and "inputs" in st.session_state:
            render_results(st.session_state["inputs"], lang, i, t)

            # New recommendation button
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            if st.button(f"↺ {t('back_to_top')}", use_container_width=True):
                st.session_state["go"] = False
                st.session_state["started"] = True
                st.rerun()

    # ── Disclaimer Footer ──
    st.markdown(clean_html(f"""
    <div style="
        background: #FFFFFF;
        border: 1.5px solid #DDE8D7;
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        margin-top: 1.5rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 0.84rem; color: #4A6052; font-family: 'Inter', 'Noto Sans Kannada', sans-serif; line-height: 1.55;">
            <strong style="color: #3D5240;">ℹ Prototype Disclaimer:</strong><br/>
            {t("disclaimer_text")}
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Branding footer
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1rem 0 0.6rem 0;
        color: #526E59;
        font-size: 0.75rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.03em;
    ">
        Field Shift — NASA Space Apps Challenge
    </div>
    """, unsafe_allow_html=True)


main()