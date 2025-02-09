SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_DIR
PLOT_DIR=$SCRIPT_DIR/roc_curves
pt_cut="250,400,600,1000"
msd_cut="50,250"
DATA_DIR="/eos/uscms/store/user/cmantill/bbbb/skimmer/"

# cd ../../boosted;
cd ../../../../;
HH4b_DIR=$(pwd);
pip install -e .;
cd $HH4b_DIR/src/HH4b/boosted;

process_year() {
    local year=$1;
    echo "Processing year $year";

    if [ $year == "2022" ]; then
        tag="24Sep27_v12v2_private_pre-sel";
    else
        tag="25Feb02_v12v2_private_pre-sel"
    fi

    local plot_dir=$PLOT_DIR/$year;
    mkdir -p $plot_dir;
    python3 ValidateAK8Tagging.py \
    --pt-cut $pt_cut \
    --msd-cut $msd_cut \
    --data-dir $DATA_DIR \
    --year $year \
    --tag $tag \
    --plot-dir $plot_dir;
}

for year in "2022" "2022EE" "2023BPix" "2023"; do
    process_year $year;
done