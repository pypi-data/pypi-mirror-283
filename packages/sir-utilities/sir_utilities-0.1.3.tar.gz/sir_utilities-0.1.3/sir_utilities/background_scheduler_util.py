from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore


def shutdown_scheduler(scheduler: BackgroundScheduler) -> None:
    if len(scheduler.get_jobs()) > 0:
        scheduler.remove_all_jobs()
    if scheduler.running:
        scheduler.shutdown()
