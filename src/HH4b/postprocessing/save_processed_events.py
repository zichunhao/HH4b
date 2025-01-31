#!/usr/bin/env python3

import argparse
from pathlib import Path
import pickle
import logging
import logging.config

from HH4b.postprocessing.PostProcess import get_bdt_training_keys, load_process_run3_samples
from HH4b import hh_vars
from HH4b.run_utils import add_bool_arg
from HH4b.log_utils import log_config

# Configure logging
log_config["root"]["level"] = "INFO"
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save processed dataframes"
    )
    parser.add_argument(
        "--templates-tag",
        type=str,
        required=True,
        help="output pickle directory of hist.Hist templates inside the ./templates dir",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="/ceph/cms/store/user/cmantill/bbbb/skimmer/",
        help="tag for input ntuples",
    )
    parser.add_argument(
        "--mass-bins",
        type=int,
        default=10,
        choices=[10, 15, 20],
        help="width of mass bins",
    )
    parser.add_argument(
        "--tag",
        type=str,
        default="24Sep25_v12v2_private_signal",
        help="tag for input ntuples",
    )
    parser.add_argument(
        "--years",
        type=str,
        nargs="+",
        default=hh_vars.years,
        choices=hh_vars.years,
        help="years to postprocess",
    )
    parser.add_argument(
        "--training-years",
        nargs="+",
        choices=hh_vars.years,
        help="years used in training",
    )
    parser.add_argument(
        "--mass",
        type=str,
        default="H2PNetMass",
        choices=["H2Msd", "H2PNetMass"],
        help="mass variable to make template",
    )
    parser.add_argument(
        "--bdt-model",
        type=str,
        default="24May31_lr_0p02_md_8_AK4Away",
        help="BDT model to load",
    )
    parser.add_argument(
        "--bdt-config",
        type=str,
        default="24May31_lr_0p02_md_8_AK4Away",
        help="BDT model to load",
    )
    parser.add_argument(
        "--txbb",
        type=str,
        default="",
        choices=["pnet-legacy", "pnet-v12", "glopart-v2"],
        help="version of TXbb tagger/mass regression to use",
    )
    parser.add_argument(
        "--txbb-wps",
        type=float,
        nargs=2,
        default=[0.975, 0.82],
        help="TXbb Bin 1, Bin 2 WPs",
    )

    parser.add_argument(
        "--bdt-wps",
        type=float,
        nargs=3,
        default=[0.98, 0.88, 0.03],
        help="BDT Bin 1, Bin 2, Fail WPs",
    )
    parser.add_argument(
        "--method",
        type=str,
        default="abcd",
        choices=["abcd", "sideband"],
        help="method for scanning",
    )

    parser.add_argument("--vbf-txbb-wp", type=float, default=0.95, help="TXbb VBF WP")
    parser.add_argument("--vbf-bdt-wp", type=float, default=0.98, help="BDT VBF WP")

    parser.add_argument(
        "--weight-ttbar-bdt", type=float, default=1.0, help="Weight TTbar discriminator on VBF BDT"
    )

    parser.add_argument(
        "--sig-keys",
        type=str,
        nargs="+",
        default=hh_vars.sig_keys,
        choices=hh_vars.sig_keys,
        help="sig keys for which to make templates",
    )
    parser.add_argument("--pt-first", type=float, default=300, help="pt threshold for leading jet")
    parser.add_argument(
        "--pt-second", type=float, default=250, help="pt threshold for subleading jet"
    )

    add_bool_arg(
        parser,
        "bdt-disc",
        default=True,
        help="use BDT discriminant defined as BDT_ggF/VBF = P_ggF/VBF / (P_ggF/VBF + P_bkg), otherwise use P_ggF/VBF",
    )
    add_bool_arg(parser, "bdt-roc", default=False, help="make BDT ROC curve")
    add_bool_arg(parser, "control-plots", default=False, help="make control plots")
    add_bool_arg(parser, "fom-scan", default=False, help="run figure of merit scans")
    add_bool_arg(parser, "fom-scan-bin1", default=True, help="FOM scan for bin 1")
    add_bool_arg(parser, "fom-scan-bin2", default=True, help="FOM scan for bin 2")
    add_bool_arg(parser, "fom-scan-vbf", default=False, help="FOM scan for VBF bin")
    add_bool_arg(parser, "templates", default=True, help="make templates")
    add_bool_arg(parser, "vbf", default=True, help="Add VBF region")
    add_bool_arg(
        parser, "vbf-priority", default=False, help="Prioritize the VBF region over ggF Cat 1"
    )
    add_bool_arg(parser, "blind", default=True, help="Blind the analysis")
    
    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process data for each year
    for year in args.years:
        logger.info(f"Processing year {year}")
        
        # Get BDT training keys
        bdt_training_keys = get_bdt_training_keys(args.bdt_model)
        
        # Process the data
        events, cutflow = load_process_run3_samples(
            args=args,
            year=year,
            bdt_training_keys=bdt_training_keys,
            control_plots=args.control_plots,
            plot_dir=output_dir,
            mass_window=[110, 140] 
        )

        # Save the processed dataframe
        output_file = output_dir / f"processed_events_{year}.pkl"
        with open(output_file, 'wb') as f:
            pickle.dump(events, f)
        logger.info(f"Saved processed events to {output_file}")

        # Save the cutflow
        cutflow_file = output_dir / f"cutflow_{year}.pkl"
        with open(cutflow_file, 'wb') as f:
            pickle.dump(cutflow, f)
        logger.info(f"Saved cutflow to {cutflow_file}")

if __name__ == "__main__":
    main()