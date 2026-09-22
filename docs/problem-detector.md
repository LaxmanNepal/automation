## Problem Detector

The Problem Detector is the engineering-alert layer of Laxman OS.

### Checks

- Failed/timed-out GitHub Actions runs from the last 30 days.
- Open issues unchanged for 30+ days.
- Open pull requests unchanged for 14+ days.
- Large open-issue backlogs.
- Dependabot, secret-scanning, and code-scanning alerts when the token has permission.

Permission-gated security endpoints are reported as unavailable rather than treated as evidence that there are no alerts.

### Automation

The scheduled scan creates deduplicated GitHub Issues for priority 70+ findings. A stable fingerprint prevents repeated daily alerts.

It does not merge pull requests, deploy code, publish content, send external messages, or make financial decisions.

For cross-repository scans and security APIs, configure the repository secret GH_PAT with the minimum GitHub permissions needed for the repositories you want to monitor.

### Manual test

Run the workflow manually with create_issues=false first. Review data/problems/latest.json. Enable issue creation only when you want the detector to open issues for high-priority findings.
