# DOCX Auto-Formatting Tool

## Overview
The project is an **automatic Word document formatting tool** that applies user-defined rules to `.docx` files.  
It eliminates the tedious process of manually formatting unformatted or semi-formatted documents by enforcing consistent styles.  

---

## Purpose
- Automate **boring and time-consuming formatting tasks**.  
- Guarantee **consistency across documents**.  
- Allow customization through flexible configuration.  

---

## Configuration
- **YAML** is used for configuration because of its readability and flexibility.  
- Rules describe formatting instructions at different levels:  

### Document-Level
- Page setup (size, margins, orientation)  
- Headers and footers  
- Default fonts and styles  

### Paragraph-Level
- Alignment (left, right, justified, centered)  
- Spacing (before/after, line spacing)  
- Indentation  
- Paragraph styles  

### Text-Level
- Font family and size  
- Bold, italics, underline  
- Colors  
- Character styles  

### Adjustments
- Standardize **titles, subtitles, or section headers**  
- Normalize **plot/table sources or captions**  
- Perform **find-and-replace operations** (regex or string-based)  

---

## Features
- **Document formatting**: global layout and structure.
- **Paragraph formatting**: spacing, indentation, alignment.
- **Text formatting**: font styles, size, color.
- **Adjustments**: specific text transformations or replacements.
- **Section and Style identyfication**: when user provides docx file identify to which paragraphs which style should be applied
---

## Goal
Users provide:
1. An **input `.docx` file**.
2. A **YAML configuration** containing formatting rules.

The system outputs a **fully formatted Word document** that conforms to the specified style guide.