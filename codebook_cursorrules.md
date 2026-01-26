| Theme | Code | Description of each code |
|-------|------|---------------------------|
| **Access Control** | Access Control | Provide Cursor with guidance on permission design, tell Cursor how to control permissions, including access to system resources, operations and data access, etc., and clarify who can perform what operations in order to prevent overprivileged or unauthorized access. Or remind Cursor to be aware of these issues. |
| | API Access Control | Provide Cursor with guidance on API access control, including permission design, authentication, authorization, and scope restrictions. Remind Cursor to consider API-specific risks such as unauthorized access, excessive privileges, and abuse of public endpoints. |
| | Authentication & Authorization | Guides Cursor on how to implement authentication mechanisms for users, middleware, or APIs, or reminds Cursor to be aware of such concerns. |
| | File/Storage Access Control | Guide Cursor on how to implement access control for files, databases, and storage systems. |
| | Rate Limiting | Reminds Cursor to pay attention to or instructs Cursor on how to limit request rates in API access control, in order to prevent excessive access to API resources. Limiting API request frequency can prevent abuse and DDoS attacks. |
| | Role-Based Access Control | Instructs Cursor on defining different roles (e.g., user/admin) and setting their resource access scope. RBAC, an important category of Access Control. |
| | Token Handling | Guides Cursor on how to construct a token management system or reminds it to pay attention to token-related mechanisms. This includes, but is not limited to: Token-based access control (i.e., using tokens to determine whether a request is authorized), token generation, token transmission, token storage, token expiration and revocation, etc. |
| **Agent Behavior & Rule Files Structure** | Cursor Development Behavior Guidance | Provides step-by-step behavioral instructions for how Cursor should approach programming tasks. Includes planning before coding, confirming understanding, avoiding incomplete outputs, avoiding guessing, and following user instructions precisely. These instructions focus on the process of code generation rather than the structure or quality of the code itself. |
| | Cursor Role Definition | Clearly defines the role Cursor should play, the services it should provide, its tasks, and technical expertise, to help it understand its responsibilities. |
| | Cursor Thinking, Reasoning & Communication Style | Guides Cursor on how to think, respond, ask questions, handle uncertainty, or reminds Cursor to be aware of such concerns. |
| | Cursor's Goal Specification | Tells Cursor what task to perform, what goal to accomplish, or what problem to solve. |
| | Exclusion Behaviors | Forbidden list, forbidden behaviors. |
| | Prompt/Rule Example/Template | Examples or templates that specific targeting how to generate prompts, how to generate rules. |
| | Rule File Description, Scopes & Nested Structures | Introduce the rule files' functions, scope domains, or nested structures (typically appear when there are multiple rule files). |
| **Architecture and Integration** | Dependency Management & Injection | Guides Cursor on how to select, install, manage, and update third-party dependencies. Includes: version, compatibility/migration guidance, upgrades, deprecation handling, dependency injection patterns. Excludes: specifies which dependencies to use and how to use them. (These should be coded as 'Languages, Stacks and Usage Guidance') |
| | Http Architecture | Guides Cursor on how to design HTTP-based communication systems. It reflects architectural-level concerns. Includes: protocol usage, connection management, and request-response modeling. Excludes: runtime network handling. |
| | Modular Architecture & Scalability | Guides Cursor on designing, implementing, and integrating components/modules in a modular and scalable way. Includes: API design strategies, component boundaries, module interfaces, middleware layers (as modular request/response pipelines), and strategies for scaling modules independently. |
| | Routing | Guides Cursor on how to organize and manage the routing system in a project, or reminds Cursor to consider such matters. A nice routing design can improve system maintainability, reduce route conflicts, and lower coupling. It is a foundational element for implementing secure access control. Includes but is not limited to: using routing mechanisms provided by specific frameworks (such as Laravel, FastAPI, React Router), defining clear RESTful routes, modularizing route files, aligning routes with components or functional modules, and using dynamic or nested routing. |
| **Build, Deployment and CI/CD** | CI/CD | Instructs Cursor on how to handle CI/CD or reminds Cursor of related concerns. 'CI/CD' stands for Continuous Integration / Continuous Deployment, is part of 'deployment' but focuses more on automation. Continuous Integration refers to automatic testing and building; Continuous Deployment refers to automatic release to production. |
| | Deployment & Release Management | Guides Cursor on how to deploy and release software into target environments, or reminds Cursor to be aware of related concerns. Includes: deployment piplines, rollout/rollback strategies, build pakaging, release strategies (blue/green, canary, rolling), deployment validation (health checks, smoke tests). |
| | Reference Documentation & Libraries | Tells Cursor which documentation, libraries or information to refer to, to get a better result or avoid guessing or using unreliable sources. |
| **Code Quality and Engineering Practices** | API Type Safety & Consistency | Instructs Cursor to enforce type correctness and consistency, especially at public APIs and module boundaries, using explicit type definitions and static type checking. Includes: explicit typing for public APIs and external interfaces (functions, variables), consistent type usage across modules, avoiding implicit or ambiguous type inference, avoiding implicit conversions, leveraging compiler/type checker guarantees. |
| | Asynchronous Programming | Guides Cursor on how to implement asynchronous programming techniques to improve responsiveness, scalability, and efficiency in I/O-bound or high-concurrency applications. This includes concurrent access, thread safety, use async/await syntax, event loops, non-blocking I/O operations, and asynchronous frameworks or libraries. Proper asynchronous programming enables systems to handle multiple tasks concurrently without blocking execution, leading to better resource utilization and user experience. |
| | Best Practices | Provide Cursor with experience-driven recommendations, which refer to technical practices or methodologies that are reliable in the actual development process. Best practices can help to standardize the coding style, avoid repeated mistakes, improve code quality and maintainability. |
| | Code Formatting & Syntax | Surface-level mechanical rules for layout, formatte and syntax, such as indentation, spacing, line breaks, bracket placement, semicolons, and concise syntax forms. These rules can be automatically detected by scripts. |
| | Code Quality Control | Provides Cursor with a high-level guidance on quality coding. Code quality control is a generalized, broad concept. We split Code Quality into "Annotations", "Testing", "Logging", "Exception Handling", etc., and group them as Group 'Code Quality and Style'.  But we still retain "Code Quality Control" as an independent code for general code quality control instructions, or just mention the keyword but do not provide specific guidance. |
| | Code Review | Tell Cursor to introduce the code review mechanism. Code review is part of the code quality control mechanism, but it's more process-oriented and directly related to security issues, so we make it as an independent code. |
| | Coding Example/Template | Provides code templates or examples for Cursor to better understand programming requirements, project conventions, etc. This includes, but is not limited to, how to call functions, naming conventions, or how to structure a function. Or ask Cursor to reference examples from somewhere else, or ask Cursor to generate examples. |
| | Coding Style | High-level coding style/philosophy/principles for the whole project. For example, write clean, simple, readable code. Not mechanical formatting conventions such as identing with two spaces, etc. Includes: naming conventions (variables, files, directories); function/class design and structure (e.g., functional over class-based); modularization vs. duplication; type/interface chose preference; how to organize module/file; component style (e.g., functional components, hooks). Excludes: architectural patterns; surface-level formatting rules (which can be detected automately by formatter tools). |
| | Defensive Programming | Guides Cursor to adopt defensive strategies to prevent errors or anticipate potential issues. This includes proactive thinking, control flow safeguards, and precondition checks. |
| | Frontend/UI Practices | Provide conventions and practical rules for frontend development or UI design, including but not limited component frameworks, style guides, UI structure, styling conventions, and general frontend architecture to use. It also includes user interface-related guidance such as layout, usage, and interaction patterns. |
| | ML - Specific | Guides Cursor on how to develop, configure, integrate, and manage ML systems, or reminds Cursor to be aware of such concerns. |
| | Naming Conventions | Provide Cursor with specific naming conventions or simply remind Cursor to follow naming conventions, in order to improve code readability and maintainability. Includes but not limits to: function naming conventions, file naming conventions, class naming, naming conventions for functions, classes, types, interfaces, variables, properties, methods, environment constants, files, and directories. |
| | Performance Optimization | Instructs Cursor on how to optimize performance, provides strategies or suggestions for performance optimization, or reminds Cursor to pay attention to such matters. Includes: frontend (e.g., lazy loading, image compression), backend (e.g., database indexing, caching), and network (e.g., CDN, compression) aspects. |
| | Tool Usage | Instruct Cursor on how to use specific tools, scripts, or utilities (e.g., deployment scripts). Includes: command-line instructions, parameters, execution workflows, deployment scripts, build scripts, etc. |
| **Maintainability and Evolution** | Annotation & Type Hints |  |
| | Code Readability & Maintainability |  |
| | Comment |  |
| | Documentation |  |
| | Git & Version Control |  |
| | Reusability |  |
| | System Currency & Iteration |  |
| **Project Structure and Configuration** | Database/Files Migration Policy |  |
| | Languages, Stacks & Usage Guidance |  |
| | Project & Environment Configuration |  |
| | Project Context & Explanation |  |
| | Project Structure & Architecture |  |
| | Type of Application Developed |  |
| **Security** | Security Awareness, Mechanisms & Practices |  |
| | Security Smells |  |
| **System Input, Data Flow and System State** | Cache Mechanisms |  |
| | Data Fetching |  |
| | Data Pipeline & Workflow |  |
| | Data Protection |  |
| | Data Representation Guidelines |  |
| | Data Storage & Integrity |  |
| | Database Design & Operations |  |
| | File Handling & Cleanup |  |
| | Network Handling |  |
| | State Management & Consistency |  |
| | Validation & Sanitize Guidance |  |
| **Testing and Error Handling** | Debugging & Troubleshooting |  |
| | Default Value Handling |  |
| | Error & Exception Handling |  |
| | Logging & Monitoring/Tracking |  |
| | Testing |  |
| | Warning Guideline |  |
