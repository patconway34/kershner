Custom Backtesting Strategy Repository
This repository contains a collection of trading strategy scripts designed to run on a custom backtesting engine. These scripts utilize a proprietary Python package called cq, which is not publicly available. Therefore, code in this repository cannot be compiled or executed independently without the full backtester environment.

Purpose
The main goals of this repository are:

To centralize the development of strategy code

To provide visibility into the logic of each script

To allow for offline review, improvement, and collaboration

To track versions and enhancements through Git versioning

Important Notes
The cloudquant package used throughout the code is custom-built and not available via pip. Do not attempt to run or lint the code without this environment.

All scripts should adhere to PEP8 and general Python best practices, except where overridden by custom engine requirements.

While automated testing and execution are not possible here, code review and optimization are encouraged.

Getting Started (for contributors)
Clone the repository

bash
Copy
Edit
git clone https://github.com/your-username/custom-backtester-strategies.git
cd custom-backtester-strategies
Understand the structure
Each script represents a trading strategy. Standard naming conventions should be used for clarity.

Read and follow Python guidelines
Follow clean coding practices and use type hints, docstrings, and modular structure where possible.

Contribute wisely
Submit pull requests with:

Descriptive commit messages

Inline comments for complex logic

A summary of proposed changes and rationale

Directory Structure
.py files are my models

Create a feature branch: git checkout -b feature/my-improvements

Commit and push your changes

Open a pull request for review

Important: Do not modify the behavior of cq functions unless explicitly coordinating with the backtester team.
