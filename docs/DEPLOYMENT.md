# Google Cloud demo deployment

Verified 2026-10-15. Project `supplieratlas-demo-20261015` (524685338738),
region `us-central1`, service `supplieratlas-demo`.

## Live release

- MCP: https://supplieratlas-demo-524685338738.us-central1.run.app/mcp
- Health: https://supplieratlas-demo-524685338738.us-central1.run.app/health
- Ready revision: `supplieratlas-demo-00004-dfd` (100% traffic).
- Catalog: `alsharqa-engineering-003+b7a55ea019a3` (37 models, 76 tables, 3,707 rows across 22 catalogs).
- Runtime source: https://github.com/mroshdy91/SupplierAtlas-Demo
- Source revision: `fc65173d210529af3eda1f698e1198f0b7d2d4cd`.
- Container: `ghcr.io/mroshdy91/supplieratlas-demo@sha256:c36889fdfbf9f41439afba4c27afbe5689f22f780a6ae4b983b40baf716e5289`.
- CI run `38747553950`: 40 tests and constrained container checks passed.
- Selection verification: 11 native installed-plugin calls exactly matched local
  validated responses; hosted SDK checks, health and unauthenticated 401 passed.
  Service/revision max 1, default min 0, CPU/memory/concurrency/timeout/throttling
  and startup-boost controls read back unchanged. Existing spend cap was not raised.
- Plugin: https://github.com/mroshdy91/SupplierAtlas-Plugin/releases/tag/v0.1.0-alpha.1
  commit `7227beee72a9103acf595bd8f27df60a8506723b`.
- Atlas Marketplace main: `1425615c5ca82963dfe26f40fce193438987bbb4`.

Cloud Run allows public invocation; the application requires a bearer token for
MCP. Health is public. Exactly three tools are exposed. This is a single-token
demo, not a multi-user account system. The generated Cloud Run alternative URL
is not in the app host allowlist; clients must use the documented endpoint.

## Verified cost controls

Request-based billing; minimum 0, maximum 1 instance at both service and revision levels; 0.5 vCPU, 256 MiB;
concurrency 1; 30-second request timeout; generation 1; CPU throttling enabled;
startup CPU boost disabled. No Cloud SQL, VPC connector, external load balancer,
Artifact Registry repository, or Cloud Build job was created for this demo.

The existing billing account had already used 0.64 GiB-month of Artifact Registry
storage (0.5 GiB-month shared free allowance), before this deployment. The user
approved public GHCR instead. Public GitHub Actions builds and GHCR publication
avoid that observed Google registry cost.

A project-scoped Cloud Run spend-cap budget was created and read back with
`outputState: CONFIGURED`: USD 0.10 per calendar month of **gross estimated
Cloud Run usage**, excluding all credits. Budget ID:
`0c0b6369-e8bb-493b-a765-ecfc95fa1ee0`. Notifications at 50%, 80%, and 100%.
This is a conservative usage cutoff, not a paid-spend allowance. It may pause the
demo even when free-tier credits would cover usage. Enforcement delay, in-flight
requests, shared free-tier allowances and uncovered ancillary costs mean this is
not a guaranteed zero-dollar cap. Do not raise it or enable paid services silently.

Google's [free-tier documentation](https://docs.cloud.google.com/free/docs/free-cloud-features),
[Cloud Run pricing](https://cloud.google.com/run/pricing), and
[spend-cap documentation](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
define the actual allowances and limitations. Public package billing is documented
by [GitHub](https://docs.github.com/en/billing/concepts/product-billing/github-packages).

## Repeat deployment without manual uploads

1. Publish reviewed allowlisted backend changes to SupplierAtlas-Demo. The
   `.github/workflows/container.yml` workflow runs tests, builds the catalog and
   container, tests HTTP under 0.5 CPU / 256 MiB, and pushes a source-revision tag
   plus the convenience `demo-001` tag to GHCR. Deploy only a verified digest.
2. From this workspace in PowerShell:

```powershell
.\deploy\deploy.ps1 -Image 'ghcr.io/mroshdy91/supplieratlas-demo@sha256:3eb7177a172d9bf82cf3d73526373c8260361ab67aa4dc30b1083e5bdff34111'
```

The CLI uses the existing approved Google login. It preserves the private token
and cursor key in `%USERPROFILE%\.supplieratlas\runtime.env.yaml`, outside the
repository, with restricted directory ACLs. The command configures public Cloud
Run invocation while application bearer authentication remains enabled. Never
print those values or upload that file. The token is also set in the Windows
user environment for newly launched MCP clients; restart Codex to inherit it.

Google CLI 584.0.0 was installed from the official archive after SHA-256
verification at `%LOCALAPPDATA%\SupplierAtlas\tools\google-cloud-sdk\bin`.
The script accepts `-Gcloud` for another installation. It uses explicit project
and region arguments, not the account's ambient project selection.

`scripts/package_deployment.py` and `deploy/cloudshell.ps1 -BuildAndTest` remain
an automated SCP/SSH fallback. They use an explicit file allowlist and verified
SSH host fingerprint. The original browser directory `/home//m_roshdy_business`
was malformed. CLI SCP uses `/home/m_roshdy_business/supplieratlas-demo.zip`;
Windows PuTTY did not expand a literal `~`. Manual browser upload is obsolete.
`deploy/cloudrun.sh` is the older IAM-private Cloud Shell deployment fallback;
the local `deploy.ps1` is the preferred published-endpoint path.

## Verification evidence and limits

- [Expansion CI run 38743151751](https://github.com/mroshdy91/SupplierAtlas-Demo/actions/runs/38743151751):
  32 tests, deterministic packaging/audit and actual container HTTP checks passed
  at 0.5 CPU / 256 MiB. All 43 published file blobs were compared with the local
  allowlist; no PDF, OCR draft or credential was published.
- Expanded hosted health/version, no-token 401 and all three SDK tools passed.
  Reference SCD rows plus expanded ceiling, fire/smoke ratings and duct hardware
  were verified. The installed native plugin discovered the expanded catalog,
  searched Flow Bar models and retrieved published performance with units,
  conditions, qualified NC and a continuation cursor.
- The compatible backend data release does not change the plugin pin. Its release
  README's initial 42-row qualification is historical; runtime discovery reports
  current coverage. All-family scope includes explicit withheld source exceptions.
- [CI run 38729268196](https://github.com/mroshdy91/SupplierAtlas-Demo/actions/runs/38729268196):
  Historical initial release: 24 tests and container HTTP checks passed. Image size 158,907,817 bytes in Docker
  inspection; this is not a claim about billable registry storage.
- Linux build issues fixed: SQLite copied with atlas ownership; uploaded shell
  source normalized to LF. No original PDF or credential is in the image.
- Hosted health reported the expected catalog; no-token MCP returned 401.
  Official MCP SDK initialized, discovered exactly three tools, called all three,
  and retrieved the reference 6x6 supply row: 100 cfm, 0.046 inH2O, NC19,
  25 cfm per side, throw 6/11 ft with the retained table conditions.
- 19 marketplace generator/release checks passed. The published marketplace
  plugin installed in Codex CLI/app-server 0.162.0-alpha.17.2 on Windows and
  authenticated, with pluginId supplieratlas@atlas-marketplace and three tools.
- Marketplace refresh encountered Windows access-denied errors replacing the
  existing in-use HAPAtlas/Atlas MEP caches. Both existing manifests remained
  present; their release pins are unchanged. SupplierAtlas installation succeeded.
  Do not force-delete unrelated plugin caches to work around file locks.
- No fresh LLM-agent evaluation, other-client live qualification, load test or
  guarantee of future free-tier usage is claimed. Source defects and excluded
  matrix/curve data are documented in SOURCE_ISSUES.md and ALSHARQA_COVERAGE.md.

Further references: [CLI transfers](https://docs.cloud.google.com/shell/docs/using-cloud-shell-with-gcloud-cli),
[Cloud Run registry support](https://docs.cloud.google.com/run/docs/deploying),
[Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing).
