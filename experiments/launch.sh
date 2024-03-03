#!/bin/bash

EXP_ID=exp1
SWEEP_ID=sweep1.0
SEED=2024

TRAIN_DATASET=path_to_training_dataset
VALID_DATASET=path_to_validation_dataset
TEST_DATASET=path_to_testing_dataset
OUTPUT_DIR=outputs/${sweep_id}
mkdir -p ${OUTPUT_DIR}

EPOCH=5
BATCH_SIZE=64
LEARNING_RATE=1e-3
VALID_INTERVAL_EPOCHS=1
EARLY_STOP_PATIENCE=3

python main.py \
--exp_id ${EXP_ID} \
--sweep_id ${SWEEP_ID} \
--seed ${SEED} \
\
--train_dataset ${TRAIN_DATASET} \
--valid_dataset ${VALID_DATASET} \
--test_dataset ${TEST_DATASET} \
--output_dir ${OUTPUT_DIR} \
\
--epochs ${EPOCH} \
--batch_size ${BATCH_SIZE} \
--learning_rate ${LEARNING_RATE} \
--valid_interval_epochs ${VALID_INTERVAL_EPOCHS} \
--early_stop_patience ${EARLY_STOP_PATIENCE} \
\
> ${OUTPUT_DIR}/log.out