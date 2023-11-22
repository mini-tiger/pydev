# Import Jinja2
from jinja2 import Environment, FileSystemLoader


# ... Your existing code ...

def txt_diff(**kwargs):
    # ... Your existing code ...

    lines = []  # Store information for each line
    line_number = 0

    for line in range(0, 10):
        row= line *2 +1
        line_number += 1

        if line > 5:
            # ... Your existing code ...

            line_info = {
                'number': line_number,
                'type': line,
                'page': line,
                'part': line,
                'result': f'<span style="background-color: #ff9999;">{row}</span>',
            }
        else:
            # ... Your existing code ...

            line_info = {
                'number': line_number,
                'type': line,
                'page': line,
                'part': line,
                'result': f'<span style="background-color: #99ff99;">{row}</span>',
            }

        lines.append(line_info)

    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # Render the template with the dynamic content
    html_output = template.render(lines=lines,src_docx_file="abc",**kwargs)

    with open('diff_output_custom_parser.html', 'w', encoding='utf-8') as file:
        file.write(html_output)

    return html_output


txt_diff(warnings="abc")
