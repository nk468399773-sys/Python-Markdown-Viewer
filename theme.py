import html
import re


CODE_BLOCK_RE = re.compile(
    r"<pre><code(?: class=\"language-([^\"]+)\")?>(.*?)</code></pre>",
    re.DOTALL,
)
UL_RE = re.compile(r"<ul>(.*?)</ul>", re.DOTALL)
LI_RE = re.compile(r"<li>(.*?)</li>", re.DOTALL)


def render_code_blocks(html_text: str) -> str:
    def replace(match):
        language = (match.group(1) or "text").upper()
        code = html.unescape(match.group(2))
        code = code.rstrip("\n")
        code = html.escape(code)
        code = code.replace("\n", "<br>")
        return (
            '<div style="margin: 14px 0 18px 0;">'
            f'<div style="background:#e9edf3;color:#334155;padding:6px 10px;'
            'border:1px solid #d7dce3;border-bottom:none;">'
            f"{language}</div>"
            f'<div style="background:#f7f8fa;color:#111827;padding:12px 14px;'
            'border:1px solid #d7dce3;">'
            f'<code>{code}</code>'
            "</div>"
            "</div>"
        )

    return CODE_BLOCK_RE.sub(replace, html_text)


def render_lists(html_text: str) -> str:
    def replace_ul(match):
        items = LI_RE.findall(match.group(1))
        if not items:
            return match.group(0)

        rendered = []
        for item in items:
            text = item.strip()
            text = re.sub(r"</p>\s*<p>", "<br><br>", text)
            text = re.sub(r"<br\s*/?>", "<br>", text)
            rendered.append(f"&#183; {text}")

        return (
            '<div style="margin: 8px 0 12px 0; line-height: 1.8;">'
            + "<br>".join(rendered)
            + "</div>"
        )

    return UL_RE.sub(replace_ul, html_text)


def wrap_html(content: str, settings) -> str:
    return f"""
    <div style="font-family: Microsoft YaHei UI; color: #1e1e1e; font-size: {settings.font_size}px; line-height: {settings.line_height};">
        {content}
    </div>
    """
