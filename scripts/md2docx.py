#!/usr/bin/env python3
# minimal markdown -> html for textutil docx conversion
import html, re, sys, os, subprocess

CSS = """
body{font-family:-apple-system,"PingFang SC","Helvetica Neue",Helvetica,Arial,sans-serif;
font-size:11.5pt;line-height:1.65;color:#1a1a1a;}
h1{font-size:20pt;border-bottom:2px solid #333;padding-bottom:6px;margin-top:20px;}
h2{font-size:15pt;margin-top:22px;color:#111;}
h3{font-size:12.5pt;margin-top:16px;color:#222;}
table{border-collapse:collapse;width:100%;margin:10px 0;}
th,td{border:1px solid #bbb;padding:6px 8px;font-size:10.5pt;vertical-align:top;}
th{background:#eee;text-align:left;}
blockquote{border-left:3px solid #999;margin:10px 0;padding:4px 14px;background:#f6f6f6;}
code{background:#eee;padding:1px 4px;font-family:Menlo,monospace;font-size:10pt;}
hr{border:none;border-top:1px solid #ccc;margin:18px 0;}
li{margin:3px 0;}
"""

def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', t)
    return t

def convert(md):
    out, lines, i = [], md.split('\n'), 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1; continue
        if s.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i+1].strip()):
            hdr = [c.strip() for c in s.strip('|').split('|')]
            out.append('<table><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in hdr) + '</tr>')
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
                i += 1
            out.append('</table>'); continue
        m = re.match(r'^(#{1,4})\s+(.*)', s)
        if m:
            lv = len(m.group(1)); out.append(f'<h{lv}>{inline(m.group(2))}</h{lv}>'); i += 1; continue
        if re.match(r'^(---+|\*\*\*+)$', s):
            out.append('<hr/>'); i += 1; continue
        if s.startswith('>'):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip()); i += 1
            out.append('<blockquote>' + '<br/>'.join(inline(b) for b in buf) + '</blockquote>'); continue
        if re.match(r'^(\d+\.|[-*])\s+', s):
            tag = 'ol' if re.match(r'^\d+\.', s) else 'ul'
            out.append(f'<{tag}>')
            while i < len(lines) and re.match(r'^(\d+\.|[-*])\s+', lines[i].strip()):
                out.append('<li>' + inline(re.sub(r'^(\d+\.|[-*])\s+', '', lines[i].strip())) + '</li>'); i += 1
            out.append(f'</{tag}>'); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|\||>|---|\d+\.\s|[-*]\s)', lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>')
    return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>' + '\n'.join(out) + '</body></html>'

src, dst = sys.argv[1], sys.argv[2]
md = open(src, encoding='utf-8').read()
tmp = '/tmp/_md2docx.html'
open(tmp, 'w', encoding='utf-8').write(convert(md))
subprocess.run(['textutil', '-convert', 'docx', '-output', dst, tmp], check=True)
os.remove(tmp)
print('OK', dst)
