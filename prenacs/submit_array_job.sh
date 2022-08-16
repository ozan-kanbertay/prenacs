#!/bin/bash

#SBATCH --job-name=prenacs_job_array
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --constraint=scratch
#SBATCH --time=00:15:00
#SBATCH --mail-type=ALL

# Change the parameters above according to your needs

PATH_TO_CONDA_BIN=/usr/users/kanbertay/software/miniconda3/bin/conda

module purge
eval "$($PATH_TO_CONDA_BIN shell.bash hook)"
conda activate prenacs_slurm_env

# DO NOT CHANGE THE CODE BELOW THIS LINE!
# =======================================
PLUGIN_FILE=$1
PARAMETERS_FILE=$2
INPUT_LIST_FILE=$3
OUTPUT_DIR=$4

prenacs-array-task \
 $PLUGIN_FILE $PARAMETERS_FILE \
 $INPUT_LIST_FILE $SLURM_ARRAY_TASK_ID \
 $OUTPUT_DIR