//must be included before any standard header
#include <Python.h>
#include "config.h"


wchar_t *GetWC(const char *c)
{
	size_t cSize = strlen(c) + 1;
	wchar_t* wc = new wchar_t[cSize];
	mbstowcs(wc, c, cSize);

	return wc;
}
/*
* Use simple python code in c++.
* No data exchanging.
*/
UTFUNC(UsePythonInCpp)
{
	debugstream.sink (suDebugSinkConsole::sOnly);
	Py_SetProgramName(GetWC("UsePythonInCpp"));
	Py_Initialize();
	PyRun_SimpleString("a = [1, 2, 3]");
	PyRun_SimpleString("print (a)");
	Py_Finalize();

	return;
}

/*
* Capsulate python function in a C++ function
*/
int great_function_from_python(int a) {
	int res;
	PyObject *pModule, *pFunc;
	PyObject *pArgs, *pValue;
	/* import */
	pModule = PyImport_Import(PyUnicode_FromString("great_module"));
	/* great_module.great_function */
	pFunc = PyObject_GetAttrString(pModule, "great_function");
	/* build args */
	pArgs = PyTuple_New(1);
	PyTuple_SetItem(pArgs, 0, PyLong_FromLong(a));
	/* call */
	pValue = PyObject_CallObject(pFunc, pArgs);
	res = PyLong_AsLong(pValue);
	return res;
}
UTFUNC(UsePythonFuncInCpp)
{
	Py_Initialize();
	printf("%d\n", great_function_from_python(0));
	Py_Finalize();
	system("pause");
}


int main(int argc, char* argv[])
{
	bool state = suUnitTest::gOnly().run ();
	suUnitTest::gOnly().dumpResults (std::cout);

	return state;
}
