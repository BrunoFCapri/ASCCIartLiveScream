def log_performance_metrics(fps, processing_time):
    with open("performance_log.txt", "a") as log_file:
        log_file.write(f"FPS: {fps}, Processing Time: {processing_time:.2f} seconds\n")

def calculate_fps(start_time, end_time, frame_count):
    elapsed_time = end_time - start_time
    if elapsed_time > 0:
        return frame_count / elapsed_time
    return 0

def monitor_performance(frame_count, start_time):
    import time
    end_time = time.time()
    fps = calculate_fps(start_time, end_time, frame_count)
    processing_time = end_time - start_time
    log_performance_metrics(fps, processing_time)
    return fps, processing_time