# 🌐 NetSage AI

## 🤖 AI-Assisted Network Troubleshooting & Diagnosis Platform

> **Evidence • Intelligence • Validation • Human Oversight**

NetSage AI is an intelligent network troubleshooting and diagnosis platform designed to assist network engineers in analyzing network incidents, interpreting technical evidence, identifying probable root causes, and reviewing AI-generated recommendations before they are accepted.

The platform combines **AI-assisted diagnosis**, **deterministic rule validation**, and **human review** into a single workflow.

---

## 🧭 Table of Contents

-   [✨ Project Overview](#-project-overview)
-   [🎯 Problem Statement](#-problem-statement)
-   [💡 Project Vision](#-project-vision)
-   [🚀 Key Features](#-key-features)
-   [🧠 How NetSage AI Works](#-how-netsage-ai-works)
-   [🏗️ System Architecture](#️-system-architecture)
-   [🔄 End-to-End Workflow](#-end-to-end-workflow)
-   [🤖 AI Diagnosis Engine](#-ai-diagnosis-engine)
-   [🔍 Deterministic Rule Checker](#-deterministic-rule-checker)
-   [👨‍💻 Human-in-the-Loop Review](#-human-in-the-loop-review)
-   [📊 Review & Diagnosis Management](#-review--diagnosis-management)
-   [🗂️ Troubleshooting Dataset](#️-troubleshooting-dataset)
-   [🖥️ Frontend](#️-frontend)
-   [⚡ Backend & API](#-backend--api)
-   [📁 Project Structure](#-project-structure)
-   [🛠️ Technology Stack](#️-technology-stack)
-   [💻 Local Installation](#-local-installation)
-   [▶️ Running the Project](#️-running-the-project)
-   [📡 API Documentation](#-api-documentation)
-   [🧪 Testing](#-testing)
-   [☁️ Deployment](#️-deployment)
-   [🔐 Security & Operational Safety](#-security--operational-safety)
-   [📈 Project Status](#-project-status)
-   [🔮 Future Enhancements](#-future-enhancements)
-   [🎓 Educational & Research Value](#-educational--research-value)
-   [🤝 Contributing](#-contributing)
-   [📄 License](#-license)
-   [👤 Author](#-author)

------------------------------------------------------------------------

## ✨ Project Overview

**NetSage AI** is a network troubleshooting and diagnosis platform that
combines AI-assisted reasoning with deterministic networking rules and
human review.

Traditional network troubleshooting often requires an engineer to
manually:

1.  Understand the reported symptom.
2.  Inspect the network topology.
3.  Examine device configuration.
4.  Interpret Cisco command output.
5.  Identify possible root causes.
6.  Validate the suspected issue.
7.  Decide on an appropriate remediation.
8.  Record the final troubleshooting outcome.

NetSage AI brings these activities into a structured workflow.

The platform accepts network evidence such as:

-   📝 Network symptoms
-   🗺️ Topology information
-   💻 Cisco command output
-   ⚙️ Configuration-related observations

It then produces a structured diagnosis that can be independently
checked by deterministic rules and reviewed by a human.

> **Core principle:** AI assists the engineer; it does not replace
> engineering judgment.

------------------------------------------------------------------------

## 🎯 Problem Statement

Network failures can originate from many different configuration or
infrastructure conditions.

For example, a connectivity problem may be caused by:

-   Incorrect VLAN assignment
-   Invalid gateway configuration
-   DHCP issues
-   DNS resolution problems
-   Routing problems
-   Access-control rules
-   NAT configuration
-   Interface failures
-   Duplicate IP addresses
-   Incorrect subnet masks
-   Wireless configuration problems

The challenge is not simply identifying a possible cause. The challenge
is determining whether the available evidence actually supports that
cause.

NetSage AI addresses this challenge by combining **evidence-based
diagnosis, deterministic validation, and human oversight**.

------------------------------------------------------------------------

## 💡 Project Vision

NetSage AI is built around a simple idea:

``` text
                    NETWORK EVIDENCE
                           │
                           ▼
                  ┌─────────────────┐
                  │   AI ANALYSIS   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ RULE VALIDATION │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  HUMAN REVIEW   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ FINAL DECISION  │
                  └─────────────────┘
```

The objective is to make troubleshooting:

-   🧠 More intelligent
-   🔎 More evidence-driven
-   ✅ More verifiable
-   👨‍💻 More reviewable
-   📋 More structured
-   📈 Easier to analyze over time

------------------------------------------------------------------------

# 🚀 Key Features

## 🤖 1. AI-Assisted Network Diagnosis

The diagnosis engine analyzes supplied network evidence and produces a
structured recommendation.

A diagnosis can contain information such as:

-   🔴 Identified issue
-   🧩 Probable root cause
-   🛠️ Recommended action
-   🔎 Supporting evidence
-   📊 Confidence-related information

The goal is to transform raw troubleshooting information into an
understandable engineering recommendation.

------------------------------------------------------------------------

## 💻 2. Cisco Command Evidence

NetSage AI is designed around real-world network troubleshooting
evidence.

Examples of Cisco-style evidence include:

``` text
show interfaces status
show ip interface brief
show vlan brief
show ip route
show running-config
```

The command output can provide important clues about:

-   Interface state
-   VLAN membership
-   IP addressing
-   Routing information
-   Device configuration
-   Network reachability

------------------------------------------------------------------------

## 🔍 3. Deterministic Rule Validation

AI-generated recommendations are not treated as automatically correct.

NetSage AI complements AI analysis with deterministic validation.

The rule-checking layer can evaluate networking conditions such as:

-   🌐 Duplicate IP detection
-   🎭 Subnet mask validation
-   🚪 Gateway validation
-   🏷️ VLAN validation
-   🔌 Interface status validation
-   🛣️ Routing validation

This creates an additional verification layer between an AI
recommendation and a human decision.

------------------------------------------------------------------------

## 👨‍⚖️ 4. Human-in-the-Loop Decision Making

NetSage AI follows a human-oversight model.

Every AI recommendation can be:

### ✅ ACCEPTED

The reviewer agrees with the recommendation.

### ✏️ EDITED

The reviewer modifies the recommendation based on their engineering
judgment.

### ❌ REJECTED

The reviewer determines that the recommendation should not be accepted.

This is especially important for network infrastructure because an
incorrect recommendation can have operational consequences.

------------------------------------------------------------------------

## 📚 5. Troubleshooting Case Management

The platform works with structured troubleshooting cases.

A case can contain information about:

-   Network symptoms
-   Topology
-   Network evidence
-   Expected diagnosis
-   Troubleshooting category
-   Supporting information

This provides a consistent foundation for testing and demonstrating the
diagnosis workflow.

------------------------------------------------------------------------

## 📊 6. Review Statistics

Human review records can be analyzed to understand how AI
recommendations perform.

Examples of useful statistics include:

``` text
Total Reviews
Accepted Reviews
Edited Reviews
Rejected Reviews
Human Corrections
```

This creates a foundation for measuring the usefulness of the diagnosis
system.

------------------------------------------------------------------------

## 🕘 7. Diagnosis & Review History

The platform provides a structured approach for maintaining
troubleshooting history.

Historical records can help engineers understand:

-   Previous cases
-   Previous recommendations
-   Human decisions
-   Corrections
-   Recurring troubleshooting patterns

------------------------------------------------------------------------

## 🖥️ 8. Professional Web Dashboard

The frontend provides a dedicated network troubleshooting interface.

The dashboard is designed around major workflow areas including:

-   🧪 Troubleshooting Cases
-   🕘 Diagnosis History
-   🔍 Rule Checker
-   👨‍💻 Human Review
-   🛡️ Human Oversight

The interface also communicates the state of the major system
components:

``` text
AI Diagnosis       → Ready
Rule Checker       → Ready
Human Review       → Required
```

------------------------------------------------------------------------

# 🧠 How NetSage AI Works

NetSage AI follows a multi-layer diagnostic pipeline.

``` text
┌─────────────────────────────┐
│       Engineer Input        │
│                             │
│ • Network Symptom           │
│ • Topology Notes            │
│ • Cisco Command Output      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      AI Diagnosis Engine    │
│                             │
│ • Analyze evidence          │
│ • Identify probable issue   │
│ • Determine root cause      │
│ • Recommend action          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Deterministic Checker    │
│                             │
│ • Validate network rules    │
│ • Identify inconsistencies  │
│ • Cross-check evidence      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Human Reviewer        │
│                             │
│   ACCEPT / EDIT / REJECT    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Review Record         │
│                             │
│ • Final decision            │
│ • Corrections               │
│ • Review information        │
└─────────────────────────────┘
```

------------------------------------------------------------------------

# 🏗️ System Architecture

``` text
                         ┌──────────────────────┐
                         │       USER           │
                         │ Network Engineer     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FRONTEND        │
                         │     React + Vite     │
                         └──────────┬───────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌──────────────────────┐
                         │       BACKEND        │
                         │       FastAPI        │
                         └───────┬───────┬──────┘
                                 │       │
                  ┌──────────────┘       └──────────────┐
                  ▼                                     ▼
        ┌──────────────────┐                   ┌──────────────────┐
        │ AI Diagnosis     │                   │ Rule Checker     │
        │ Engine           │                   │                  │
        └────────┬─────────┘                   └────────┬─────────┘
                 │                                      │
                 └────────────────┬─────────────────────┘
                                  ▼
                       ┌──────────────────────┐
                       │   HUMAN REVIEW       │
                       │ Accept / Edit /      │
                       │ Reject               │
                       └──────────┬───────────┘
                                  ▼
                       ┌──────────────────────┐
                       │ REVIEW MANAGEMENT    │
                       │ History & Statistics │
                       └──────────────────────┘
```

------------------------------------------------------------------------

# 🔄 End-to-End Workflow

### 1️⃣ Submit Evidence

The engineer enters the network symptom and relevant evidence.

Example:

``` text
A PC receives an IP address but cannot reach
the server in VLAN 30.
```

### 2️⃣ Add Topology Information

``` text
PC is connected to an access switch.
Server is located in VLAN 30.
Gateway is configured on the router.
```

### 3️⃣ Add Cisco Evidence

``` text
show interfaces status
show vlan brief
show ip route
```

### 4️⃣ Generate AI Diagnosis

The diagnosis engine analyzes the available evidence and produces a
structured recommendation.

### 5️⃣ Validate the Diagnosis

The deterministic checker evaluates relevant network rules
independently.

### 6️⃣ Human Review

The reviewer examines the AI recommendation, evidence, validation
results, and suggested remediation.

The reviewer chooses:

``` text
✅ ACCEPT
✏️ EDIT
❌ REJECT
```

### 7️⃣ Store the Outcome

The final review information is recorded for traceability and future
analysis.

------------------------------------------------------------------------

# 🤖 AI Diagnosis Engine

The AI diagnosis layer is responsible for converting network evidence
into a structured troubleshooting recommendation.

The engine is located in:

``` text
ai/diagnosis_engine.py
```

The project also contains a corresponding test module:

``` text
ai/test_diagnosis_engine.py
```

The diagnosis engine is intended to reason over the evidence supplied by
the engineer rather than making unsupported assumptions.

------------------------------------------------------------------------

# 🔍 Deterministic Rule Checker

The deterministic validation layer provides rule-based network
verification.

This is important because AI reasoning and deterministic engineering
rules serve different purposes.

``` text
AI
│
├── Flexible evidence interpretation
├── Probable root-cause reasoning
└── Recommendation generation

Deterministic Rules
│
├── Explicit networking conditions
├── Repeatable validation
└── Consistent results
```

Combining both approaches provides a stronger troubleshooting workflow.

------------------------------------------------------------------------

# 👨‍💻 Human-in-the-Loop Review

Human oversight is a central design principle of NetSage AI.

The system does not assume:

``` text
AI Recommendation = Final Truth
```

Instead:

``` text
AI Recommendation
        │
        ▼
Evidence + Rule Validation
        │
        ▼
Human Engineering Review
        │
        ├── ✅ Accept
        ├── ✏️ Edit
        └── ❌ Reject
```

------------------------------------------------------------------------

# 📊 Review & Diagnosis Management

The review layer is implemented through:

``` text
review/review_manager.py
review/review_log.json
```

The review manager supports operations around:

-   Loading reviews
-   Creating reviews
-   Review statistics
-   Corrected reviews

This provides a foundation for measuring how human reviewers interact
with AI-generated recommendations.

------------------------------------------------------------------------

# 🗂️ Troubleshooting Dataset

The project contains structured troubleshooting data in:

``` text
data/cases.csv
```

The dataset is loaded through:

``` text
data/case_loader.py
```

Representative troubleshooting areas include:

  Category          Example Focus
  ----------------- ----------------------------------
  🏷️ VLAN           VLAN assignment and segmentation
  🚪 Gateway        Default gateway configuration
  📡 DHCP           Address assignment
  🌐 DNS            Name resolution
  🛣️ Routing        Route and reachability issues
  🔐 ACL            Access-control behavior
  🔄 NAT            Address translation
  📶 Wireless       Wireless connectivity
  🔌 Interface      Interface state
  ⚠️ Duplicate IP   Address conflicts
  🎭 Subnet Mask    Addressing inconsistencies

------------------------------------------------------------------------

# 🖥️ Frontend

The frontend is implemented using:

-   ⚛️ React
-   ⚡ Vite
-   🎨 CSS
-   🟨 JavaScript

Important files:

``` text
frontend/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── package.json
└── vite.config.js
```

The frontend provides the primary user interface for interacting with
the troubleshooting workflow.

------------------------------------------------------------------------

# ⚡ Backend & API

The backend is implemented using **FastAPI**.

Main backend entry point:

``` text
backend/main.py
```

The backend integrates the major project components and exposes API
functionality for the frontend.

The application is served locally with Uvicorn.

------------------------------------------------------------------------

# 📁 Project Structure

``` text
NetSage-AI/
│
├── 🤖 ai/
│   ├── diagnosis_engine.py
│   └── test_diagnosis_engine.py
│
├── ⚡ backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── 🔍 checker/
│   └── ...
│
├── 🗂️ data/
│   ├── case_loader.py
│   └── cases.csv
│
├── 🖥️ frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── 📝 prompts/
│   └── ai/
│
├── 👨‍💻 review/
│   ├── review_manager.py
│   └── review_log.json
│
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Layer                 Technology
  --------------------- -----------------------------
  🖥️ Frontend           React
  ⚡ Frontend Tooling   Vite
  🎨 Styling            CSS
  🐍 Backend            Python
  🚀 API Framework      FastAPI
  🔥 ASGI Server        Uvicorn
  🧠 Intelligence       AI-assisted diagnosis
  🔍 Validation         Deterministic network rules
  📄 Dataset            CSV
  📊 Review Records     JSON
  🔧 Version Control    Git
  🐙 Repository         GitHub
  ☁️ Deployment         Render

------------------------------------------------------------------------

# 💻 Local Installation

## 📋 Prerequisites

Install:

-   🐍 Python 3
-   🟢 Node.js
-   📦 npm
-   🔧 Git

## 1️⃣ Clone

``` bash
git clone https://github.com/sakshat0545-collab/NetSage-AI.git
cd NetSage-AI
```

## 2️⃣ Backend

``` bash
cd backend
pip install -r requirements.txt
```

## 3️⃣ Start Backend

``` bash
uvicorn main:app --reload
```

Backend:

``` text
http://127.0.0.1:8000
```

## 4️⃣ Frontend

Open a second terminal:

``` bash
cd frontend
npm install
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

# 📡 API Documentation

FastAPI provides interactive API documentation automatically.

With the backend running:

``` text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to:

-   🔎 Inspect endpoints
-   🧪 Test requests
-   📥 Submit data
-   📤 Inspect responses
-   🛠️ Debug backend behavior

Alternative documentation:

``` text
http://127.0.0.1:8000/redoc
```

------------------------------------------------------------------------

# 🧪 Testing

Testing support is included for the diagnosis engine.

``` text
ai/test_diagnosis_engine.py
```

Testing should verify:

-   Diagnosis generation
-   Evidence interpretation
-   Expected troubleshooting cases
-   Deterministic validation
-   Review operations
-   Correct recording of decisions

------------------------------------------------------------------------

# ☁️ Deployment

NetSage AI is designed to support cloud deployment.

The backend can be deployed as a web service using **Render**.

A production-style command can be configured around the FastAPI
application:

``` bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Because this repository contains multiple top-level Python components,
deployment configuration must ensure that Python can resolve the `ai`,
`review`, and `backend` modules correctly.

> ⚠️ Always verify deployment logs before considering a production
> service operational.

------------------------------------------------------------------------

# 🔐 Security & Operational Safety

NetSage AI is a **diagnostic assistance platform**, not an autonomous
network-change system.

Recommended operational model:

``` text
AI Recommendation
       │
       ▼
Evidence Verification
       │
       ▼
Rule Validation
       │
       ▼
Human Approval
       │
       ▼
Controlled Network Change
```

### 🔒 Security Principles

-   Never commit passwords or API keys.
-   Never expose credentials in source code.
-   Use environment variables for secrets.
-   Avoid uploading sensitive production configurations unnecessarily.
-   Validate AI-generated recommendations before applying them.
-   Use appropriate access controls for production deployments.

------------------------------------------------------------------------

# 📈 Project Status

## ✅ Implemented

-   [x] 🤖 AI-assisted diagnosis engine
-   [x] 🗂️ Structured troubleshooting cases
-   [x] 🔍 Deterministic rule validation
-   [x] 👨‍💻 Human review workflow
-   [x] 📊 Review statistics
-   [x] 🕘 Review/diagnosis history foundation
-   [x] ⚡ FastAPI backend
-   [x] 🖥️ React + Vite frontend
-   [x] 📡 Swagger API documentation
-   [x] 🔧 Git/GitHub repository
-   [x] ☁️ Cloud deployment configuration

## 🚧 Future / In Progress

-   [ ] 🌐 Complete production frontend deployment
-   [ ] 🔗 Production frontend/backend integration
-   [ ] 🧪 Expanded automated test coverage
-   [ ] 🗄️ Production-grade database
-   [ ] 🔐 Authentication and authorization
-   [ ] 📈 Advanced monitoring
-   [ ] 🧠 More advanced diagnosis intelligence

------------------------------------------------------------------------

# 🔮 Future Enhancements

### 🗄️ Persistent Database

Move review storage to a production database for:

-   Better scalability
-   Queryable history
-   Concurrent access
-   Structured analytics

### 🔐 Authentication & Authorization

Potential roles:

``` text
Administrator
Network Engineer
Reviewer
Viewer
```

### 🌐 Advanced Topology Analysis

Future versions could analyze:

-   Device relationships
-   VLAN paths
-   Routing paths
-   Interface dependencies
-   Network segmentation

### 📡 Network Monitoring Integration

Potential integration with monitoring platforms could allow analysis of
live network telemetry.

### 🧠 Improved AI Reasoning

Potential improvements:

-   Better evidence ranking
-   Detailed confidence scoring
-   Multi-step troubleshooting
-   Historical case similarity
-   Expanded networking knowledge
-   Additional Cisco command parsers

### 🔄 CI/CD

A future automated pipeline could follow:

``` text
GitHub
   │
   ▼
Automated Tests
   │
   ▼
Build
   │
   ▼
Deployment
   │
   ▼
Production
```

------------------------------------------------------------------------

# 🎓 Educational & Research Value

NetSage AI demonstrates the integration of several important areas of
computer science and software engineering.

### 🤖 Artificial Intelligence

-   AI-assisted reasoning
-   Evidence-based diagnosis
-   Recommendation generation

### 🌐 Computer Networking

-   VLANs
-   IP addressing
-   Subnetting
-   Gateways
-   Routing
-   DNS
-   DHCP
-   ACLs
-   NAT
-   Network interfaces

### 🧑‍💻 Software Engineering

-   Modular architecture
-   REST APIs
-   Frontend/backend separation
-   Testing
-   Version control
-   Cloud deployment

### 🛡️ Responsible AI

-   Human oversight
-   Explainability
-   Validation
-   Controlled acceptance
-   Auditability

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Create a feature branch:

``` bash
git checkout -b feature/your-feature
```

Make your changes and test them locally.

Then:

``` bash
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Open a Pull Request on GitHub.

------------------------------------------------------------------------

# 📄 License

This project is currently intended for **educational, research, and
demonstration purposes**.

A formal open-source license can be added as the project evolves.

------------------------------------------------------------------------

# 👤 Author

## Sakshat Shrivatra

🎓 Computer Science / Software Engineering Project

🐙 GitHub:\
https://github.com/sakshat0545-collab

------------------------------------------------------------------------

# ⭐ NetSage AI

### 🌐 Smarter Network Troubleshooting Through

**🤖 AI Intelligence + 🔍 Deterministic Validation + 👨‍💻 Human
Expertise**

> **Diagnose intelligently. Validate deterministically. Decide
> responsibly.**

------------------------------------------------------------------------

```{=html}
<p align="center">
```
Built with ❤️ for intelligent and responsible network troubleshooting.
```{=html}
</p>
```
