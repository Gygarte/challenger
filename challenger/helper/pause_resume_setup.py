from multiprocessing import Event


def pause_resume_setup(event: Event) -> None:
    global unpaused
    unpause = event
