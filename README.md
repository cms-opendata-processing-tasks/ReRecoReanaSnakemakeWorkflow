# ReReco REANA Snakemake Workflow

A REANA workflow for processing CMS RAW heavy-ion data into RECO format and producing HiForest ntuples with PF candidate plots.

## Pipeline

```
RAW (EOS) → raw2reco (CMSSW 5.3.8) → reco2forest (CMSSW 5.3.20) → plotforest → plots
```

| Step | Rule | Output |
|------|------|--------|
| RAW → RECO | `raw2reco` | `res/pahighpt_reco.root` |
| RECO → HiForest | `reco2forest` | `res/HiForest.root` |
| HiForest → plots | `plotforest` | `res/plots/*.png` |

**Input data:** CMS Open Data HIRun2013 PAHighPt RAW 
**Outputs:** `res/HiForest.root` and four PF candidate plots (pT, η, φ, η-φ)

## Prerequisites

- CERN account with an active Kerberos ticket (`kinit <username>@CERN.CH`)
- REANA access token from [reana.cern.ch](https://reana.cern.ch)

> **Note:** The workflow uses the `htcondorcern` compute backend with Kerberos authentication. To run on a different backend, remove the following lines from `reana.yaml`:
> ```yaml
> compute_backend: htcondorcern
> htcondor_max_runtime: espresso
> kerberos: true
> ```

## Setup

Install the client:

```bash
pip install -r requirements.txt
```

Set your credentials:
CERN reana access token requires approval
```bash
export REANA_SERVER_URL=https://reana.cern.ch
export REANA_ACCESS_TOKEN=<your-token>
```

## Running

```bash
reana-client run -w rereco-reana-snakemake-workflow
```

To change the number of events (default: 10), edit `events` in `reana.yaml`:

```yaml
inputs:
  parameters:
    events: 100
```

## Monitoring

```bash
# Check status
reana-client status -w rereco-reana-snakemake-workflow

# Stream logs
reana-client logs -w rereco-reana-snakemake-workflow
```

Progress can also be viewed at [reana.cern.ch](https://reana.cern.ch).

## Retrieving results

```bash
reana-client download -w rereco-reana-snakemake-workflow
```

## References

- [REANA getting started](https://docs.reana.io/getting-started/first-example/)
- [HSF REANA tutorial](https://hsf-training.github.io/hsf-training-reana-webpage)
