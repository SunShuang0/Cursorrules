# Overview
This is a study of .cursorrules files in GitHub open source projects.

Here, we share the materials we produced in this study:
- The rawler script: crawler_cursorrules.py
- The repo files counting script: files_count.py
- The database designing: patterns.md
- The dataset: \[the whole dataset will be shared once the paper is accepted\]
- The codebook: codebook_cursorrules.md

## Overview of the study
Prompts are the primary mechanism for communicating with AI agents and directly influence the quality and reliability of AI-generated code. As AI-assisted programming becomes widely adopted, modern tools increasingly combine dynamic conversational prompts with static configuration-like prompt files. Despite the growing trend, prior research has primarily focused on conversational prompts, while prompt files remain understudied.

To address this gap, we conduct an empirical study of configuration prompt files in Cursor, a widely used AI-assisted code editor. We collect and analyze over 12,110 .cursorrules files from 11,427 GitHub repositories to characterize their distribution, evolution, and maintenance. Complementing this, we perform qualitative analysis on a sample of 65 prompt files and develop a 65-code codebook capturing how developers express programming intent, project context, engineering practices, and security considerations.

Our results show that .cursorrules files emerged rapidly from mid-2024. Their adoption is concentrated in small-scale, low-activity, single-maintainer repositories, suggesting toy projects rather than professional development. The content of prompt files is dominated by guidance on code quality and engineering practices, project structure and configuration, and maintainability, while security-related content appears less frequently. Our analysis shows that there is a continuity of themes and topics between the now-legacy .cursorrules files and the current standard *.mdc files. 


## Research Questions
**RQ1**: What are .cursorrules files, and in which open source projects do they appear?

**RQ2**: What is the evolution of .cursorrules files?

**RQ3**: What are the major topics in .cursorrules?

**RQ4**: Which types of security aspects are considered in .cursorrules?

To answer RQ1 and RQ2, we conducted a quantitative analysis on 11746 repos that contain .cursorrules files. Here, we publish the crawler scripts we built and used during the study, the patterns that we collected, and the figure-drawing scripts, so that anyone who is interested can reproduce the entire analysis process easily.

To answer RQ3 and RQ4, we conducted a qualitative analysis on 51 .cursorrules files and 14 .cursor/rules .mdc files on ATLAS.ti, and eventually established a comprehensive codebook that consists of 70 codes that are themed into 10 themes. Here, we publish our ATLAS project pack and codebook, and provide a brief description (definition & scope) for each code and each theme. Based on this, it would be easier to review and discuss the appropriateness of the codebook.

## Quantitative Analysis
### Crawler with a keyword-strategy
crawler_cursorrules.py

### Repo files counting without traversal
files_count.py

### Database design
patterns.md

### Dataset
The whole dataset will be shared once the paper is accepted.


## Qualitative Analysis
### Top 10 codes in .cursorrules and .mdc files

| Code (short)                                | Freq  | Representative excerpt |
|----------------------------------------------|-------|-------------------------|
| Languages, Stacks & Usage Guidance           | 10.3% | FastAPI backend developer with deep knowledge of Python 3.11+. |
| Exclusion Behaviors                          | 5.8%  | Avoid unnecessary curly braces in conditionals. |
| Tool Usage                                   | 5.3%  | You could use the tools/web_scraper.py file to scrape the web. |
| Performance Optimization                      | 4.4%  | Use Python 3.11+ features for improved performance and type safety. |
| Coding Style                                 | 3.6%  | Write concise, technical TypeScript code with accurate examples. |
| Code Readability & Maintainability           | 3.5%  | Refactor to improve readability and reduce future maintenance cost. |
| Error & Exception Handling                   | 3.2%  | Use early returns and guard clauses; implement proper exception handling. |
| Naming Conventions                           | 3.2%  | Use descriptive variable names with proper prefixes. |
| **Security Awareness, Mechanisms & Practices** | 3.0%  | Follow security best practices. Validate all input data. Protect against common vulnerabilities. Handle sensitive data appropriately. |
| Project Structure & Architecture             | 2.6%  | `<directory_structure>`: api/ API documentation and Swagger files ... |



### Top 10 codes in .mdc files
| Code (short)                                      | Freq  | Representative excerpt |
|---------------------------------------------------|-------|-------------------------|
| Languages, Stacks & Usage Guidance                | 12.2% | ... modern frontend development with Next.js 15 and React 18 |
| Coding Example/Template                           | 6.8%  | Good: `A["User Input"] --> B["Validate Data"];` Bad (potential error): `A[User Input] --> B[Validate Data];` |
| Exclusion Behaviors                               | 6.2%  | Do NOT use Unix/Linux commands that don't exist on Windows. |
| Project Structure & Architecture                  | 5.9%  | Assume a modular structure: `app/`, `components/`, `lib/`, `shared/`, `routes/` |
| Frontend/UI Practices                             | 5.1%  | Use Shadcn UI, Radix, and Tailwind for components and styling. |
| Rule File Description, Scopes & Nested Structures | 5.1%  | This document defines how Cursor (or any AI) should generate code for this project to prevent unintended results, maintain consistency, and improve developer experience. |
| Tool Usage                                        | 5.1%  | Install Shadcn/UI components with `pnpm dlx shadcn@latest add <component-name>` |
| Cursor Development Behavior Guidance              | 3.9%  | Always look at the example ... Fully implement all requested functionality. |
| Naming Conventions                                | 2.7%  | PascalCase for components, camelCase for functions and variables |
| Best Practices                                    | 2.4%  | Follow memory management best practices |


### Codebook
codebook_cursorrules.md



