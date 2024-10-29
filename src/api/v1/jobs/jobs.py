import logging

from apscheduler.schedulers.background import BackgroundScheduler

from src.api.v1.services.counters import CountersSevice
from src.database.db import SessionDep

scheduler = BackgroundScheduler()


def job_increment_counter():
    with SessionDep() as session:
        logging.info("Incrementing job counter")
        CountersSevice.increment_counter(session, "job")


def start_scheduler():
    scheduler.start()
    scheduler.add_job(job_increment_counter, "interval", seconds=3)
    logging.info("Scheduler startedASASSA")


def shutdown_scheduler():
    scheduler.shutdown()
    logging.info("Scheduler shut down")
