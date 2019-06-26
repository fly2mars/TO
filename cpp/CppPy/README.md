Using python cod in C++
------------------------

Python is a c lib, so the real python is running in the python*.dll. So you can write a c++ program to run python.


I use Anaconda, the python.h is in the [path]/Anaconda/include. And, the lib is in [path]/Anaconda/libs.

```
//
#include <Python.h>

Py_SetProgramName(argv[0]);
Py_Initialize();
PyRun_SimpleString("print 'Hello Python!'\n");
Py_Finalize();
return 0;
```

#### Reference

1. ÖÐÎÄ https://zhuanlan.zhihu.com/p/20150641
2. https://github.com/luciferz2012/python-c
3. python 3.6 document

