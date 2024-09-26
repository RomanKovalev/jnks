# How to use Part_2

1. [Install Cmake](https://cmake.org/download/)
2. Clone repository
```
git clone git@github.com:RomanKovalev/jnks.git
cd jnks\part_2\build
``` 
3. **cmake .. -G "Visual Studio 16 2019" -A x64** - configure the CMake project for building using Visual Studio 2019 for 64-bit architecture and generate project files.
4. **cmake --build . --config Release** - compile the project and produce the exe file.
```
cd MathClient\Release
.\MathClient.exe

Output:
a + b = 106.4
a - b = -91.6
a * b = 732.6
a / b = 0.0747475
```

## Docker
1. Clone repository
```
git clone git@github.com:RomanKovalev/jnks.git
cd jnks\part_2
``` 
2. **docker build -t math_client .** - build image
3. **docker run --rm math_client** - run container
```
docker run --rm math_client

Output
a + b = 106.4
a - b = -91.6
a * b = 732.6
a / b = 0.0747475
```
