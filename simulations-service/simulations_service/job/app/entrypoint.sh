#!/bin/sh


echo "SIMULATION_NUMBER: $SIMULATION_NUMBER"

case "$SIMULATION_NUMBER" in
 1) echo "job1" ;;
 2) echo "job2" ;;
 3) echo "job3" ;;
 4) echo "job4" ;;
 5) echo "job5" ;;
 6) echo "job6" ;;
 7) echo "job7" ;;
 8) echo "job8" ;;
 9) echo "job9" ;;
 10) echo "job10" ;;
 *) echo "job else" ;;
esac

# TODO: Preprocess, download the image file from S3
# python3 preprocess.py

# Remove current input file
rm input_data/lbmPara.json

# Copy the input file based on simulation number(1-10)
cp batch_jobs/lbmPara_$SIMULATION_NUMBER.json input_data/lbmPara.json

cat input_data/lbmPara.json

# Run simulation
make && ./a.out input_data output_data

# Post process the simulation results
python3 python_script.py