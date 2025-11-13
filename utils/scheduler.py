# utils/scheduler.py
import threading, time
import uuid

_jobs = {}
_lock = threading.Lock()
_running = False

def _runner():
    while _running:
        now = time.time()
        to_run = []
        with _lock:
            for jid, job in list(_jobs.items()):
                if job.get("enabled", True) and job.get("next_run", 0) <= now:
                    to_run.append((jid, job))
        for jid, job in to_run:
            try:
                job["callback"](job["city"], jid)
            except Exception as e:
                print(f"Scheduler job {jid} failed: {e}")
            with _lock:
                job["next_run"] = time.time() + job.get("interval_minutes", 60) * 60
        time.sleep(1)

def start_scheduler():
    global _running
    if _running:
        return
    _running = True
    t = threading.Thread(target=_runner, daemon=True)
    t.start()

def stop_scheduler():
    global _running
    _running = False

def add_job(city, interval_minutes, callback):
    jid = str(uuid.uuid4())
    job = {
        "city": city,
        "interval_minutes": interval_minutes,
        "interval": interval_minutes,
        "callback": callback,
        "enabled": True,
        "next_run": time.time() + 5
    }
    with _lock:
        _jobs[jid] = job
    return jid

def remove_job(jid):
    with _lock:
        _jobs.pop(jid, None)

def list_jobs():
    with _lock:
        return {jid: {k:v for k,v in job.items() if k != "callback"} for jid,job in _jobs.items()}
