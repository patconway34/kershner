Custom Backtesting Strategy Repository
This repository contains a collection of trading strategy scripts designed to run on a custom backtesting engine. These scripts depend on a proprietary Python package named cq, which is not publicly distributed. Therefore, the code cannot be compiled or executed independently outside of the full backtesting environment.

Purpose
The main goals of this repository are:

To centralize development of backtesting strategy scripts

To document logic behind each strategy for offline review

To facilitate collaboration among trusted developers

To track progress via Git version control

To standardize the integration of all new variables and logic through documentation.doc

Environment Notes
The cloudquant (cq) package used in these scripts is custom-built and cannot be installed via pip.

Attempting to run, lint, or compile the code outside the approved environment will fail.

Scripts are expected to follow PEP8 and general Python best practices, except when overridden by specific engine or strategy constraints.

Code & Documentation Structure
Each .py file represents a standalone trading strategy model.

The documentation.doc file is the authoritative reference for:

Variable definitions

Strategy purpose and structure

Shared logic and constraints

All helper files (e.g., shared indicators or notes) are also stored in the flat layout.

⚠️ All new variables must be documented first in documentation.doc. If a variable or feature is not described there, it will be flagged during review.

Repository Layout
All files are placed directly in the kershner/ directory.

bash
Copy
Edit
kershner/
├── strategy_one.py         # A strategy model
├── strategy_two.py         # Another model
├── notes.txt               # Optional notes or logs
├── documentation.doc       # Master variable + logic documentation
└── README.md               # This file
There is no subdirectory structure. All scripts, documentation, and references currently exist at the top level.

Getting Started (for contributors)
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/custom-backtester-strategies.git
cd custom-backtester-strategies/kershner
Understand the structure:

One strategy per .py file

Flat file layout — no folders

documentation.doc defines all accepted variables and logic structure

Follow coding standards:

Use PEP8

Add type hints and docstrings

Keep logic modular and clean

Contributing Workflow
Create a feature branch:

bash
Copy
Edit
git checkout -b feature/my-improvements
Make your edits. Be sure to:

Document new variables in documentation.doc

Add inline comments for complex logic

Avoid modifying cq package behavior unless explicitly approved

Commit your changes:

bash
Copy
Edit
git commit -m "Describe changes and rationale"
Push and open a pull request:

Summarize proposed changes

Reference affected scripts or documentation sections

Include reasoning and context

Review Process
Pull requests will be reviewed for:

Logical consistency

Code structure and documentation

Adherence to project-specific and PEP8 standards

Final Notes
This repository is for code review and version tracking, not execution.

Every enhancement must be backed by clear documentation in documentation.doc.

Flat layout simplifies navigation; future folder organization will follow growth and modular needs.
