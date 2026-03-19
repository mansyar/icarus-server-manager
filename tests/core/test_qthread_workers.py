import pytest
from PySide6.QtCore import QObject, Signal, QThread
from icarus_sentinel.ui.workers import GenericWorker

class DummyWorker(GenericWorker):
    def run(self):
        self.finished.emit("Done")

def test_generic_worker_signal(qtbot):
    """Test that GenericWorker emits the finished signal correctly."""
    worker = DummyWorker()
    thread = QThread()
    worker.moveToThread(thread)
    
    thread.started.connect(worker.run)
    worker.finished.connect(thread.quit)
    
    with qtbot.waitSignal(worker.finished, timeout=2000) as blocker:
        thread.start()
        
    assert blocker.args == ["Done"]
    thread.wait(2000)
    if thread.isRunning():
        thread.terminate()
