import markdown

markdown_string = """
# h1 Heading
## h2 Heading
### h3 Heading

**This is bold text**
*This is italic text*

Unordered List

+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered List

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa

## Tables

| Syntax      | Description |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |
"""

html = markdown.markdown(markdown_string, extensions=['markdown.extensions.tables'])
print(html)