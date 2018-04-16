A c++ version SIMP
--------------
This is a c++ version realization of the 99 lines matlab code from Eric et al.[1].

#### Building

This code has the following dependencies: 

- [Eigen](http://eigen.tuxfamily.org)
- [matplotlib-cpp](https://github.com/lava/matplotlib-cpp)[Optional]

Build steps:

1. git clone [path]
2. run ./build-win.sh in the git bash window.
   When finished, the vc solution files are generated and built in the directory of cpp/build.
   You can use visual studio to edit code. 
3. run ./clean.sh to clean build files.


[1] https://link.springer.com/article/10.1007/s00158-010-0594-7
