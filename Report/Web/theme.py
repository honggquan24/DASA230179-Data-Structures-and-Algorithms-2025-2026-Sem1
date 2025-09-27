from textwrap import dedent

THEME_DARKMODE = {
    "bg1":    "#0f0f23",
    "bg2":    "#1a1a2e",
    "bg3":    "#191b1f",
    "text":   "#E6F1FF",
    "muted":  "#8892b0",
    "accent": "#f6f6f6",
    "accent2":"#00d4ff",
    "gold":   "#ffd700",
    "panel_alpha": "0.05",  
    "blur_px": "10px", 
}

THEME_LIGHTMODE = {
    "bg1":    "#ffffff",      
    "bg2":    "#f5f7fa",      
    "bg3":    "#eef2f6",      
    "text":   "#1a1a1a",      
    "muted":  "#6b7280",      
    "accent": "#3b82f6",      
    "accent2":"#06b6d4",      
    "gold":   "#f59e0b",      
    "panel_alpha": "0.8",     
    "blur_px": "8px",         
}


def get_css(theme: dict) -> str:
    t = theme

    # Xác định nếu là light mode để điều chỉnh CSS
    is_light = t["bg1"] == "#ffffff" or t["text"] == "#1a1a1a"

    # Màu nền panel chính — trong light mode nên đậm hơn để text nổi
    panel_bg = "rgba(255,255,255, var(--panel-alpha))" if not is_light else "rgba(255,255,255, 0.85)"
    panel_border = "rgba(255,255,255, 0.1)" if not is_light else "rgba(0,0,0,0.08)"

    # Màu shadow cho main content — tối hơn trong light mode
    shadow_color = "rgba(0, 0, 0, 0.3)" if not is_light else "rgba(0, 0, 0, 0.08)"

    # Màu nền gradient cho chữ heading — giữ nguyên nhưng điều chỉnh shadow cho dễ đọc
    heading_shadow = (
        "0 0 30px color-mix(in oklab, var(--accent) 35%, transparent)" if not is_light
        else "0 2px 8px color-mix(in oklab, var(--accent) 25%, transparent)"
    )

    # Màu nền contact section
    contact_bg = (
        "color-mix(in oklab, var(--accent) 15%, transparent)" if not is_light
        else "color-mix(in oklab, var(--accent) 5%, white)"
    )
    contact_border = (
        "color-mix(in oklab, var(--accent) 40%, transparent)" if not is_light
        else "color-mix(in oklab, var(--accent) 20%, white)"
    )
    contact_shadow = (
        "0 4px 20px color-mix(in oklab, var(--accent) 12%, transparent)" if not is_light
        else "0 2px 8px color-mix(in oklab, var(--accent) 8%, transparent)"
    )

    # Social container background
    social_container_bg = (
        "rgba(255,255,255,0.05)" if not is_light else "rgba(0,0,0,0.03)"
    )
    social_container_border = (
        "rgba(255,255,255,0.1)" if not is_light else "rgba(0,0,0,0.08)"
    )

    # Gradient cho scrollbar thumb
    scrollbar_thumb_bg = (
        "linear-gradient(135deg, var(--accent), var(--accent2))" if not is_light
        else "linear-gradient(135deg, var(--accent), var(--accent2))"
    )
    scrollbar_track_bg = (
        "rgba(255,255,255,0.1)" if not is_light else "rgba(0,0,0,0.05)"
    )

    # Input và Button styling - đồng bộ với theme
    input_bg = "rgba(255,255,255,0.08)" if not is_light else "rgba(255,255,255,0.9)"
    input_border = "rgba(255,255,255,0.15)" if not is_light else "rgba(0,0,0,0.12)"
    input_focus_border = "var(--accent)" if not is_light else "var(--accent)"
    
    button_bg = "linear-gradient(135deg, var(--accent), var(--accent2))" if not is_light else "linear-gradient(135deg, var(--accent), var(--accent2))"
    button_text = "#ffffff" if not is_light else "#ffffff"
    button_shadow = "0 4px 15px color-mix(in oklab, var(--accent) 25%, transparent)" if not is_light else "0 2px 8px color-mix(in oklab, var(--accent) 20%, transparent)"

    return dedent(f"""
    <head>
        <link rel="stylesheet"
              href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
              rel="stylesheet">
    </head>

    <style>
    :root {{
        --bg1: {t["bg1"]};
        --bg2: {t["bg2"]};
        --bg3: {t["bg3"]};
        --text: {t["text"]};
        --muted: {t["muted"]};
        --accent: {t["accent"]};
        --accent2: {t["accent2"]};
        --gold: {t["gold"]};
        --panel-alpha: {t["panel_alpha"]};
        --blur: {t["blur_px"]};
    }}

    /* Global Styles */
    .stApp {{
        background: linear-gradient(135deg, var(--bg1) 0%, var(--bg2) 50%, var(--bg3) 100%);
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }}

    /* Animated background particles — Ẩn trong light mode để tránh rối mắt */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image:
            radial-gradient(2px 2px at 20px 30px, var(--accent), transparent),
            radial-gradient(2px 2px at 40px 70px, var(--accent2), transparent),
            radial-gradient(1px 1px at 90px 40px, var(--gold), transparent),
            radial-gradient(1px 1px at 130px 80px, #ff6b6b, transparent);
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: 0;
        {'display: none;' if is_light else ''}
    }}
    @keyframes sparkle {{
        0% {{ transform: translateY(0px) rotate(0deg); opacity: 0.7; }}
        50% {{ transform: translateY(-100px) rotate(180deg); opacity: 1; }}
        100% {{ transform: translateY(-200px) rotate(360deg); opacity: 0.7; }}
    }}

    /* Main content styling */
    .main-content {{
        position: relative; z-index: 1;
        backdrop-filter: blur(var(--blur));
        background: {panel_bg};
        border-radius: 20px;
        border: 1px solid {panel_border};
        padding: 2rem; margin: 1rem 0;
        box-shadow: 0 8px 32px {shadow_color};
    }}

    /* Profile section styling */
    .profile-section {{
        background: {'linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05))' if not is_light else 'linear-gradient(145deg, rgba(0,0,0,0.02), rgba(0,0,0,0.01))'};
        border-radius: 20px; padding: 2rem;
        border: 1px solid {panel_border};
        box-shadow: 0 8px 32px {shadow_color};
        backdrop-filter: blur(var(--blur));
        position: relative; overflow: hidden;
    }}
    .profile-section::before {{
        content: '';
        position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(transparent, color-mix(in oklab, var(--accent) 30%, transparent), transparent);
        animation: rotate 10s linear infinite; z-index: -1;
        {'opacity: 0.3;' if is_light else 'opacity: 0.7;'}
    }}
    @keyframes rotate {{ 0% {{transform: rotate(0deg);}} 100% {{transform: rotate(360deg);}} }}

    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {{
        background: linear-gradient(135deg, var(--accent), var(--accent2), var(--gold));
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-shadow: {heading_shadow};
    }}
    .main-title {{ font-size: 3.5rem !important; margin-bottom: .5rem !important; animation: glow 2s ease-in-out infinite alternate; }}
    .subtitle   {{ font-size: 1.8rem !important; color: var(--accent) !important; margin-bottom: 1rem !important; font-weight: 500 !important; }}
    @keyframes glow {{
        from {{ text-shadow: 0 0 20px color-mix(in oklab, var(--accent) 30%, transparent); }}
        to   {{ text-shadow: 0 0 30px color-mix(in oklab, var(--accent) 60%, transparent), 0 0 40px color-mix(in oklab, var(--accent) 30%, transparent); }}
    }}

    /* Description text styling */
    .description {{
        color: var(--muted);
        font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;
        padding: 1rem; border-left: 3px solid var(--accent);
        background: color-mix(in oklab, var(--accent) 10%, transparent);
        border-radius: 0 10px 10px 0;
    }}

    /* Contact section styling */
    .contact-section {{
        background: {contact_bg};
        border-radius: 15px; padding: 1.5rem; margin: 2rem 0;
        border: 1px solid {contact_border};
        box-shadow: {contact_shadow};
    }}
    .contact-item {{
        display: flex; align-items: center; margin: .8rem 0;
        color: var(--text); font-size: 1rem; transition: all .3s ease;
    }}
    .contact-item:hover {{ color: var(--accent); transform: translateX(10px); }}
    .contact-item i {{ margin-right: 10px; color: var(--accent); width: 20px; }}

    /* Social icons styling */
    .social-container {{
        background: {social_container_bg};
        border-radius: 15px; padding: 1.5rem; text-align: center;
        border: 1px solid {social_container_border}; margin-top: 2rem;
    }}
    .social-icons {{
        display: flex; justify-content: center; gap: 2rem; padding: 1rem 0;
    }}
    .social-icon {{
        display: inline-block; width: 60px; height: 60px; line-height: 60px; text-align: center;
        background: linear-gradient(145deg, color-mix(in oklab, var(--accent) 10%, transparent), color-mix(in oklab, var(--accent2) 10%, transparent));
        border-radius: 50%; border: 2px solid transparent; background-clip: padding-box;
        transition: all .4s ease; position: relative; overflow: hidden;
    }}
    .social-icon::before {{
        content: ''; position: absolute; inset: 0; border-radius: 50%; padding: 2px;
        background: linear-gradient(45deg, var(--accent), var(--accent2), var(--gold));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: exclude; mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude; opacity: 0; transition: opacity .4s ease;
    }}
    .social-icon:hover::before {{ opacity: 1; }}
    .social-icon:hover {{ transform: translateY(-5px) scale(1.1); box-shadow: 0 10px 30px color-mix(in oklab, var(--accent) 30%, transparent); }}
    .social-icon i {{ color: var(--muted); font-size: 1.5rem; transition: all .3s ease; position: relative; z-index: 1; }}
    .social-icon:hover i {{ color: var(--accent); transform: scale(1.2); }}

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        display: flex;
        flex-wrap: nowrap;
        justify-content: space-between;
        gap: 10px;
        width: 100%;
        padding: 10px;
        border-radius: 16px;
        background: {panel_bg};
        border: 1px solid {panel_border};
        backdrop-filter: blur(var(--blur));
        overflow-x: auto;
        scrollbar-width: none;
    }}

    .stTabs [data-baseweb="tab"] {{
        flex: 1 1 auto;
        min-width: 110px;
        height: 44px;
        padding: 0 16px;
        border-radius: 12px;
        color: var(--muted);
        background: transparent;
        border: 1px solid transparent;
        transition: all .25s ease;
        font-weight: 600;
        letter-spacing: .2px;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, color-mix(in oklab, var(--accent) 20%, transparent), color-mix(in oklab, var(--accent2) 10%, transparent)) !important;
        color: var(--accent) !important;
        border: 1px solid color-mix(in oklab, var(--accent) 35%, transparent) !important;
        box-shadow: 0 4px 15px color-mix(in oklab, var(--accent) 20%, transparent);
    }}

    /* Input Field Styling - Đồng bộ với theme */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    input[type="text"],
    input[type="number"],
    textarea {{
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(var(--blur)) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    input[type="text"]:focus,
    input[type="number"]:focus,
    textarea:focus {{
        border: 2px solid {input_focus_border} !important;
        box-shadow: 0 0 0 3px color-mix(in oklab, var(--accent) 20%, transparent) !important;
        outline: none !important;
        transform: translateY(-1px) !important;
    }}

    .stTextInput > div > div > input::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: var(--muted) !important;
        opacity: 0.8 !important;
    }}

    /* Button styling - Đồng bộ hoàn toàn với theme */
    .stButton button,
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"] {{
        background: rgba(255,255,255,0.0) !important;
        color: {button_text} !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: {button_shadow} !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        cursor: pointer !important;
    }}

    .stButton button:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px color-mix(in oklab, var(--accent) 35%, transparent) !important;
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    }}

    .stButton button:active,
    button[data-testid="baseButton-primary"]:active,
    button[data-testid="baseButton-secondary"]:active {{
        transform: translateY(0) scale(1) !important;
        box-shadow: 0 2px 8px color-mix(in oklab, var(--accent) 25%, transparent) !important;
    }}

    /* Streamlit specific button fixes */
    .stDownloadButton button {{
        background: linear-gradient(135deg, var(--gold), #ffa000) !important;
        color: white !important;
    }}

    .stDownloadButton button:hover {{
        background: linear-gradient(135deg, #ffa000, var(--gold)) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }}

    /* Generic buttons (dialogs, forms, etc.) */
    button[data-baseweb="button"] {{
        background: {input_bg} !important;
        color: var(--text) !important;
        border: 1px solid {input_border} !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        margin: 0.25rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }}

    button[data-baseweb="button"]:hover {{
        background: var(--accent) !important;
        color: white !important;
        transform: translateY(-1px) !important;
        border-color: var(--accent) !important;
    }}

    /* Decorative line */
    .decoration-line {{
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
        margin: 2rem 0; border-radius: 1px; animation: pulse-line 3s ease-in-out infinite;
    }}
    @keyframes pulse-line {{
        0%, 100% {{ opacity: .5; transform: scaleX(1); }}
        50% {{ opacity: 1; transform: scaleX(1.02); }}
    }}

    /* Floating elements — Ẩn trong light mode */
    .floating-element {{
        position: absolute; border-radius: 50%; opacity: 0.1; animation: float 6s ease-in-out infinite;
        {'display: none;' if is_light else ''}
    }}
    .floating-element:nth-child(1) {{ width: 80px; height: 80px; top: 10%; right: 10%; background: var(--accent); animation-delay: 0s; }}
    .floating-element:nth-child(2) {{ width: 60px; height: 60px; top: 60%; right: 20%; background: var(--accent2); animation-delay: 2s; }}
    .floating-element:nth-child(3) {{ width: 40px; height: 40px; top: 30%; right: 5%; background: var(--gold); animation-delay: 4s; }}
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        33%      {{ transform: translateY(-20px) rotate(120deg); }}
        66%      {{ transform: translateY(10px) rotate(240deg); }}
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: {scrollbar_track_bg}; border-radius: 10px; }}
    ::-webkit-scrollbar-thumb {{ background: {scrollbar_thumb_bg}; border-radius: 10px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(135deg, var(--accent2), var(--accent)); }}

    /* Additional fixes for stack display area */
    .stAlert {{
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        backdrop-filter: blur(var(--blur)) !important;
    }}

    /* Ensure all text elements are properly colored */
    p, span, div, label {{
        color: var(--text) !important;
    }}

    /* Fix for metric containers */
    .stMetric {{
        background: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        backdrop-filter: blur(var(--blur)) !important;
    }}
    </style>
    """).strip()