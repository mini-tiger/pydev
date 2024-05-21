def generate_markdown_table(data):
    if not data or not data[0]:
        return ""

    # Get the number of columns
    num_columns = len(data[0])

    # Ensure all data elements are strings and escape any special characters
    def escape_markdown_special_chars(text):
        return str(text).replace('|', '\\|').replace('\n', ' ')

    # Generate the header
    header = "| " + " | ".join(escape_markdown_special_chars(cell) for cell in data[0]) + " |"

    # Generate the separator
    separator = "| " + " | ".join(["---"] * num_columns) + " |"

    # Generate the rows
    rows = ["| " + " | ".join(escape_markdown_special_chars(cell) for cell in row) + " |" for row in data[1:]]

    # Combine all parts
    markdown_table = "\n".join([header, separator] + rows)

    return markdown_table

# Example data with variable number of columns
data = [
    ['1', '高端机械校准件技术-1 (LF~20/26.5GHz, SOTL类型，难度等级3.0)', '0分', '求职者简历中未提及机械校准件技术，缺乏直接相关经验。'],
    ['1', '高端机械校准件技术-1 (LF~20/26.5GHz, SOTL类型，难度等级3.0)', '0分', '求职者简历中未提及机械校准件技术，缺乏直接相关经验。']
]

# Generate the markdown table
markdown_table = generate_markdown_table(data)

# Write the markdown table to a file
with open('output.md', 'w', encoding='utf-8') as file:
    file.write(markdown_table)

print("Markdown table written to output.md")
