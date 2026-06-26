"""Generate PF candidate plots from a HiForest ROOT file.

Usage: python3 plot_forest.py <HiForest.root> <output_dir>
"""

import sys
import os
import ROOT

hiforest_path = sys.argv[1]
out_dir = sys.argv[2]

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(1)

f = ROOT.TFile.Open(hiforest_path)
if not f or f.IsZombie():
    sys.exit(f"Cannot open {hiforest_path}")

tree = f.Get("pfcandAnalyzer/pfTree")
if not tree:
    sys.exit("pfcandAnalyzer/pfTree not found in HiForest.root")

print(f"pfTree entries: {tree.GetEntries()}")

c = ROOT.TCanvas("c_pt", "PF Candidate pT", 800, 600)
c.SetLogy(1)
h_pt = ROOT.TH1F("h_pt", "PF Candidate p_{T};p_{T} [GeV];Entries", 100, 0, 100)
tree.Draw("pfPt>>h_pt", "", "goff")
h_pt.SetLineColor(ROOT.kBlue + 1)
h_pt.Draw("HIST")
c.SaveAs(os.path.join(out_dir, "pfcand_pt.png"))

c2 = ROOT.TCanvas("c_eta", "PF Candidate eta", 800, 600)
h_eta = ROOT.TH1F("h_eta", "PF Candidate #eta;#eta;Entries", 60, -3, 3)
tree.Draw("pfEta>>h_eta", "", "goff")
h_eta.SetLineColor(ROOT.kRed + 1)
h_eta.Draw("HIST")
c2.SaveAs(os.path.join(out_dir, "pfcand_eta.png"))

c3 = ROOT.TCanvas("c_phi", "PF Candidate phi", 800, 600)
h_phi = ROOT.TH1F("h_phi", "PF Candidate #phi;#phi [rad];Entries", 64, -3.2, 3.2)
tree.Draw("pfPhi>>h_phi", "", "goff")
h_phi.SetLineColor(ROOT.kGreen + 2)
h_phi.Draw("HIST")
c3.SaveAs(os.path.join(out_dir, "pfcand_phi.png"))

c4 = ROOT.TCanvas("c_etaphi", "PF Candidate eta-phi", 800, 600)
h_etaphi = ROOT.TH2F("h_etaphi",
                     "PF Candidate occupancy;#eta;#phi [rad]",
                     60, -3, 3, 64, -3.2, 3.2)
tree.Draw("pfPhi:pfEta>>h_etaphi", "", "goff")
h_etaphi.Draw("COLZ")
c4.SaveAs(os.path.join(out_dir, "pfcand_etaphi.png"))

f.Close()
print(f"Plots saved to {out_dir}")
