Read `AGENTS.md` first.

Then read:

* `<TASK_FILE>`
* `<CLAUDE_REVIEW_JSON>`
* the reviewed LaTeX files
* the sources, implementation files and architecture decisions needed to verify the findings

Verify every Claude finding independently. Claude’s findings are recommendations and must not be accepted automatically.

For each finding:

1. identify the affected passage;
2. verify it against the available evidence;
3. classify it as `ACCEPTED`, `REJECTED` or `DEFERRED`;
4. document the decision under `.ai/decisions/`;
5. apply only changes resulting from `ACCEPTED` findings.

Rules:

* make the smallest sufficient changes;
* do not rewrite unrelated passages;
* do not introduce unsupported facts or citations;
* preserve labels, citation keys and established terminology;
* explain rejected and deferred findings with concrete evidence;
* do not modify the original Claude review;
* do not commit, push or merge.

Do not execute any Python, LaTeX, Git or review scripts. I will run all checks manually.

At the end, report briefly:

1. number of accepted, rejected and deferred findings;
2. decision for each finding;
3. changed files;
4. unresolved issues;
5. the next manual command I should run.
