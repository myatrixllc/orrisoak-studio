#!/usr/bin/env python3
"""
ORRISOAK STUDIO — Apply Black/Gold/White Theme to All Tools
Run from: /Users/jularyy/data/orrisoak-studio/
Command:  python3 apply-theme.py
"""

import glob, os

# ── THEME REPLACEMENTS ──
# Each tuple: (old_string, new_string)
REPLACEMENTS = [
    # CSS Variables — dark high-contrast theme
    ('--gold:#C9A84C;--gold-light:#E8D5A3;--gold-dim:rgba(201,168,76,0.1);\n  --gold-border:rgba(201,168,76,0.2);--black:#070707;--s1:#0F0F0F;\n  --s2:#161616;--s3:#1E1E1E;--s4:#252525;--cream:#F0E9DC;--muted:#786D61;\n  --green:#4CAF7D;--blue:#7B9FE8;--orange:#D4894A;--red:#D45A5A;',
     '--gold:#C9A84C;--gold-light:#E8D5A3;--gold-dim:rgba(201,168,76,0.12);\n  --gold-border:rgba(201,168,76,0.35);--black:#080808;--s1:#111111;\n  --s2:#1A1A1A;--s3:#242424;--s4:#2E2E2E;--cream:#F0EDE8;--muted:#C8B89A;\n  --green:#4CAF7A;--blue:#7BAAF0;--orange:#E08840;--red:#E05040;'),

    # Muted color fixes (old dim muted)
    ('--muted:#786D61;', '--muted:#C8B89A;'),
    ('--muted:#A89880;', '--muted:#C8B89A;'),
    ('--muted:#6A5A4A;', '--muted:#C8B89A;'),

    # Cream text color
    ('--cream:#F0E9DC;', '--cream:#F0EDE8;'),
    ('color:var(--muted);line-height:2;}', 'color:#C8B89A;line-height:2;}'),

    # Body backgrounds
    ('body{background:var(--black);color:var(--cream);font-family:\'Josefin Sans\',sans-serif;font-weight:300;min-height:100vh;}',
     'body{background:#080808;color:#F0EDE8;font-family:\'Josefin Sans\',sans-serif;font-weight:300;min-height:100vh;}'),

    # Tool card descriptions
    ('.tool-desc{font-size:9px;letter-spacing:1px;color:var(--muted);line-height:2;}',
     '.tool-desc{font-size:9px;letter-spacing:1px;color:#C8B89A;line-height:2;}'),

    # Tool card backgrounds
    ('.tool-card{background:var(--s1);border:1px solid var(--gold-border);',
     '.tool-card{background:#151515;border:1px solid rgba(201,168,76,0.35);'),

    # Step text
    ('.step-text{font-size:10px;color:var(--muted);line-height:2;}',
     '.step-text{font-size:10px;color:#C8B89A;line-height:2;}'),

    # Sub descriptions
    ('.sub-desc{font-size:10px;color:var(--muted);line-height:2;}',
     '.sub-desc{font-size:10px;color:#C8B89A;line-height:2;}'),

    # Hero subtitle
    ('color:var(--muted);margin-top:14px;line-height:2;position:relative;}',
     'color:#C8B89A;margin-top:14px;line-height:2;position:relative;}'),

    # Stat labels
    ('.hero-stat-label{font-size:7px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);margin-top:4px;}',
     '.hero-stat-label{font-size:7px;letter-spacing:3px;text-transform:uppercase;color:#C8B89A;margin-top:4px;}'),

    # Section backgrounds s1
    ('background:var(--s1);border:1px solid var(--gold-border);padding:24px;',
     'background:#151515;border:1px solid rgba(201,168,76,0.35);padding:24px;'),

    # FM sidebar
    ('.fm-folder{padding:10px 16px;cursor:pointer;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);',
     '.fm-folder{padding:10px 16px;cursor:pointer;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#C8B89A;'),

    # FM empty
    ('.fm-empty{color:var(--muted);font-size:10px;',
     '.fm-empty{color:#C8B89A;font-size:10px;'),

    # Gate box
    ('.gate-sub{font-size:8px;letter-spacing:8px;text-transform:uppercase;color:var(--muted);margin-bottom:40px;}',
     '.gate-sub{font-size:8px;letter-spacing:8px;text-transform:uppercase;color:#C8B89A;margin-bottom:40px;}'),

    # Header date
    ('.header-date{font-size:8px;letter-spacing:4px;text-transform:uppercase;color:var(--muted);}',
     '.header-date{font-size:8px;letter-spacing:4px;text-transform:uppercase;color:#C8B89A;}'),

    # Logout btn
    ('.logout-btn{background:none;border:1px solid rgba(201,168,76,0.2);color:var(--muted);',
     '.logout-btn{background:none;border:1px solid rgba(201,168,76,0.35);color:#C8B89A;'),

    # Code blocks - green text on dark
    ('.code-block{background:var(--black);border:1px solid rgba(201,168,76,0.15);padding:12px 14px;margin-top:10px;font-family:monospace;font-size:11px;color:#98C98A;',
     '.code-block{background:#0D0D0D;border:1px solid rgba(201,168,76,0.25);padding:12px 14px;margin-top:10px;font-family:monospace;font-size:11px;color:#A8E090;'),

    # S1 backgrounds used directly
    ('background:var(--s1);border:1px solid var(--gold-border);margin-bottom:40px;',
     'background:#151515;border:1px solid rgba(201,168,76,0.35);margin-bottom:40px;'),

    # Countdown bar
    ('.countdown-bar{background:var(--s1);border:1px solid var(--gold-border);',
     '.countdown-bar{background:#151515;border:1px solid rgba(201,168,76,0.35);'),

    # File manager
    ('.file-manager{background:var(--s1);border:1px solid var(--gold-border);margin-bottom:40px;}',
     '.file-manager{background:#151515;border:1px solid rgba(201,168,76,0.35);margin-bottom:40px;}'),

    # FM head
    ('.fm-head{background:var(--s2);border-bottom:1px solid var(--gold-border);',
     '.fm-head{background:#1A1A1A;border-bottom:1px solid rgba(201,168,76,0.35);'),

    # FM sidebar border
    ('.fm-sidebar{border-right:1px solid var(--gold-border);padding:16px 0;}',
     '.fm-sidebar{border-right:1px solid rgba(201,168,76,0.35);padding:16px 0;}'),

    # FM main files
    ('.fm-file{background:var(--s2);border:1px solid var(--gold-border);',
     '.fm-file{background:#1A1A1A;border:1px solid rgba(201,168,76,0.35);'),

    # Password section
    ('background:var(--s1);border:1px solid var(--gold-border);padding:24px;margin-bottom:40px;',
     'background:#151515;border:1px solid rgba(201,168,76,0.35);padding:24px;margin-bottom:40px;'),
]

def apply_theme(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            changes += 1

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes

# ── RUN ON ALL HTML FILES ──
files = sorted(glob.glob('*.html'))
total_changes = 0

print('=' * 55)
print('  ORRISOAK STUDIO — Applying Black/Gold/White Theme')
print('=' * 55)

for fname in files:
    changes = apply_theme(fname)
    status = f'✓ {changes} fixes' if changes > 0 else '— no changes'
    print(f'  {fname:<45} {status}')
    total_changes += changes

print('=' * 55)
print(f'  Total: {len(files)} files, {total_changes} replacements applied')
print('  Run: git add . && git commit -m "Apply dark theme" && git push')
print('=' * 55)
