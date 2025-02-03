#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $SCRIPT_DIR/HH4b/src/HH4b/postprocessing

OUTPUT_DIR="${SCRIPT_DIR}/events"
mkdir -p ${OUTPUT_DIR}

set -xe;

python3 save_processed_events.py \
--output-dir ${OUTPUT_DIR} \
--templates-tag 24Nov11GloParTv2 \
--tag 24Sep25_v12v2_private_signal \
--mass H2PNetMass \
--txbb glopart-v2 \
--bdt-config v5_glopartv2 \
--bdt-model 24Nov7_v5_glopartv2_rawmass \
--txbb-wps 0.9375 0.7475 \
--bdt-wps 0.9075 0.6375 0.03 \
--vbf \
--vbf-txbb-wp 0.775 \
--vbf-bdt-wp 0.9825 \
--no-fom-scan \
--data-dir /ceph/cms/store/user/cmantill/bbbb/skimmer/ \
--no-vbf-priority \
--pt-second 250 \
--pt-first 300 \
--no-templates