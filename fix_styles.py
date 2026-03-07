import os
import re

html_dir = "templates"
css_file = "static/style.css"

files = ["ala3.html"]

class_counter = 100
new_css = ""
style_map = {}

def process_file(filepath):
    global new_css, class_counter, style_map
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replacer(match):
        global new_css, class_counter, style_map
        tag_start = match.group(1)
        before_style = match.group(2)
        style_val = match.group(3)
        after_style = match.group(4)

        if "display: none" in style_val and len(style_val.strip()) < 15:
            cname = "hidden"
        else:
            if style_val in style_map:
                cname = style_map[style_val]
            else:
                cname = f"extracted-inline-{class_counter}"
                class_counter += 1
                style_map[style_val] = cname
                new_css += f".{cname} {{\n    {style_val}\n}}\n"

        rest_of_tag = before_style + after_style
        
        class_match = re.search(r'class=(["\'])(.*?)\1', rest_of_tag)
        if class_match:
            existing_class = class_match.group(2)
            span_start, span_end = class_match.span(2)
            rest_of_tag = rest_of_tag[:span_start] + existing_class + " " + cname + rest_of_tag[span_end:]
            return f"<{tag_start}{rest_of_tag}>"
        else:
            return f"<{tag_start} class=\"{cname}\"{rest_of_tag}>"

    pattern = re.compile(r'<([a-zA-Z0-9\-]+)([^>]*?)\sstyle="([^"]+)"([^>]*?)>')
    new_content = pattern.sub(replacer, content)

    # Let's also extract <style> blocks
    style_block_pattern = re.compile(r'<style>([\s\S]*?)</style>')
    for m in style_block_pattern.finditer(new_content):
        new_css += f"\n/* Extracted style block */\n{m.group(1)}\n"
    new_content = style_block_pattern.sub('', new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

for f in files:
    process_file(os.path.join(html_dir, f))

with open(css_file, 'a', encoding='utf-8') as f:
    f.write("\n/* --- Automatically extracted inline styles (ala3) --- */\n")
    f.write(new_css)

print("Done extracting styles from ala3.html!")
