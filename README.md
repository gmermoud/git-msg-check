# Git commit message checker

A configurable commit message checker compatible with [pre-commit](https://pre-commit.com).

Clear and informative commit messages promote good collaboration and more
effective code reviews. The checker enforces the following guidelines:

- The header of the commit message must have the following format:

  ```txt
  Pipelines: include column "windowSize" in group by of aggregation

  Bug #249 is fixed by this change.
  ```

- The component tells the reader which area of the code is impacted by
  the change.
- The summary must not exceed 50 characters (configurable via `--max-summary-length`).
- The summary should not end with a dot.
- Any line must not exceed 72 characters (configurable via `--max-line-length`).
- A tag can be prepended to the summary line, for instance:

  ```txt
  [BREAKING] API: remove the field `isValid` to endpoint metrics
  ```

## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/gmermoud/git-msg-check.git
  rev: "insert the version you want to use"
  hooks:
    - id: git-msg-check
      name: Validate commit message
      stages: [commit-msg]
      language_version: python3
      args: ["--max-summary-length=55"]
```

Then, you may install the hook using:

```shell
pre-commit install -t commit-msg
```

## Contribute, bug reports or feature requests

I will gladly review and accept your changes if you submit a PR. Feel free to open an issue 
for any bug or feature request.
