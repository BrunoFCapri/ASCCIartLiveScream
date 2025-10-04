"""
Manager de hilos para procesamiento ASCII
"""
import threading
import time
from queue import Queue, Empty
from typing import List, Callable, Any, Dict

class ThreadManager:
    """ULTRA-OPTIMIZADO: Administrador de hilos con mínimo overhead"""
    
    def __init__(self, thread_count: int = 4):
        self.thread_count = thread_count
        self.threads: List[threading.Thread] = []
        # Usar queues con tamaño fijo para mejor rendimiento
        self.task_queue = Queue(maxsize=thread_count * 2)
        self.result_queue = Queue(maxsize=thread_count * 2)
        self.running = False
        
        # Estadísticas optimizadas (acceso atómico)
        self._lock = threading.Lock()
        self.stats = {
            'tasks_completed': 0,
            'total_processing_time': 0.0,
            'average_task_time': 0.0,
            'queue_waits': 0,
            'busy_workers': 0
        }
        
        # Pre-alocar threads para reutilización
        self._thread_pool = []
        self._init_thread_pool()
    
    def _init_thread_pool(self):
        """Pre-inicializa pool de hilos para reutilización"""
        for i in range(self.thread_count):
            thread = threading.Thread(target=self._optimized_worker, args=(i,))
            thread.daemon = True
            self._thread_pool.append(thread)
        
    def start_workers(self):
        """OPTIMIZADO: Inicia hilos pre-configurados"""
        if self.running:
            return  # Ya están ejecutándose
            
        self.running = True
        self.threads = self._thread_pool.copy()
        
        # Iniciar todos los hilos del pool
        for thread in self.threads:
            if not thread.is_alive():
                thread.start()
            
        print(f"⚡ {self.thread_count} hilos ultra-optimizados iniciados")
    
    def stop_workers(self):
        """Detiene todos los hilos trabajadores"""
        self.running = False
        
        # Agregar tareas de terminación
        for _ in range(self.thread_count):
            self.task_queue.put(None)
        
        # Esperar a que terminen
        for thread in self.threads:
            thread.join(timeout=1)
        
        print("🛑 Todos los hilos detenidos")
    
    def _optimized_worker(self, worker_id: int):
        """ULTRA-OPTIMIZADO: Worker con mínimo overhead y batch processing"""
        local_stats = {'completed': 0, 'total_time': 0.0}
        batch_results = []
        batch_size = 5  # Procesar en lotes para reducir sincronización
        
        while self.running:
            try:
                # Intentar obtener tarea sin bloquear mucho tiempo
                task = self.task_queue.get(timeout=0.1)
                if task is None:  # Señal de terminación
                    break
                
                # Incrementar contador de workers ocupados
                with self._lock:
                    self.stats['busy_workers'] += 1
                
                start_time = time.perf_counter()  # Más preciso que time.time()
                
                # Ejecutar tarea
                func, args, task_id = task
                result = func(*args)
                
                processing_time = time.perf_counter() - start_time
                
                # Acumular resultados en lote
                batch_results.append((task_id, result, processing_time))
                local_stats['completed'] += 1
                local_stats['total_time'] += processing_time
                
                # Enviar lote cuando esté lleno o cada cierto tiempo
                if len(batch_results) >= batch_size:
                    self._flush_batch_results(batch_results, local_stats)
                    batch_results.clear()
                    local_stats = {'completed': 0, 'total_time': 0.0}
                
                # Decrementar contador de workers ocupados
                with self._lock:
                    self.stats['busy_workers'] -= 1
                
            except Empty:
                # Sin tareas disponibles - flush resultados pendientes
                if batch_results:
                    self._flush_batch_results(batch_results, local_stats)
                    batch_results.clear()
                    local_stats = {'completed': 0, 'total_time': 0.0}
                continue
            except Exception as e:
                print(f"⚠️ Error en worker {worker_id}: {e}")
                with self._lock:
                    self.stats['busy_workers'] = max(0, self.stats['busy_workers'] - 1)
        
        # Flush final de resultados pendientes
        if batch_results:
            self._flush_batch_results(batch_results, local_stats)
    
    def _flush_batch_results(self, batch_results: List, local_stats: Dict):
        """Envía lote de resultados de manera eficiente"""
        try:
            # Enviar todos los resultados del lote
            for result in batch_results:
                self.result_queue.put_nowait(result)
            
            # Actualizar estadísticas globales de manera atómica
            with self._lock:
                self.stats['tasks_completed'] += local_stats['completed']
                self.stats['total_processing_time'] += local_stats['total_time']
                if self.stats['tasks_completed'] > 0:
                    self.stats['average_task_time'] = (
                        self.stats['total_processing_time'] / 
                        self.stats['tasks_completed']
                    )
        except Exception:
            pass  # Ignorar errores de queue llena
    
    def submit_task(self, func: Callable, args: tuple, task_id: Any = None) -> None:
        """Envía una tarea a la cola de procesamiento"""
        self.task_queue.put((func, args, task_id))
    
    def get_results(self, timeout: float = 0.1) -> List[tuple]:
        """Obtiene todos los resultados disponibles"""
        results = []
        try:
            while True:
                result = self.result_queue.get(timeout=timeout)
                results.append(result)
        except Empty:
            pass
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de rendimiento"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reinicia las estadísticas"""
        self.stats = {
            'tasks_completed': 0,
            'total_processing_time': 0.0,
            'average_task_time': 0.0
        }