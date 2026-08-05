import html as htmllib

def esc(s):
    return htmllib.escape(s, quote=False)

def runs_to_html(runs):
    out = []
    for text, bold, italic in runs:
        t = esc(text)
        if bold and italic:
            t = f'<strong><em>{t}</em></strong>'
        elif bold:
            t = f'<strong>{t}</strong>'
        elif italic:
            t = f'<em>{t}</em>'
        out.append(t)
    return ''.join(out)

def _merge_child_into_parent(list_stack, ul_html):
    last = list_stack[-1][1][-1]
    if last.endswith('</li>'):
        list_stack[-1][1][-1] = last[:-5] + ul_html + '</li>'
    else:
        list_stack[-1][1][-1] = last + ul_html

def convert_blocks(blocks, start, end):
    html_parts = []
    i = start
    list_stack = []

    def pop_deeper_than(level):
        while list_stack and list_stack[-1][0] > level:
            lvl, items = list_stack.pop()
            ul_html = '<ul>' + ''.join(items) + '</ul>'
            if list_stack:
                _merge_child_into_parent(list_stack, ul_html)
            else:
                html_parts.append(ul_html)

    def close_all_lists():
        pop_deeper_than(-1)

    while i < end:
        b = blocks[i]
        style = b['style']
        numpr = b['numpr']
        text = b['text'].strip()

        if not text and not numpr:
            i += 1
            continue

        if numpr is not None:
            ilvl, numid = numpr
            item_html = f'<li>{runs_to_html(b["runs"])}</li>'
            pop_deeper_than(ilvl)
            if list_stack and list_stack[-1][0] == ilvl:
                list_stack[-1][1].append(item_html)
            else:
                list_stack.append([ilvl, [item_html]])
            i += 1
            continue
        else:
            close_all_lists()

        if style == 'Heading2':
            html_parts.append(f'<h2>{runs_to_html(b["runs"])}</h2>')
        elif style == 'Heading3':
            html_parts.append(f'<h3>{runs_to_html(b["runs"])}</h3>')
        elif style == 'Title':
            pass
        else:
            if text:
                html_parts.append(f'<p>{runs_to_html(b["runs"])}</p>')
        i += 1

    close_all_lists()
    return '\n'.join(html_parts)
