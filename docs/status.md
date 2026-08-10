# Current Status

Last Updated

2026-08-09

---

# Completed

Board

- ChessBoard wrapper
- Move generation
- Undo
- FEN

Evaluation

- Feature Registry
- EvaluationSnapshot
- Evaluator
- WeightManager

Search

- Greedy
- Minimax
- AlphaBeta
- Iterative Deepening
- Move Ordering
- Transposition Table

Features

- Material
- Piece Square
- Mobility
- Pawn Structure
- King Safety
- Bishop Pair
- Pawn Shield
- Rook File
- Connected Rooks
- Rook Seventh
- Space
- Knight Outpost
- Bishop Mobility
- Knight Mobility
- Rook Mobility
- Queen Mobility

Evolution

- Match Library
- Selection
- Evolution
- Evolution Runner
- Evolution Strategy
- Evolution Config
- Weight Save
- Generation Save
- JSON Evolution Log
- Resume Foundation

Benchmark

- EPD parser
- EPD loader
- Single position evaluation
- Benchmark runner
- Benchmark result

Texel Tuning

- Parquet Dataset
- TrainingBatch
- In-memory Dataset Cache
- TrainingPosition
- EvaluationSnapshot
- NumPy Feature Vector
- Texel Loss
- Gradient Computation
- Mini-batch SGD
- Validation Loss
- Best Weight Checkpoint
- Resume Training
- Fresh Training
- ReduceLROnPlateau Scheduler
- Early Stopping
- Learning Rate Logging
- Configurable Training
- Configurable Training Dataset Directory
- Training Dataset Builder
- Train / Validation Parquet Generation
- Feature Vector Parquet Serialization
- Feature Registry metadata
- Feature schema validation
- 500,000 position dataset generation
- Train 449,662 positions
- Validation 50,338 positions

---

# Current Training Result

## Dataset

Source

- Lichess/chess-position-evaluations

Current Dataset

- Maximum samples: 500,000
- Minimum Stockfish depth: 20
- CP limit: ±1000
- Train ratio: 0.9
- Seed: 42
- Buffer size: 5,000

Generated Dataset

- Total: 500,000
- Train: 449,662
- Validation: 50,338

Feature Vector

- Feature count: 19
- Stored in Parquet as `feature_values`
- Feature Registry metadata stored in Parquet
- Feature schema hash stored in Parquet

---

## Dataset Loading

Training and validation datasets are loaded into memory
before the first training epoch.

Training Dataset

- 449,662 samples
- Initial load: approximately 6.4–6.8 sec

Validation Dataset

- 50,338 samples
- Current training configuration loads 10,000 validation samples
- Initial load: approximately 0.6–0.7 sec

After loading, the dataset is reused across epochs.

The Parquet files are not reopened for every epoch.

This removes repeated Parquet I/O from the main training loop.

---

## Training Configuration

### Last Recorded Experiment

- Fresh training
- Dataset: `data/training_500k`
- Learning rate: 1.0
- Epochs: 100
- Batch size: 1024
- Training samples: 449,662
- Validation samples: 10,000
- Validation interval: 5
- Train loss interval: 10
- Patience: 10

### Current Code Configuration

The current `PRODUCTION_CONFIG` is:

- Learning rate: 5.0
- Epochs: 100
- Batch size: 4096
- Training samples: unlimited (`None`)
- Validation samples: 10,000
- Validation interval: 5
- Train loss interval: 10
- Patience: 10

The current production configuration is defined in
`src/chess_ai_lab/tuning/config.py`.

The training entry point uses `PRODUCTION_CONFIG`
directly.

Therefore, the last recorded LR=1.0 experiment and the
current default training configuration must be treated
as separate states.

Initial weights for a fresh run are the built-in
evaluation weights.

Training can also resume from
`weights/best_weight.json` when `--fresh` is not specified.

Initial weights

- Built-in evaluation weights
- Training started with `--fresh`

---

## Training Result

Best validation loss

- Validation loss: 0.024605
- Epoch: 100

Final training loss

- Train loss: 0.024462

Final validation loss

- Validation loss: 0.024605

The LR=1.0 experiment improved validation loss
relative to the earlier LR=0.1 experiment.

However, the difference in validation loss alone
does not establish a corresponding increase in playing strength.

---

## Training Performance

Previous implementation

- Dataset was reopened/read during training epochs
- 100 epoch experiments took several minutes

Current implementation

- Dataset loaded once into memory
- Training data reused across epochs
- Dataset processing is effectively removed from epoch timing

Typical epoch benchmark

- Total: approximately 0.03–0.08 sec
- Evaluation: approximately 0.006–0.017 sec
- Gradient: approximately 0.024–0.059 sec
- Optimizer: approximately 0.000–0.002 sec

The current bottleneck is gradient computation,
not Parquet loading.

This makes repeated hyperparameter experiments
substantially cheaper.
---

# Current Training

## Last Recorded Experimental Configuration

The latest recorded training experiment used:

- Dataset: `data/training_500k`
- Epochs: 100
- Batch size: 1024
- Learning rate: 1.0
- Validation interval: 5
- Train loss interval: 10
- Patience: 10
- Fresh training: yes
- Training samples: 449,662
- Validation samples: 10,000

This configuration corresponds to the recorded LR=1.0
training result below.

## Current Code Configuration

The current default `PRODUCTION_CONFIG` is:

- Epochs: 100
- Batch size: 4096
- Learning rate: 5.0
- Validation interval: 5
- Train loss interval: 10
- Patience: 10
- Maximum training samples: unlimited
- Maximum validation samples: 10,000

The current configuration has not yet been associated
with a recorded training result in this document.

Therefore, the LR=5.0 configuration must not be described
as a measured training result until an experiment has
actually been run and recorded.

---

## Learning Rate Experiments

The learning rate is currently being treated as
an experimental variable.

### Recorded Experiments

Previous experiments:

- LR = 0.1
- LR = 0.3
- LR = 1.0

Observed best validation losses:

- LR = 0.1: approximately 0.025093
- LR = 0.3: approximately 0.024733
- LR = 1.0: approximately 0.024605

These results suggest that the previous learning rate
may have been too conservative.

### Current Code Setting

The current `PRODUCTION_CONFIG` uses:

- LR = 5.0

This is a configuration change, not yet a measured
experimental result.

No conclusion should be drawn about LR=5.0 until a
controlled training run has been completed.

Further experiments are required before selecting
a production learning rate.

Validation loss alone must not be treated as proof
of stronger chess play.

---

## Current Best Experimental Result

The best recorded result in the current experiment log
is still the LR=1.0 experiment.

Configuration

- Dataset: `data/training_500k`
- Learning rate: 1.0
- Epochs: 100
- Batch size: 1024
- Fresh training: yes
- Validation samples: 10,000

Result

- Best validation loss: 0.024605
- Best epoch: 100
- Final train loss: 0.024462
- Final validation loss: 0.024605

This is the best recorded experimental result,
not necessarily the result of the current default
training configuration.

The current default configuration uses LR=5.0 and
batch size=4096, but its training result has not yet
been recorded here.

---

# Weight Benchmark

## Historical Baseline

The following results were obtained before the current
500,000-position training experiment.

They must not be interpreted as the benchmark result
of the current LR=1.0 experiment.

---

WAC Benchmark

Dataset

- data/wac.epd
- Limit: 32 positions

## Built-in Weight

Configuration

- Weight: built-in FEATURE_WEIGHTS
- Depth: 2
- Positions: 32

Result

- Solved: 6
- Accuracy: 18.8%
- Nodes: 41,160
- NPS: approximately 1,948

## Trained Weight

Configuration

- Weight: weights_trained.json
- Depth: 2
- Positions: 32

Result

- Solved: 6
- Accuracy: 18.8%
- Nodes: 41,160
- NPS: approximately 1,712

## Trained Weight / Depth 3

Configuration

- Weight: weights_trained.json
- Depth: 3
- Positions: 32

Result

- Solved: 8
- Accuracy: 25.0%
- Nodes: 474,687
- NPS: approximately 1,697
- Time: 279.59 sec

---

# Current Interpretation

The current WAC benchmark does not yet demonstrate
a clear strength improvement from the trained weights.

At depth 2, built-in and trained weights produced the
same 18.8% accuracy on the first 32 WAC positions.

The depth 3 benchmark with trained weights reached 25.0%,
but this result is not directly comparable to the depth 2 results.

The current benchmark sample is too small to draw a strong
conclusion about the quality of the trained weights.

Validation loss improvement is also very small across the
100 epoch run.

Therefore the current results should be treated as an
experimental baseline rather than a validated improvement.

---

# Current Investigation

The following questions are currently under investigation.

1. Does increasing the Training Dataset from 100,000
   to 500,000 positions improve learned evaluation quality?

2. Is the current learning rate of 5.0 appropriate,
   compared with the previously tested values 0.1, 0.3,
   and 1.0?

3. Does increasing the number of epochs continue to
   reduce validation loss meaningfully?

4. Does ReduceLROnPlateau improve convergence compared
   with a fixed learning rate?

5. Does lower Texel validation loss correlate with
   stronger chess playing performance?

6. How much do the learned weights differ from the
   built-in evaluation weights?

7. Does the trained evaluation function improve
   WAC accuracy under identical benchmark conditions?

8. Does the trained evaluation function improve
   self-play results against the built-in evaluation?

9. Is the current validation set sufficiently
   independent from the training data?

10. Does repeated tuning on the same dataset eventually
    overfit the validation set?

11. What dataset size provides a useful trade-off
    between training quality and experiment speed?

12. Does the current in-memory training path preserve
    the mathematical behavior of the previous training
    implementation?

---

# Experiment Infrastructure

The training system is being optimized not only for
training quality but also for experiment throughput.

Current improvements

- Dataset loaded once into memory
- NumPy feature matrices reused across epochs
- Validation dataset cached in memory
- Configurable dataset directory
- Fresh training mode
- Configurable learning rate
- Configurable epoch count
- Configurable validation interval
- Configurable train loss interval
- Early stopping
- ReduceLROnPlateau

Goal

The system should make it inexpensive to run many
controlled experiments with different:

- Dataset sizes
- Learning rates
- Epoch counts
- Batch sizes
- Scheduler settings
- Feature combinations

The priority is to reduce experiment turnaround time
before performing large-scale hyperparameter searches.

---

# Current Constraints

Out of Scope

- NNUE
- Deep Learning
- Reinforcement Learning

---

# AI Instructions

作業前に

architecture.md

invariants.md

を確認する。

推測でコードを書き換えない。

必要なファイルは要求する。

1回の変更では1つの目的のみ扱う。

---

# Next Task

## 1. Validate the Current Training Configuration

Run the current `PRODUCTION_CONFIG` and record its actual
training behavior.

Current configuration:

- Learning rate: 5.0
- Epochs: 100
- Batch size: 4096
- Training samples: unlimited
- Validation samples: 10,000
- Validation interval: 5
- Train loss interval: 10
- Patience: 10

Record:

- Training time
- Best validation loss
- Best epoch
- Final training loss
- Final validation loss
- Final learning rate
- Best weight path
- Final weight path

Do not interpret the result as a strength improvement
until it is compared under identical benchmark conditions.

---

## 2. Controlled Learning Rate Experiment

Compare learning rates under identical conditions.

Candidate learning rates:

- LR = 0.1
- LR = 0.3
- LR = 1.0
- LR = 5.0

For each run:

- Start from the same built-in weights
- Use the same dataset
- Use the same validation set
- Use the same epoch count
- Use the same batch size
- Use the same scheduler configuration

Record:

- Learning rate
- Epoch
- Best validation loss
- Best epoch
- Final validation loss
- Final training loss
- Training time
- Final weights

Only the intended experimental variable should change.

---

## 3. Epoch / Convergence Experiment

After identifying a reasonable learning-rate range,
test whether additional epochs continue to improve
validation loss.

Example:

- 100 epochs
- 200 epochs
- 500 epochs

Record the complete validation-loss trend.

Do not assume that lower validation loss or more epochs
produce stronger chess play.

---

## 4. Independent Playing Strength Evaluation

For each promising trained weight:

- Run WAC benchmark
- Run self-play against the built-in weight
- Use identical search depth
- Use identical benchmark conditions

Record:

- Accuracy
- Nodes
- NPS
- Elapsed time
- Match results

Training loss and playing strength must remain separate
measurements.

---

## 5. Experiment Record

Every significant experiment should record:

- Dataset identifier
- Dataset size
- Feature Registry
- Feature schema hash
- Learning rate
- Epochs
- Batch size
- Validation size
- Scheduler configuration
- Initial weight source
- Best validation loss
- Best epoch
- Final validation loss
- Final training loss
- Training time
- Final weight path
- WAC result
- Self-play result

The goal is to make experiments reproducible
and directly comparable.