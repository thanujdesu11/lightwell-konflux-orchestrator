# DO NOT MERGE — DO NOT OPEN A PR UPSTREAM — DO NOT TREAT AS PRODUCTION

**KONFLUX-15844 local spike only** (Thanuj / Perf Scale).

This branch is a **personal backup / scratchpad** of experimental edits so a
clean/SCRATCH Python build can complete on **kflux-lw-p01 /
`konflux-perfscale-3-tenant`**.

## Forbidden

- Do **not** open a pull request against
  `konflux-lightwell/lightwell-konflux-orchestrator`
- Do **not** merge this into `main` on the upstream repo
- Do **not** push this branch to `origin` (upstream)
- Do **not** copy these defaults into Jenkins / prod as-is
- Do **not** assume Lightwell endorses these changes

## Why this must stay out of upstream

1. **Sandbox retargeting** — hardcoded perfscale-3 namespace, kflux-lw-p01 API
   URLs, probe git (`jhutar/lw-pypi.org-ntplib-1`), scratch Quay IR, probe
   git-auth secret name. Those are Perf Scale spike wiring, not Lightwell
   product defaults.
2. **Attach-build-index workaround** — embeds a patched `taskSpec` and optional
   `REQUIRE_VULN` because the shared catalog task hardcodes `--require-vuln`.
   A real fix belongs to Lightwell (official clean-build / catalog task change),
   not a Perf Scale PR that bypasses the catalog.
3. **Fail-closed by design** — `--require-vuln` protects remediated builds;
   relaxing it for SCRATCH is a product decision for Lightwell, not something
   to land casually in their repo.

## What this spike proved

Clean/SCRATCH `ntplib` PipelineRun can go green end-to-end
(clone → sdist → fromager → clamav → attach-build-index with `"vulns": []`)
on the perf sandbox with these local hacks.

## Allowed use

- Reference for Thanuj / Elijah / Jan while discussing KONFLUX-15844
- Personal fork backup under `thanujdesu11/lightwell-konflux-orchestrator`

If upstream wants clean-build support, start a **new, minimal** design with
Lightwell — do not promote this branch.
