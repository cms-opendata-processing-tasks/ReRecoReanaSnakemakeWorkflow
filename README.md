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

The datasets missing and to be processes, compute times taken from runs of 500 events

| Dataset                                      | Record ID | Size RECO | Size RAW  | Events   | Events parent | ~compute hours |
| -------------------------------------------- | --------- | --------- | --------- | -------- | ------------- | -------------- |
| **5.02 Tev PbP**                             | .         | -         | -         | -        | -             | 0.9162 s/e     |
| /PAHighPt/HIRun2013-28Sep2013-v1/RECO        | 24655     | 17.7TB    | 39.2TB    | 36872579 | 222789373     | 56753.5        |
| /PAMuon/HIRun2013-28Sep2013-v1/RECO          | 24658     | 5.5TB     | 15.0TB    | 15445691 | 101376106     | 25800.2        |
| /PAMinBias1/HIRun2013-28Sep2013-v1/RECO      | 24656     | 7.1TB     | 24.9TB    | 4175636  | 20834818      | 5302.5         |
| /PAMinBiasUPC/HIRun2013-28Sep2013-v1/RECO    | 24657     | 7.1TB     | 24.9TB    | 38599905 | 291360429     | 74151.2        |
| /PAMinBias2/HIRun2013-PromptReco-v1/RECO (?) | 24652     | 2.0TB     | 1.1TB (?) | 10709384 | 10709384      | 2725.5         |
| **2.76 TeV pp 2013**                         | -         | -         | -         | -        | -             | 0.39 s/event   |
| /PPPhoton/Run2013A-PromptReco-v1/RECO        | 24644     | 4.2TB     | 2.2TB     | 22410264 | --            | 2427.8         |
| /PPMuon/Run2013A-PromptReco-v1/RECO          | 24643     | 6.1TB     | 3.3TB     | 33397807 | --            | 3618.1         |
| /PPMinBias/Run2013A-PromptReco-v1/RECO       | 24642     | 2.3TB     | 2.0TB     | 34393913 | --            | 3726.0         |
| /PPJet/Run2013A-PromptReco-v1/RECO           | 24645     | 6.4TB     | 3.4TB     | 33716079 | --            | 3652.6         |
| /PPFSQ/Run2013A-PromptReco-v1/RECO           | 24640     | 1.1TB     | 2.1TB     | 13847463 | --            | 1500.1         