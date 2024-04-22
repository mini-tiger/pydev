# Introduction

Draw a plot for training， it supports two file formats：trainer_state.json and trainer_log.jsonl

trainer_log.jsonl

```json
{"current_steps": 3, "total_steps": 892, "loss": 2.1718, "eval_loss": null, "pre
dict_loss": null, "reward": null, "learning_rate": 0.001, "epoch": 0.01, "percen
tage": 0.34, "elapsed_time": "0:00:20", "remaining_time": "1:41:49"}
{"current_steps": 6, "total_steps": 892, "loss": 1.6447, "eval_loss": null, "pre
dict_loss": null, "reward": null, "learning_rate": 0.000996629213483146, "epoch"
: 0.03, "percentage": 0.67, "elapsed_time": "0:00:38", "remaining_time": "1:34:5
9"}
```

trainer_state.json

```json
{
  "best_metric": null,
  "best_model_checkpoint": null,
  "epoch": 4.0,
  "eval_steps": 500,
  "global_step": 892,
  "is_hyper_param_search": false,
  "is_local_process_zero": true,
  "is_world_process_zero": true,
  "log_history": [
    {
      "epoch": 0.01,
      "learning_rate": 0.001,
      "loss": 2.1718,
      "step": 3
    },
    {
      "epoch": 0.03,
      "learning_rate": 0.000996629213483146,
      "loss": 1.6447,
      "step": 6
    },
    {
      "epoch": 0.04,
      "learning_rate": 0.0009932584269662923,
      "loss": 1.5445,
      "step": 9
    },
    {
      "epoch": 0.05,
      "learning_rate": 0.0009921348314606742,
      "loss": 2.9452,
      "step": 12
    },
```



# How to usage it

1. make a temp directory

   ```
   mkdir lr
   ```

   

2. change to the temp directory and make sub directories and put the file into the sub directories.

   ```
   ./3e-05
   ./3e-05/trainer_state.json
   ./ploting.py
   ./1e-05
   ./1e-05/trainer_state.json
   ./5e-05
   ./5e-05/trainer_state.json
   ```

3. run the xxx_ploting.py script to generate the loss png

   ```shell
   python ./xxx_ploting.py --dir .
   ```

4. there will be a training_loss.png in the current directory.