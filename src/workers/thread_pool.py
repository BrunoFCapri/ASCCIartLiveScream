class ThreadPool:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.tasks = []
        self.threads = []
        self.is_running = True

    def worker(self):
        while self.is_running:
            try:
                task = self.tasks.pop(0)
                task()
            except IndexError:
                continue

    def add_task(self, task):
        self.tasks.append(task)

    def start(self):
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            self.threads.append(thread)

    def stop(self):
        self.is_running = False
        for thread in self.threads:
            thread.join()