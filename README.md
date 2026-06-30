# JD Analyser \& Resume Fit Scorer

AI-powered tool that analyzes job descriptions and scores resume fit using Claude API.



## Features

* Extracts required skills, experience level, salary estimates from any JD
* Compares your resume against a JD and returns a fit score (0-100)
* Logs every analysis to a growing JSON dataset with timestamps
* Human-in-the-loop salary correction (compares AI estimate vs real market knowledge)





## Tech Stack

Python, Anthropic Claude API, JSON



## What I learned building this

* API integration and prompt engineering
* Structured output parsing (handling LLM markdown-wrapped JSON)
* Building reusable functions vs throwaway scripts
* Data persistence patterns

