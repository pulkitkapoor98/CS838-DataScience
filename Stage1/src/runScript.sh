#!/bin/bash
# Run Script

python data_clean.py $1 $2
python markup_PositiveEx.py $1 $2
python pre_processing.py $1 $2