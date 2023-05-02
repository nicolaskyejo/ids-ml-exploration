DATASET_PATH_AFFIX = "cic2017_dataset/MachineLearningCSV/MachineLearningCVE"
SEED = 0
TEST_SIZE_PROPORTION = 0.33
CACHE_SIZE_MB = 1024
PART_OF_DATA = "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"
# this file doesn't exist in the original dataset, it's just a concatenated result of the several files `head -1
# Wednesday-workingHours.pcap_ISCX.csv > combined.csv && tail -n +2 -q
# Tuesday-WorkingHours.pcap_ISCX.csv Wednesday-workingHours.pcap_ISCX.csv
# Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
# Friday-WorkingHours-Morning.pcap_ISCX.csv Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
# Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv >> combined.csv`
ALL_DATA = "combined_without_monday.csv"
