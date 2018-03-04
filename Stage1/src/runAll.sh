# run Command: source runAll.sh
# uncomment below line if you want to generate all data again from raw data
# Data Flow: rawdata ->  cleandata -> (positive examples, unspervised data) -> dictionary of all candidates with 0/1 labels

./runScript.sh 1 308
python ExtractAndSaveFeatures.py
python classificationModels.py
