# Overview
This is a study of .cursorrules files in GitHub open source projects.

Here, we share the materials we produced in this study:
- The rawler script: crawler_cursorrules.py
- The repo files counting script: files_count.py
- The database designing: patterns.md
- The dataset: the whole dataset will be shared once the paper is accepted
- The codebook: codebook_cursorrules.md
- The ATLAS.ti project pack: cursorrules.atlasti


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
### Codebook
codebook_cursorrules.md

### ATLAS.ti project pack
cursorrules.atlasti

# Contact Us
