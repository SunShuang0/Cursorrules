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
| **Build, Deployment and CI/CD** | CI/CD |  |
| | Deployment & Release Management |  |
| | Reference Documentation & Libraries |  |
| **Code Quality and Engineering Practices** | API Type Safety & Consistency |  |
| | Asynchronous Programming |  |
| | Best Practices |  |
| | Code Formatting & Syntax |  |
| | Code Quality Control |  |
| | Code Review |  |
| | Coding Example/Template |  |
| | Coding Style |  |
| | Defensive Programming |  |
| | Frontend/UI Practices |  |
| | ML - Specific |  |
| | Naming Conventions |  |
| | Performance Optimization |  |
| | Tool Usage |  |
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
