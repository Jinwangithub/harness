# Privacy

Harness is a local workflow bundle. It does not include telemetry, analytics, or a hosted service.

When used, the coding agent reads and may edit files in the active repository according to the user's request and the repository's agent permissions. Change records are written to that repository's `.harness/changes/` directory.

Harness can optionally use external tools configured by the user, including OpenViking MCP. Information sent to those services is governed by the service and configuration the user selected. Harness does not add credentials or configure external services by itself.
