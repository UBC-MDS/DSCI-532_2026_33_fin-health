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

   Optionally, you can also install [`conda-lock`](https://github.com/conda/conda-lock) by using **one** of the following commands:

   ```bash
   pipx install conda-lock
   condax install conda-lock
   pip install conda-lock
   conda install --channel=conda-forge --name=base conda-lock
   mamba install --channel=conda-forge --name=base conda-lock
   ```

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

   Or install via `conda-lock` (faster installation):

   ```bash
   conda-lock install -n fin-health conda-lock.yml
   conda activate fin-health
   ```

5. Create a branch for local development using the default branch (typically `develop`) as a starting point. Use `fix` or `feature` as a prefix for your branch name.

    ```shell
    git checkout develop
    git checkout -b fix-name-of-your-bugfix
    ```

    Now you can make your changes locally.

6. When you're done making changes, lint and format your code with [Ruff](https://docs.astral.sh/ruff/):

    ```bash
    ruff check src/ --fix .
    ruff format src/
    ```

7. Check that your changes pass our test suite.

    ```bash
    pytest -v --cov --cov-branch --cov-report=term-missing --cov-report=xml
    ```

8. Commit your changes and push your branch to GitHub. Please use [semantic
   commit messages](https://www.conventionalcommits.org/).

    ```shell
    git add .
    git commit -m "fix: summarize your changes"
    git push -u origin fix-name-of-your-bugfix
    ```

9. Open the link displayed in the message when pushing your new branch in order to submit a pull request.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring.
3. Your pull request will automatically be checked by the full test suite. It needs to pass all of them before it can be considered for merging.
