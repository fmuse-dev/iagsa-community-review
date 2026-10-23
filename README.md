# Integrated AI Governance and Safety Architecture (IAGSA)

A vendor-neutral proposal for end-to-end AI governance and safety, open for community review, testing and further development.

IAGSA connects ten functional domains: institutional purpose, lifecycle evaluation, identity, delegated authority, policy, runtime enforcement, privacy, monitoring, evidence, and intervention/remedy. Its contribution is an integrated responsibility model, explicit **authority–effect–evidence contracts**, six acceptance gates, 25 research requirements and an executable research demonstrator. The broad architectural proposal and the experiments supporting particular mechanisms should be read together.

**Author:** Fardowsa Muse · **Paper and frozen technical evidence:** https://doi.org/10.5281/zenodo.23595879

## Start here

| Your goal | Start with |
| --- | --- |
| Read the proposal | Download the separate manuscript PDF from the DOI record |
| Inspect or reproduce the experiments | [Reviewer guide](docs/REVIEWER_GUIDE.md), then `START_HERE.md` inside the technical ZIP |
| Understand what the findings establish | [Evidence scope and interpretation](docs/EVIDENCE_SCOPE.md) |
| Report a counterexample or propose an extension | [Contribution guide](CONTRIBUTING.md) and issue templates |
| Reuse or redistribute material | [MIT License](LICENSE) and [scope](LICENSE_STATUS.md); separate Zenodo artifacts retain their own terms |

## What this companion provides

This repository is the navigation and discussion companion to the frozen technical package on Zenodo. That package contains the evaluated source code, dependencies, protocols, raw results, historical evidence and verification tools. The manuscript is a separate PDF. Downloading and verifying the package does not require access to the private development repository.

The companion deliberately does not copy the private repository's history or cloud deployment automation. Its preparation tool verifies an exact archive digest before extracting it. Normal companion CI exercises only that tool and its rejection cases; it does not start VMs, call hosted models or reproduce the scientific experiments.

## Findings worth challenging

Experiments demonstrate feasibility of the tested technical composition and expose consequential failure boundaries: prohibited effects through exposed routes, an accepted-work revocation gap, and incorrect model decisions released under valid authorization. Successful protocol execution is not equivalent to successful prevention. Recorded-result verification is not fresh execution or independent replication.

The proposal does not claim demonstrated production readiness, institutional legitimacy, effective human judgment, or comprehensive cross-provider enforcement. These boundaries specify the evidence required to develop the architecture further; they do not discard the completed technical experiments.

Please preserve adverse and incomplete observations when extending the work. Contributions should identify the precise contract, scenario, source revision, resource-state observation and evidence comparison being challenged.
