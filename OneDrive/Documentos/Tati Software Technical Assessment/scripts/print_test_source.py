import inspect
import importlib
import sys
sys.path.insert(0, r'C:\Users\jabul\OneDrive\Documentos\Tati Software Technical Assessment')
mod = importlib.import_module('todos.tests')
print(inspect.getsource(mod.TodoAPITest.test_delete_todo))
