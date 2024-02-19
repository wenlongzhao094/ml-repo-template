#!/bin/bash

BATCH_SIZE=32
LEARNING_RATE=0.01
OUTPUT_DIR=outputs/debug

mkdir -p ${OUTPUT_DIR}

python main.py \
--batch_size ${BATCH_SIZE} \
--learning_rate ${LEARNING_RATE} \
> ${OUTPUT_DIR}/log.out