from chess_ai_lab.tuning.lr_scheduler import StepLRScheduler

scheduler = StepLRScheduler(
    initial_lr=0.01,
    step_size=5,
    gamma=0.5,
)

for epoch in range(15):
    print(
        epoch,
        scheduler.get_lr(epoch),
    )