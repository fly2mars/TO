#include "../config.h"

#include <Eigen/Dense>
#include <Eigen/Sparse>

//Test Unit
UTFUNC(reshape)
{
	Eigen::MatrixXf M1(4, 3);    // Column-major storage
	M1 << 1, 2, 3,
		4, 5, 6,
		7, 8, 9,
		10,11,12;
	std::cout << M1 << std::endl;
	Eigen::Map<Eigen::RowVectorXf> v1(M1.data(), M1.size());
	std::cout << "v1:" << std::endl << v1 << std::endl;

	Eigen::Map<Eigen::MatrixXf> M2(v1.data(), 3, 4);
	std::cout << "M2:" << std::endl << M2 << std::endl;
}
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
