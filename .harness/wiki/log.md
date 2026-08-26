# Business Wiki Log

Append-only decision log. Delivery Approval, Formal Wiki Decision, and Change Retirement Authorization are separate decisions.

## Log record template
- Stable decision ID: `{stable-decision-id}`
- Source change ID: `{change-id}`
- Formal Wiki Decision: `{approved-subset/rejected/deferred/none}`
- Human approval evidence: `{explicit decision}`
- Approved candidate IDs: `{candidate IDs / none}`
- Official Wiki paths: `{canonical paths / none}`
- Source evidence summary: `{artifact and evidence summary}`
- Wiki index synchronized: `{yes/not-applicable}`
- Retirement authorization: `{authorized/not-authorized/not-applicable}`
- Cleanup disposition: `{retired-after-sync/retained}`
- Notes: `{reason}`
