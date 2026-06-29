EVENTS = config.get("events", 10)

RAW_FILES = open("files.txt").read().strip().split("\n")


rule all:
    input:
        "res/plots/pfcand_pt.png",
        "res/plots/pfcand_eta.png",
        "res/plots/pfcand_phi.png",
        "res/plots/pfcand_etaphi.png",


rule raw2reco:
    output:
        "res/pahighpt_reco.root",
    params:
        events=EVENTS,
        filein=RAW_FILES,
    container:
        "docker://gitlab-registry.cern.ch/cms-cloud/cmssw-docker/cmssw_5_3_8_patch3-slc5_amd64_gcc462:latest"
    shell:
        """
        source /cvmfs/cms.cern.ch/cmsset_default.sh
        scramv1 project CMSSW CMSSW_5_3_8_patch3
        cd CMSSW_5_3_8_patch3/src
        eval `scramv1 runtime -sh`
        mkdir -p $REANA_WORKSPACE/res
        cmsDriver.py --process reRECO --scenario pp \
            -s RAW2DIGI,L1Reco,RECO,USER:EventFilter/HcalRawToDigi/hcallaserhbhehffilter2012_cff.hcallLaser2012Filter \
            --datatier RECO --data --eventcontent RECO \
            --customise Configuration/DataProcessing/RecoTLR.customisePromptHI \
            --conditions GR_P_V43F::All -n {params.events} --no_exec \
            --fileout file:$REANA_WORKSPACE/res/pahighpt_reco.root \
            --python reco_2013A_PAHighPt_hcalFilter.py \
            --filein={params.filein}
        cmsRun reco_2013A_PAHighPt_hcalFilter.py
        """


rule reco2forest:
    input:
        "res/pahighpt_reco.root",
    output:
        "res/HiForest.root",
    container:
        "docker://gitlab-registry.cern.ch/cms-cloud/cmssw-docker-opendata/cmssw_5_3_20-slc6_amd64_gcc472"
    shell:
        """
        source /opt/cms/entrypoint.sh
        cd /code/CMSSW_5_3_20/src/
        eval `scramv1 runtime -sh`
        mkdir -p $REANA_WORKSPACE/scatter $REANA_WORKSPACE/logs $REANA_WORKSPACE/res
        wget https://raw.githubusercontent.com/cms-opendata-validation/HeavyIonDataValidation/53X/runForest_pPb_DATA_53X_OD.py
        python $REANA_WORKSPACE/patch_forest.py runForest_pPb_DATA_53X_OD.py file://$REANA_WORKSPACE/res/pahighpt_reco.root
        cp runForest_pPb_DATA_53X_OD.py /code/CMSSW_5_3_20/src/HeavyIonsAnalysis/JetAnalysis/test/
        cd /code/CMSSW_5_3_20/src/HeavyIonsAnalysis/JetAnalysis/test/
        cmsRun runForest_pPb_DATA_53X_OD.py
        cp HiForest*.root $REANA_WORKSPACE/res/HiForest.root
        """


rule plotforest:
    input:
        "res/HiForest.root",
    output:
        "res/plots/pfcand_pt.png",
        "res/plots/pfcand_eta.png",
        "res/plots/pfcand_phi.png",
        "res/plots/pfcand_etaphi.png",
    container:
        "docker://gitlab-registry.cern.ch/cms-cloud/root-vnc:latest"
    shell:
        """
        chmod 644 $REANA_WORKSPACE/res/HiForest.root
        mkdir -p $REANA_WORKSPACE/res/plots
        python $REANA_WORKSPACE/plot_forest.py \
            $REANA_WORKSPACE/res/HiForest.root \
            $REANA_WORKSPACE/res/plots
        """
