#include "../config.h"

//Test Unit
UTFUNC(debug2Console)
{
	debugstream.sink (suDebugSinkConsole::sOnly);

	cdebug << "add";

	return;
}

UTFUNC(debug2file)
{
	suDebugSinkFile::sOnly.setFile("r:/debug.txt");
	debugstream.sink(suDebugSinkFile::sOnly);
	cdebug << "debug here...\n";
}


int main(int argc, char* argv[])
{
	bool state = suUnitTest::gOnly().run ();
	suUnitTest::gOnly().dumpResults (std::cout);

	return state;
}
