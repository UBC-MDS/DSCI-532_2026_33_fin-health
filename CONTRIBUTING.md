# Contributing

Contributions of all kinds are welcome here, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

## Example Contributions

You can contribute in many ways, for example:

* [Report bugs](#report-bugs)
* [Fix Bugs](#fix-bugs)
* [Implement Features](#implement-features)
* [Write Documentation](#write-documentation)
* [Submit Feedback](#submit-feedback)

### Report Bugs

Report bugs at <https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues>.

**If you are reporting a bug, please follow the template guidelines. The more
detailed your report, the easier and thus faster we can help you.**

### Fix Bugs

Look through the GitHub issues for bugs. Anything labelled with `bug` and `help wanted` is open to whoever wants to implement it. When you decide to work on such an issue, please assign yourself to it and add a comment that you'll be working on that, too. If you see another issue without the `help wanted` label, just post a comment, the maintainers are usually happy for any support that they can get.

### Implement Features

Look through the GitHub issues for features. Anything labelled with
`enhancement` and `help wanted` is open to whoever wants to implement it. As
for [fixing bugs](#fix-bugs), please assign yourself to the issue and add a comment that you'll be working on that, too. If another enhancement catches your fancy, but it doesn't have the `help wanted` label, just post a comment, the maintainers are usually happy for any support that they can get.

### Write Documentation

fin-health could always use more documentation, whether as
part of the official documentation, in docstrings, or even on the web in blog
posts, articles, and such. Just
[open an issue](https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues)
to let us know what you will be working on so that we can provide you with guidance.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health/issues> using the Peer Review template. If your feedback fits the format of the Peer Review template, please use that. Remember that this is a volunteer-driven project and everybody has limited time.

## Git Workflow

We use a branching workflow based on GitHub Flow. Here's how it works:

### Branch Structure

```
main
 └── develop
      ├── feature/feature-name
      │    └── test/feature-name
      └── fix/bug-name
```

### Workflow Steps

1. **`main` branch**: The stable, production-ready branch. Only receives merges from `develop` after milestone completion.

2. **`develop` branch**: The integration branch where all features and fixes are merged. Branched from `main`.

3. **Feature branches**: For new features, branch from `develop`:

   ```bash
   git switch develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   git push origin feature/your-feature-name
   ```

4. **Fix branches**: For bug fixes, branch from `develop`:

   ```bash
   git switch develop
   git pull origin develop
   git checkout -b fix/bug-name
   git push origin fix/bug-name
   ```

5. **Test branches**: For writing tests, branch from your feature branch:

   ```bash
   git switch feature/your-feature-name
   git checkout -b test/your-feature-name
   git push origin test/your-feature-name
   ```

   When tests are complete, create a PR from `test/your-feature-name` → `feature/your-feature-name`.

6. **Merging back**: Once your feature is complete (code + tests), create a PR from `feature/your-feature-name` → `develop`.

### Pull Request Process

1. Ensure all tests pass locally before creating a PR
2. Request review from at least one team member
3. Address all review comments before merging
4. After approval, merge and delete the feature branch

## Developer Setup

Ready to contribute? Here's how to set up fin-health for
local development.

1. Install [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) as a prerequisite.

2. Fork the <https://github.com/UBC-MDS/DSCI-532_2026_33_fin-health>
   repository on GitHub.

3. Clone your fork locally (*if you want to work locally*)

    ```shell
    git clone git@github.com:your_name_here/DSCI-532_2026_33_fin-health.git
    ```

4. Create and activate the conda environment using one of two ways:

   Install via `conda`:

   ```bash
   conda env create -f environment.yml
   conda activate fin-health
   ```


5. Install `chromium` via `playwright` for browser testing:

   ```bash
   playwright install chromium
   ```

6. Create a branch for local development using the default branch (typically `develop`) as a starting point. Use `fix` or `feature` as a prefix for your branch name.

    ```shell
    git checkout develop
    git checkout -b fix-name-of-your-bugfix
    ```

    Now you can make your changes locally.

7. When you're done making changes, lint and format your code with [Ruff](https://docs.astral.sh/ruff/):

    ```bash
    ruff check src/ --fix .
    ruff format src/
    ```

8. Check that your changes pass our test suite.

    ```bash
    pytest -v --cov --cov-branch --cov-report=term-missing --cov-report=xml
    ```

9. Commit your changes and push your branch to GitHub. Please use [semantic
   commit messages](https://www.conventionalcommits.org/).

    ```shell
    git add .
    git commit -m "fix: summarize your changes"
    git push -u origin fix-name-of-your-bugfix
    ```

10. Open the link displayed in the message when pushing your new branch in order to submit a pull request.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring.
3. Your pull request will automatically be checked by the full test suite. It needs to pass all of them before it can be considered for merging.

## Milestone 3 Retrospective

### What went well

- **Modular refactor**: Breaking the monolithic `app.py` into `data.py`, `components/`, `charts/`, and `pages/` made parallel development much smoother. Team members could work on separate files without constant merge conflicts.
- **Clear task ownership**: Assigning specific files to each team member (e.g., Jiro owns `data.py` and `ai_explorer.py`, Shruti owns adaptive charts) prevented overlap and reduced coordination overhead.
- **querychat integration**: The fin-chat page with natural language data filtering was successfully delivered, adding significant user value.
- **Page 2 completion**: All Company Health KPIs and charts became fully reactive, replacing M2 placeholders.

### What could be improved

- **Blocking dependencies**: Tasks 3–5 were blocked by Task 2 (data module extraction), which created a bottleneck early in the sprint. We should identify and merge blocking PRs within the first 2 days.
- **Testing coverage**: LLM behavior tests were added but unit test coverage for chart builders and components was not comprehensive enough. M4 adds playwright end-to-end tests to address this.
- **PR review turnaround**: Some PRs sat unreviewed for 2–3 days. Setting a 24-hour review SLA would help.

### Key lessons

1. Merge blocking PRs (data modules, shared utilities) within the first 2 days of a milestone.
2. Each PR should include at least one test for the new functionality.
3. Keep PR scope small — one logical change per PR.

## Milestone 4 Collaboration Norms

Building on M3 lessons, the team adopts the following norms for M4:

1. **24-hour review SLA**: All PRs must receive at least one review within 24 hours of opening. If the assigned reviewer is unavailable, any team member may review.

2. **Blocking PRs first**: Environment setup and data migration PRs must be merged within the first 2 days. All other work branches from the updated `develop`.

3. **Test with every feature**: Every feature PR must include at least one test (unit or integration). Playwright tests count for UI features.

4. **Spec before code**: Specification documents (`reports/m4_spec.md`) and `CONTRIBUTING.md` updates are merged before any feature branches are started.

5. **Communication**: Post daily async standup updates in the team Slack channel covering: what you did, what you plan to do, and any blockers.

6. **Branch naming**: Follow the established convention:
   - `docs/` for documentation
   - `chore/` for environment/config
   - `feat/` for new features
   - `fix/` for bug fixes

7. **Commit messages**: Continue using [Conventional Commits](https://www.conventionalcommits.org/) format (e.g., `feat:`, `fix:`, `docs:`, `chore:`, `test:`).