# Commit Message Instructions

Generate concise, professional Git commit messages for the Weather Intelligence Platform.

## Format

Use exactly this structure:

`<type>(<scope>): <short imperative description>`
- `<primary change>`
- `<technical change>`
- `<purpose, impact, or validation>`

## Rules

- Title: maximum 72 characters.
- Use imperative language.
- Use Conventional Commit types: feat, fix, refactor, test, docs, chore, deploy, ci, perf.
- Use a short, relevant scope such as k8s, airflow, api, ml, docker, postgres, spark, dashboard, oci, aws.
- Description: 2–4 lines only.
- Every description line MUST start with `-`.
- One clear point per line.
- Keep each line concise, normally under 120 characters.
- Do not write paragraph-style descriptions.
- Do not add blank lines between description bullets.
- Describe only changes supported by the Git diff.
- Do not invent tests, deployment results, or functionality.
- Do not use vague phrases such as "updated files", "made changes", or "improved the project".
- Do not repeat the commit title in the description.

## Project Task

When clearly identifiable, include the relevant task in the first description line:

- W# D# for Phase 1
- P2-W# D# for Phase 2

Do not invent a task number. Omit it when it cannot be determined reliably.

## Examples

feat(k8s): deploy FastAPI service
- W11 D3: Added the FastAPI Kubernetes Deployment.
- Added the Kubernetes Service configuration.
- Configured required API environment variables.
- Prepared the API for cluster deployment.

fix(api): correct prediction response
- W10 D4: Fixed validation of the prediction response.
- Updated the API response handling.
- Added validation for the corrected response structure.

docs(k8s): document deployment commands
- W11 D4: Added Kubernetes deployment and verification commands.
- Documented pod, deployment, and service inspection.
- Clarified the deployment workflow.
