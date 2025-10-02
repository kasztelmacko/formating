# Feature Specifications

## Core Features

### 1. docx styles identifier
This feature aims to take docx document as input, and classify each paragraph or text part inside a paragraph to a given style.
The available styles are:
- main_text
- chapter_titles
- subchapter_titles_level_2
- subchapter_titles_level_3
- caption_style
- header_row_style
- source_style

The styles will be classified based on typical characteristics for given style, like:
- common words or characters (ex. Chapter, 1.1.1),
- user feedback loop

### 2. docx style applier
This feature aims to take docx document and a yaml configuration file, and apply the styling based on the config to the styles
The styles applied can be of the following types:

#### document level changes - where user defines document features like:
- page_size
- margins
- orientation
- default_font
- trim_spaces (feature to clean white spaces or empty paragraphs)
- refactor_section_numbering (feature to adjust current document numbering)

#### paragraph_styles - where user defines main style used for main text
- paragraph_format (alignment, spacing, indent)
- font_format

#### chapter_and_section_rules - where user defines rules for chatper and sections
- numbering_format
- paragraph_format
- font_format

#### table_rules - where user defines rules for tables
#### figure_rules - where user defines rules for figures
Both table and figure rules aim to structure the paragraphs around the object (table / figure) by adjusting the paragraph before (adding object number and title), and paragraph after (Source etc.)

#### formula_rules - where user defines rules for formulas

#### list_rules - where user defines rules for numbered / bullet lists
Those rules determine how lists will look like in the document by specifying:
- bullet_char
- paragraph_format
- list_item_termination
- indent

#### header_footer_rules - where user defines rules for document headers and footers
This feature allows comprehensive customization of headers and footers including:
- header_style and footer_style (font formatting and paragraph formatting)
- header_content and footer_content (three-column layout: left, center, right)
- Dynamic field support for:
  - Page numbering: {page}, {numpages}
  - Date and time: {date}, {time}, {datetime}
  - Mixed static and dynamic content

The system uses Word's native field codes to ensure proper functionality when documents are opened in Microsoft Word, with automatic updates for page numbers and dates.