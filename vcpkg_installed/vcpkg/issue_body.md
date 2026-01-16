Package: nlohmann-json:x64-windows@3.12.0#2

**Host Environment**

- Host: x64-windows
- Compiler: MSVC 19.44.35222.0
- CMake Version: 3.31.10
-    vcpkg-tool version: 2025-12-16-44bb3ce006467fc13ba37ca099f64077b8bbf84d
    vcpkg-scripts version: 389d14fa0e 2026-01-14 (13 hours ago)

**To Reproduce**

`vcpkg install `

**Failure logs**

```
Downloading https://github.com/nlohmann/json/archive/v3.12.0.tar.gz -> nlohmann-json-v3.12.0.tar.gz
warning: Download https://github.com/nlohmann/json/archive/v3.12.0.tar.gz failed -- retrying after 1000ms
warning: Download https://github.com/nlohmann/json/archive/v3.12.0.tar.gz failed -- retrying after 2000ms
warning: Download https://github.com/nlohmann/json/archive/v3.12.0.tar.gz failed -- retrying after 4000ms
Successfully downloaded nlohmann-json-v3.12.0.tar.gz
-- Extracting source D:/A股急速交易系统/vcpkg/downloads/nlohmann-json-v3.12.0.tar.gz
-- Applying patch fix-4736_char8_t.patch
-- Applying patch fix-4742_std_optional.patch
-- Using source at D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean
-- Configuring x64-windows
CMake Error at scripts/cmake/vcpkg_execute_required_process.cmake:127 (message):
    Command failed: D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\ninja-1.13.2-windows\\ninja.exe -v
    Working Directory: D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/vcpkg-parallel-configure
    Error code: 1
    See logs for more information:
      D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-dbg-CMakeCache.txt.log
      D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-rel-CMakeCache.txt.log
      D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-dbg-CMakeConfigureLog.yaml.log
      D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-rel-CMakeConfigureLog.yaml.log
      D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-out.log

Call Stack (most recent call first):
  D:/A股急速交易系统/vcpkg_installed/x64-windows/share/vcpkg-cmake/vcpkg_cmake_configure.cmake:269 (vcpkg_execute_required_process)
  ports/nlohmann-json/portfile.cmake:21 (vcpkg_cmake_configure)
  scripts/ports.cmake:206 (include)



```

<details><summary>D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-dbg-CMakeConfigureLog.yaml.log</summary>

```

---
events:
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineSystem.cmake:205 (message)"
      - "CMakeLists.txt:7 (project)"
    message: |
      The system is: Windows - 10.0.26100 - AMD64
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:17 (message)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:64 (__determine_compiler_id_test)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCXXCompiler.cmake:126 (CMAKE_DETERMINE_COMPILER_ID)"
      - "CMakeLists.txt:7 (project)"
    message: |
      Compiling the CXX compiler identification source file "CMakeCXXCompilerId.cpp" failed.
      Compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe 
      Build flags: /nologo;/DWIN32;/D_WINDOWS;/utf-8;/GR;/EHsc;/MP
      Id flags:  
      
      The output was:
      2
      CMakeCXXCompilerId.cpp
      LINK : fatal error LNK1104: 无法打开文件“kernel32.lib”
      
      
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:17 (message)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:64 (__determine_compiler_id_test)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCXXCompiler.cmake:126 (CMAKE_DETERMINE_COMPILER_ID)"
      - "CMakeLists.txt:7 (project)"
    message: |
      Compiling the CXX compiler identification source file "CMakeCXXCompilerId.cpp" succeeded.
      Compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe 
      Build flags: /nologo;/DWIN32;/D_WINDOWS;/utf-8;/GR;/EHsc;/MP
      Id flags: -c 
      
      The output was:
      0
      CMakeCXXCompilerId.cpp
      
      
      Compilation of the CXX compiler identification source "CMakeCXXCompilerId.cpp" produced "CMakeCXXCompilerId.obj"
      
      The CXX compiler identification is MSVC, found in:
        D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/3.31.10/CompilerIdCXX/CMakeCXXCompilerId.obj
      
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:1289 (message)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:250 (CMAKE_DETERMINE_MSVC_SHOWINCLUDES_PREFIX)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCXXCompiler.cmake:126 (CMAKE_DETERMINE_COMPILER_ID)"
      - "CMakeLists.txt:7 (project)"
    message: |
      Detecting CXX compiler /showIncludes prefix:
        main.c
        注意: 包含文件:  D:\\A股急速交易系统\\vcpkg\\buildtrees\\nlohmann-json\\x64-windows-dbg\\CMakeFiles\\ShowIncludes\\foo.h
        
      Found prefix "注意: 包含文件:  "
  -
    kind: "try_compile-v1"
    backtrace:
...
Skipped 8 lines
...
    cmakeVariables:
      CMAKE_CXX_FLAGS: " /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP "
      CMAKE_CXX_FLAGS_DEBUG: "/MDd /Z7 /Ob0 /Od /RTC1 "
      CMAKE_CXX_SCAN_FOR_MODULES: "OFF"
      CMAKE_EXE_LINKER_FLAGS: "/machine:x64"
      CMAKE_MSVC_DEBUG_INFORMATION_FORMAT: ""
      CMAKE_MSVC_RUNTIME_LIBRARY: "MultiThreaded$<$<CONFIG:Debug>:Debug>$<$<STREQUAL:dynamic,dynamic>:DLL>"
      VCPKG_CHAINLOAD_TOOLCHAIN_FILE: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/scripts/toolchains/windows.cmake"
      VCPKG_CRT_LINKAGE: "dynamic"
      VCPKG_CXX_FLAGS: ""
      VCPKG_CXX_FLAGS_DEBUG: ""
      VCPKG_CXX_FLAGS_RELEASE: ""
      VCPKG_C_FLAGS: ""
      VCPKG_C_FLAGS_DEBUG: ""
      VCPKG_C_FLAGS_RELEASE: ""
      VCPKG_INSTALLED_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg_installed"
      VCPKG_LINKER_FLAGS: ""
      VCPKG_LINKER_FLAGS_DEBUG: ""
      VCPKG_LINKER_FLAGS_RELEASE: ""
      VCPKG_PLATFORM_TOOLSET: "v143"
      VCPKG_PREFER_SYSTEM_LIBS: "OFF"
      VCPKG_SET_CHARSET_FLAG: "ON"
      VCPKG_TARGET_ARCHITECTURE: "x64"
      VCPKG_TARGET_TRIPLET: "x64-windows"
      Z_VCPKG_ROOT_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg"
    buildResult:
      variable: "CMAKE_CXX_ABI_COMPILED"
      cached: true
      stdout: |
        Change Dir: 'D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/CMakeScratch/TryCompile-hf9jyp'
        
        Run Build Command(s): D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\ninja-1.13.2-windows\\ninja.exe -v cmTC_96637
        [1/2] C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\cl.exe  /nologo /TP   /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP   /MDd /Z7 /Ob0 /Od /RTC1  -MDd /showIncludes /FoCMakeFiles\\cmTC_96637.dir\\CMakeCXXCompilerABI.cpp.obj /FdCMakeFiles\\cmTC_96637.dir\\ /FS -c D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\share\\cmake-3.31\\Modules\\CMakeCXXCompilerABI.cpp
        [2/2] C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_96637.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_96637.dir\\CMakeCXXCompilerABI.cpp.obj  /out:cmTC_96637.exe /implib:cmTC_96637.lib /pdb:cmTC_96637.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        FAILED: [code=4294967295] cmTC_96637.exe 
        C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_96637.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_96637.dir\\CMakeCXXCompilerABI.cpp.obj  /out:cmTC_96637.exe /implib:cmTC_96637.lib /pdb:cmTC_96637.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        RC Pass 1: command "rc /fo CMakeFiles\\cmTC_96637.dir/manifest.res CMakeFiles\\cmTC_96637.dir/manifest.rc" failed (exit code 0) with the following output:
        no such file or directory
        ninja: build stopped: subcommand failed.
        
      exitCode: -1
  -
    kind: "try_compile-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeTestCXXCompiler.cmake:56 (try_compile)"
      - "CMakeLists.txt:7 (project)"
    checks:
      - "Check for working CXX compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe"
    directories:
      source: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/CMakeScratch/TryCompile-669b6l"
      binary: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/CMakeScratch/TryCompile-669b6l"
    cmakeVariables:
      CMAKE_CXX_FLAGS: " /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP "
      CMAKE_CXX_FLAGS_DEBUG: "/MDd /Z7 /Ob0 /Od /RTC1 "
      CMAKE_CXX_SCAN_FOR_MODULES: "OFF"
      CMAKE_EXE_LINKER_FLAGS: "/machine:x64"
      CMAKE_MSVC_DEBUG_INFORMATION_FORMAT: ""
      CMAKE_MSVC_RUNTIME_LIBRARY: "MultiThreaded$<$<CONFIG:Debug>:Debug>$<$<STREQUAL:dynamic,dynamic>:DLL>"
      VCPKG_CHAINLOAD_TOOLCHAIN_FILE: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/scripts/toolchains/windows.cmake"
      VCPKG_CRT_LINKAGE: "dynamic"
      VCPKG_CXX_FLAGS: ""
      VCPKG_CXX_FLAGS_DEBUG: ""
      VCPKG_CXX_FLAGS_RELEASE: ""
      VCPKG_C_FLAGS: ""
      VCPKG_C_FLAGS_DEBUG: ""
      VCPKG_C_FLAGS_RELEASE: ""
      VCPKG_INSTALLED_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg_installed"
      VCPKG_LINKER_FLAGS: ""
      VCPKG_LINKER_FLAGS_DEBUG: ""
      VCPKG_LINKER_FLAGS_RELEASE: ""
      VCPKG_PLATFORM_TOOLSET: "v143"
      VCPKG_PREFER_SYSTEM_LIBS: "OFF"
      VCPKG_SET_CHARSET_FLAG: "ON"
      VCPKG_TARGET_ARCHITECTURE: "x64"
      VCPKG_TARGET_TRIPLET: "x64-windows"
      Z_VCPKG_ROOT_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg"
    buildResult:
      variable: "CMAKE_CXX_COMPILER_WORKS"
      cached: true
      stdout: |
        Change Dir: 'D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/CMakeScratch/TryCompile-669b6l'
        
        Run Build Command(s): D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\ninja-1.13.2-windows\\ninja.exe -v cmTC_d74e9
        [1/2] C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\cl.exe  /nologo /TP   /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP   /MDd /Z7 /Ob0 /Od /RTC1  -MDd /showIncludes /FoCMakeFiles\\cmTC_d74e9.dir\\testCXXCompiler.cxx.obj /FdCMakeFiles\\cmTC_d74e9.dir\\ /FS -c D:\\A股急速交易系统\\vcpkg\\buildtrees\\nlohmann-json\\x64-windows-dbg\\CMakeFiles\\CMakeScratch\\TryCompile-669b6l\\testCXXCompiler.cxx
        [2/2] C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_d74e9.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_d74e9.dir\\testCXXCompiler.cxx.obj  /out:cmTC_d74e9.exe /implib:cmTC_d74e9.lib /pdb:cmTC_d74e9.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        FAILED: [code=4294967295] cmTC_d74e9.exe 
        C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_d74e9.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_d74e9.dir\\testCXXCompiler.cxx.obj  /out:cmTC_d74e9.exe /implib:cmTC_d74e9.lib /pdb:cmTC_d74e9.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        RC Pass 1: command "rc /fo CMakeFiles\\cmTC_d74e9.dir/manifest.res CMakeFiles\\cmTC_d74e9.dir/manifest.rc" failed (exit code 0) with the following output:
        no such file or directory
        ninja: build stopped: subcommand failed.
        
      exitCode: -1
...
```
</details>

<details><summary>D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-rel-CMakeConfigureLog.yaml.log</summary>

```

---
events:
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineSystem.cmake:205 (message)"
      - "CMakeLists.txt:7 (project)"
    message: |
      The system is: Windows - 10.0.26100 - AMD64
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:17 (message)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:64 (__determine_compiler_id_test)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCXXCompiler.cmake:126 (CMAKE_DETERMINE_COMPILER_ID)"
      - "CMakeLists.txt:7 (project)"
    message: |
      Compiling the CXX compiler identification source file "CMakeCXXCompilerId.cpp" failed.
      Compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe 
      Build flags: /nologo;/DWIN32;/D_WINDOWS;/utf-8;/GR;/EHsc;/MP
      Id flags:  
      
      The output was:
      2
      CMakeCXXCompilerId.cpp
      LINK : fatal error LNK1104: 无法打开文件“kernel32.lib”
      
      
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:17 (message)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:64 (__determine_compiler_id_test)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCXXCompiler.cmake:126 (CMAKE_DETERMINE_COMPILER_ID)"
      - "CMakeLists.txt:7 (project)"
    message: |
      Compiling the CXX compiler identification source file "CMakeCXXCompilerId.cpp" succeeded.
      Compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe 
      Build flags: /nologo;/DWIN32;/D_WINDOWS;/utf-8;/GR;/EHsc;/MP
      Id flags: -c 
      
      The output was:
      0
      CMakeCXXCompilerId.cpp
      
      
      Compilation of the CXX compiler identification source "CMakeCXXCompilerId.cpp" produced "CMakeCXXCompilerId.obj"
      
      The CXX compiler identification is MSVC, found in:
        D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/CMakeFiles/3.31.10/CompilerIdCXX/CMakeCXXCompilerId.obj
      
  -
    kind: "message-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:1289 (message)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCompilerId.cmake:250 (CMAKE_DETERMINE_MSVC_SHOWINCLUDES_PREFIX)"
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeDetermineCXXCompiler.cmake:126 (CMAKE_DETERMINE_COMPILER_ID)"
      - "CMakeLists.txt:7 (project)"
    message: |
      Detecting CXX compiler /showIncludes prefix:
        main.c
        注意: 包含文件:  D:\\A股急速交易系统\\vcpkg\\buildtrees\\nlohmann-json\\x64-windows-rel\\CMakeFiles\\ShowIncludes\\foo.h
        
      Found prefix "注意: 包含文件:  "
  -
    kind: "try_compile-v1"
    backtrace:
...
Skipped 8 lines
...
    cmakeVariables:
      CMAKE_CXX_FLAGS: " /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP "
      CMAKE_CXX_FLAGS_DEBUG: "/MDd /Z7 /Ob0 /Od /RTC1 "
      CMAKE_CXX_SCAN_FOR_MODULES: "OFF"
      CMAKE_EXE_LINKER_FLAGS: "/machine:x64"
      CMAKE_MSVC_DEBUG_INFORMATION_FORMAT: ""
      CMAKE_MSVC_RUNTIME_LIBRARY: "MultiThreaded$<$<CONFIG:Debug>:Debug>$<$<STREQUAL:dynamic,dynamic>:DLL>"
      VCPKG_CHAINLOAD_TOOLCHAIN_FILE: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/scripts/toolchains/windows.cmake"
      VCPKG_CRT_LINKAGE: "dynamic"
      VCPKG_CXX_FLAGS: ""
      VCPKG_CXX_FLAGS_DEBUG: ""
      VCPKG_CXX_FLAGS_RELEASE: ""
      VCPKG_C_FLAGS: ""
      VCPKG_C_FLAGS_DEBUG: ""
      VCPKG_C_FLAGS_RELEASE: ""
      VCPKG_INSTALLED_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg_installed"
      VCPKG_LINKER_FLAGS: ""
      VCPKG_LINKER_FLAGS_DEBUG: ""
      VCPKG_LINKER_FLAGS_RELEASE: ""
      VCPKG_PLATFORM_TOOLSET: "v143"
      VCPKG_PREFER_SYSTEM_LIBS: "OFF"
      VCPKG_SET_CHARSET_FLAG: "ON"
      VCPKG_TARGET_ARCHITECTURE: "x64"
      VCPKG_TARGET_TRIPLET: "x64-windows"
      Z_VCPKG_ROOT_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg"
    buildResult:
      variable: "CMAKE_CXX_ABI_COMPILED"
      cached: true
      stdout: |
        Change Dir: 'D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/CMakeFiles/CMakeScratch/TryCompile-3l5ope'
        
        Run Build Command(s): D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\ninja-1.13.2-windows\\ninja.exe -v cmTC_90922
        [1/2] C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\cl.exe  /nologo /TP   /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP   /MDd /Z7 /Ob0 /Od /RTC1  -MDd /showIncludes /FoCMakeFiles\\cmTC_90922.dir\\CMakeCXXCompilerABI.cpp.obj /FdCMakeFiles\\cmTC_90922.dir\\ /FS -c D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\share\\cmake-3.31\\Modules\\CMakeCXXCompilerABI.cpp
        [2/2] C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_90922.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_90922.dir\\CMakeCXXCompilerABI.cpp.obj  /out:cmTC_90922.exe /implib:cmTC_90922.lib /pdb:cmTC_90922.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        FAILED: [code=4294967295] cmTC_90922.exe 
        C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_90922.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_90922.dir\\CMakeCXXCompilerABI.cpp.obj  /out:cmTC_90922.exe /implib:cmTC_90922.lib /pdb:cmTC_90922.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        RC Pass 1: command "rc /fo CMakeFiles\\cmTC_90922.dir/manifest.res CMakeFiles\\cmTC_90922.dir/manifest.rc" failed (exit code 0) with the following output:
        no such file or directory
        ninja: build stopped: subcommand failed.
        
      exitCode: -1
  -
    kind: "try_compile-v1"
    backtrace:
      - "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeTestCXXCompiler.cmake:56 (try_compile)"
      - "CMakeLists.txt:7 (project)"
    checks:
      - "Check for working CXX compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe"
    directories:
      source: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/CMakeFiles/CMakeScratch/TryCompile-aghtba"
      binary: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/CMakeFiles/CMakeScratch/TryCompile-aghtba"
    cmakeVariables:
      CMAKE_CXX_FLAGS: " /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP "
      CMAKE_CXX_FLAGS_DEBUG: "/MDd /Z7 /Ob0 /Od /RTC1 "
      CMAKE_CXX_SCAN_FOR_MODULES: "OFF"
      CMAKE_EXE_LINKER_FLAGS: "/machine:x64"
      CMAKE_MSVC_DEBUG_INFORMATION_FORMAT: ""
      CMAKE_MSVC_RUNTIME_LIBRARY: "MultiThreaded$<$<CONFIG:Debug>:Debug>$<$<STREQUAL:dynamic,dynamic>:DLL>"
      VCPKG_CHAINLOAD_TOOLCHAIN_FILE: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg/scripts/toolchains/windows.cmake"
      VCPKG_CRT_LINKAGE: "dynamic"
      VCPKG_CXX_FLAGS: ""
      VCPKG_CXX_FLAGS_DEBUG: ""
      VCPKG_CXX_FLAGS_RELEASE: ""
      VCPKG_C_FLAGS: ""
      VCPKG_C_FLAGS_DEBUG: ""
      VCPKG_C_FLAGS_RELEASE: ""
      VCPKG_INSTALLED_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg_installed"
      VCPKG_LINKER_FLAGS: ""
      VCPKG_LINKER_FLAGS_DEBUG: ""
      VCPKG_LINKER_FLAGS_RELEASE: ""
      VCPKG_PLATFORM_TOOLSET: "v143"
      VCPKG_PREFER_SYSTEM_LIBS: "OFF"
      VCPKG_SET_CHARSET_FLAG: "ON"
      VCPKG_TARGET_ARCHITECTURE: "x64"
      VCPKG_TARGET_TRIPLET: "x64-windows"
      Z_VCPKG_ROOT_DIR: "D:/A\u80a1\u6025\u901f\u4ea4\u6613\u7cfb\u7edf/vcpkg"
    buildResult:
      variable: "CMAKE_CXX_COMPILER_WORKS"
      cached: true
      stdout: |
        Change Dir: 'D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/CMakeFiles/CMakeScratch/TryCompile-aghtba'
        
        Run Build Command(s): D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\ninja-1.13.2-windows\\ninja.exe -v cmTC_06668
        [1/2] C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\cl.exe  /nologo /TP   /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP   /MDd /Z7 /Ob0 /Od /RTC1  -MDd /showIncludes /FoCMakeFiles\\cmTC_06668.dir\\testCXXCompiler.cxx.obj /FdCMakeFiles\\cmTC_06668.dir\\ /FS -c D:\\A股急速交易系统\\vcpkg\\buildtrees\\nlohmann-json\\x64-windows-rel\\CMakeFiles\\CMakeScratch\\TryCompile-aghtba\\testCXXCompiler.cxx
        [2/2] C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_06668.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_06668.dir\\testCXXCompiler.cxx.obj  /out:cmTC_06668.exe /implib:cmTC_06668.lib /pdb:cmTC_06668.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        FAILED: [code=4294967295] cmTC_06668.exe 
        C:\\WINDOWS\\system32\\cmd.exe /C "cd . && D:\\A股急速交易系统\\vcpkg\\downloads\\tools\\cmake-3.31.10-windows\\cmake-3.31.10-windows-x86_64\\bin\\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\\cmTC_06668.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\\BuildTools\\VC\\Tools\\MSVC\\14.44.35207\\bin\\Hostx64\\x64\\link.exe /nologo CMakeFiles\\cmTC_06668.dir\\testCXXCompiler.cxx.obj  /out:cmTC_06668.exe /implib:cmTC_06668.lib /pdb:cmTC_06668.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
        RC Pass 1: command "rc /fo CMakeFiles\\cmTC_06668.dir/manifest.res CMakeFiles\\cmTC_06668.dir/manifest.rc" failed (exit code 0) with the following output:
        no such file or directory
        ninja: build stopped: subcommand failed.
        
      exitCode: -1
...
```
</details>

<details><summary>D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-out.log</summary>

```
[1/2] "D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" -E chdir ".." "D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" "D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean" "-G" "Ninja" "-DCMAKE_BUILD_TYPE=Release" "-DCMAKE_INSTALL_PREFIX=D:/A股急速交易系统/vcpkg/packages/nlohmann-json_x64-windows" "-DFETCHCONTENT_FULLY_DISCONNECTED=ON" "-DJSON_Diagnostics=OFF" "-DJSON_Install=ON" "-DJSON_MultipleHeaders=ON" "-DJSON_BuildTests=OFF" "-DJSON_ImplicitConversions=ON" "-DCMAKE_MAKE_PROGRAM=D:\A股急速交易系统\vcpkg\downloads\tools\ninja-1.13.2-windows\ninja.exe" "-DBUILD_SHARED_LIBS=ON" "-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/toolchains/windows.cmake" "-DVCPKG_TARGET_TRIPLET=x64-windows" "-DVCPKG_SET_CHARSET_FLAG=ON" "-DVCPKG_PLATFORM_TOOLSET=v143" "-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY=ON" "-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=TRUE" "-DCMAKE_VERBOSE_MAKEFILE=ON" "-DVCPKG_APPLOCAL_DEPS=OFF" "-DCMAKE_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/buildsystems/vcpkg.cmake" "-DCMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION=ON" "-DVCPKG_CXX_FLAGS=" "-DVCPKG_CXX_FLAGS_RELEASE=" "-DVCPKG_CXX_FLAGS_DEBUG=" "-DVCPKG_C_FLAGS=" "-DVCPKG_C_FLAGS_RELEASE=" "-DVCPKG_C_FLAGS_DEBUG=" "-DVCPKG_CRT_LINKAGE=dynamic" "-DVCPKG_LINKER_FLAGS=" "-DVCPKG_LINKER_FLAGS_RELEASE=" "-DVCPKG_LINKER_FLAGS_DEBUG=" "-DVCPKG_TARGET_ARCHITECTURE=x64" "-DCMAKE_INSTALL_LIBDIR:STRING=lib" "-DCMAKE_INSTALL_BINDIR:STRING=bin" "-D_VCPKG_ROOT_DIR=D:/A股急速交易系统/vcpkg" "-D_VCPKG_INSTALLED_DIR=D:/A股急速交易系统/vcpkg_installed" "-DVCPKG_MANIFEST_INSTALL=OFF"
FAILED: [code=1] ../CMakeCache.txt 
"D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" -E chdir ".." "D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" "D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean" "-G" "Ninja" "-DCMAKE_BUILD_TYPE=Release" "-DCMAKE_INSTALL_PREFIX=D:/A股急速交易系统/vcpkg/packages/nlohmann-json_x64-windows" "-DFETCHCONTENT_FULLY_DISCONNECTED=ON" "-DJSON_Diagnostics=OFF" "-DJSON_Install=ON" "-DJSON_MultipleHeaders=ON" "-DJSON_BuildTests=OFF" "-DJSON_ImplicitConversions=ON" "-DCMAKE_MAKE_PROGRAM=D:\A股急速交易系统\vcpkg\downloads\tools\ninja-1.13.2-windows\ninja.exe" "-DBUILD_SHARED_LIBS=ON" "-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/toolchains/windows.cmake" "-DVCPKG_TARGET_TRIPLET=x64-windows" "-DVCPKG_SET_CHARSET_FLAG=ON" "-DVCPKG_PLATFORM_TOOLSET=v143" "-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY=ON" "-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=TRUE" "-DCMAKE_VERBOSE_MAKEFILE=ON" "-DVCPKG_APPLOCAL_DEPS=OFF" "-DCMAKE_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/buildsystems/vcpkg.cmake" "-DCMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION=ON" "-DVCPKG_CXX_FLAGS=" "-DVCPKG_CXX_FLAGS_RELEASE=" "-DVCPKG_CXX_FLAGS_DEBUG=" "-DVCPKG_C_FLAGS=" "-DVCPKG_C_FLAGS_RELEASE=" "-DVCPKG_C_FLAGS_DEBUG=" "-DVCPKG_CRT_LINKAGE=dynamic" "-DVCPKG_LINKER_FLAGS=" "-DVCPKG_LINKER_FLAGS_RELEASE=" "-DVCPKG_LINKER_FLAGS_DEBUG=" "-DVCPKG_TARGET_ARCHITECTURE=x64" "-DCMAKE_INSTALL_LIBDIR:STRING=lib" "-DCMAKE_INSTALL_BINDIR:STRING=bin" "-D_VCPKG_ROOT_DIR=D:/A股急速交易系统/vcpkg" "-D_VCPKG_INSTALLED_DIR=D:/A股急速交易系统/vcpkg_installed" "-DVCPKG_MANIFEST_INSTALL=OFF"
-- The CXX compiler identification is MSVC 19.44.35222.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - failed
-- Check for working CXX compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe
-- Check for working CXX compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe - broken
...
Skipped 14 lines
...
    FAILED: [code=4294967295] cmTC_06668.exe 
    C:\WINDOWS\system32\cmd.exe /C "cd . && D:\A股急速交易系统\vcpkg\downloads\tools\cmake-3.31.10-windows\cmake-3.31.10-windows-x86_64\bin\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\cmTC_06668.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\BuildTools\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\link.exe /nologo CMakeFiles\cmTC_06668.dir\testCXXCompiler.cxx.obj  /out:cmTC_06668.exe /implib:cmTC_06668.lib /pdb:cmTC_06668.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
    RC Pass 1: command "rc /fo CMakeFiles\cmTC_06668.dir/manifest.res CMakeFiles\cmTC_06668.dir/manifest.rc" failed (exit code 0) with the following output:
    no such file or directory
    ninja: build stopped: subcommand failed.
    
    

  

  CMake will not be able to correctly generate this project.
Call Stack (most recent call first):
  CMakeLists.txt:7 (project)


-- Configuring incomplete, errors occurred!
[2/2] "D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" -E chdir "../../x64-windows-dbg" "D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" "D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean" "-G" "Ninja" "-DCMAKE_BUILD_TYPE=Debug" "-DCMAKE_INSTALL_PREFIX=D:/A股急速交易系统/vcpkg/packages/nlohmann-json_x64-windows/debug" "-DFETCHCONTENT_FULLY_DISCONNECTED=ON" "-DJSON_Diagnostics=OFF" "-DJSON_Install=ON" "-DJSON_MultipleHeaders=ON" "-DJSON_BuildTests=OFF" "-DJSON_ImplicitConversions=ON" "-DCMAKE_MAKE_PROGRAM=D:\A股急速交易系统\vcpkg\downloads\tools\ninja-1.13.2-windows\ninja.exe" "-DBUILD_SHARED_LIBS=ON" "-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/toolchains/windows.cmake" "-DVCPKG_TARGET_TRIPLET=x64-windows" "-DVCPKG_SET_CHARSET_FLAG=ON" "-DVCPKG_PLATFORM_TOOLSET=v143" "-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY=ON" "-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=TRUE" "-DCMAKE_VERBOSE_MAKEFILE=ON" "-DVCPKG_APPLOCAL_DEPS=OFF" "-DCMAKE_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/buildsystems/vcpkg.cmake" "-DCMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION=ON" "-DVCPKG_CXX_FLAGS=" "-DVCPKG_CXX_FLAGS_RELEASE=" "-DVCPKG_CXX_FLAGS_DEBUG=" "-DVCPKG_C_FLAGS=" "-DVCPKG_C_FLAGS_RELEASE=" "-DVCPKG_C_FLAGS_DEBUG=" "-DVCPKG_CRT_LINKAGE=dynamic" "-DVCPKG_LINKER_FLAGS=" "-DVCPKG_LINKER_FLAGS_RELEASE=" "-DVCPKG_LINKER_FLAGS_DEBUG=" "-DVCPKG_TARGET_ARCHITECTURE=x64" "-DCMAKE_INSTALL_LIBDIR:STRING=lib" "-DCMAKE_INSTALL_BINDIR:STRING=bin" "-D_VCPKG_ROOT_DIR=D:/A股急速交易系统/vcpkg" "-D_VCPKG_INSTALLED_DIR=D:/A股急速交易系统/vcpkg_installed" "-DVCPKG_MANIFEST_INSTALL=OFF"
FAILED: [code=1] ../../x64-windows-dbg/CMakeCache.txt 
"D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" -E chdir "../../x64-windows-dbg" "D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe" "D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean" "-G" "Ninja" "-DCMAKE_BUILD_TYPE=Debug" "-DCMAKE_INSTALL_PREFIX=D:/A股急速交易系统/vcpkg/packages/nlohmann-json_x64-windows/debug" "-DFETCHCONTENT_FULLY_DISCONNECTED=ON" "-DJSON_Diagnostics=OFF" "-DJSON_Install=ON" "-DJSON_MultipleHeaders=ON" "-DJSON_BuildTests=OFF" "-DJSON_ImplicitConversions=ON" "-DCMAKE_MAKE_PROGRAM=D:\A股急速交易系统\vcpkg\downloads\tools\ninja-1.13.2-windows\ninja.exe" "-DBUILD_SHARED_LIBS=ON" "-DVCPKG_CHAINLOAD_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/toolchains/windows.cmake" "-DVCPKG_TARGET_TRIPLET=x64-windows" "-DVCPKG_SET_CHARSET_FLAG=ON" "-DVCPKG_PLATFORM_TOOLSET=v143" "-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON" "-DCMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY=ON" "-DCMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP=TRUE" "-DCMAKE_VERBOSE_MAKEFILE=ON" "-DVCPKG_APPLOCAL_DEPS=OFF" "-DCMAKE_TOOLCHAIN_FILE=D:/A股急速交易系统/vcpkg/scripts/buildsystems/vcpkg.cmake" "-DCMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION=ON" "-DVCPKG_CXX_FLAGS=" "-DVCPKG_CXX_FLAGS_RELEASE=" "-DVCPKG_CXX_FLAGS_DEBUG=" "-DVCPKG_C_FLAGS=" "-DVCPKG_C_FLAGS_RELEASE=" "-DVCPKG_C_FLAGS_DEBUG=" "-DVCPKG_CRT_LINKAGE=dynamic" "-DVCPKG_LINKER_FLAGS=" "-DVCPKG_LINKER_FLAGS_RELEASE=" "-DVCPKG_LINKER_FLAGS_DEBUG=" "-DVCPKG_TARGET_ARCHITECTURE=x64" "-DCMAKE_INSTALL_LIBDIR:STRING=lib" "-DCMAKE_INSTALL_BINDIR:STRING=bin" "-D_VCPKG_ROOT_DIR=D:/A股急速交易系统/vcpkg" "-D_VCPKG_INSTALLED_DIR=D:/A股急速交易系统/vcpkg_installed" "-DVCPKG_MANIFEST_INSTALL=OFF"
-- The CXX compiler identification is MSVC 19.44.35222.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - failed
-- Check for working CXX compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe
-- Check for working CXX compiler: C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe - broken
CMake Error at D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31/Modules/CMakeTestCXXCompiler.cmake:73 (message):
  The C++ compiler

    "C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe"

  is not able to compile a simple test program.

  It fails with the following output:

    Change Dir: 'D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/CMakeScratch/TryCompile-669b6l'
    
    Run Build Command(s): D:\A股急速交易系统\vcpkg\downloads\tools\ninja-1.13.2-windows\ninja.exe -v cmTC_d74e9
    [1/2] C:\BuildTools\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\cl.exe  /nologo /TP   /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP   /MDd /Z7 /Ob0 /Od /RTC1  -MDd /showIncludes /FoCMakeFiles\cmTC_d74e9.dir\testCXXCompiler.cxx.obj /FdCMakeFiles\cmTC_d74e9.dir\ /FS -c D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\x64-windows-dbg\CMakeFiles\CMakeScratch\TryCompile-669b6l\testCXXCompiler.cxx
    [2/2] C:\WINDOWS\system32\cmd.exe /C "cd . && D:\A股急速交易系统\vcpkg\downloads\tools\cmake-3.31.10-windows\cmake-3.31.10-windows-x86_64\bin\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\cmTC_d74e9.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\BuildTools\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\link.exe /nologo CMakeFiles\cmTC_d74e9.dir\testCXXCompiler.cxx.obj  /out:cmTC_d74e9.exe /implib:cmTC_d74e9.lib /pdb:cmTC_d74e9.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
    FAILED: [code=4294967295] cmTC_d74e9.exe 
    C:\WINDOWS\system32\cmd.exe /C "cd . && D:\A股急速交易系统\vcpkg\downloads\tools\cmake-3.31.10-windows\cmake-3.31.10-windows-x86_64\bin\cmake.exe -E vs_link_exe --msvc-ver=1944 --intdir=CMakeFiles\cmTC_d74e9.dir --rc=rc --mt=CMAKE_MT-NOTFOUND --manifests  -- C:\BuildTools\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\link.exe /nologo CMakeFiles\cmTC_d74e9.dir\testCXXCompiler.cxx.obj  /out:cmTC_d74e9.exe /implib:cmTC_d74e9.lib /pdb:cmTC_d74e9.pdb /version:0.0 /machine:x64  /nologo    /debug /INCREMENTAL /subsystem:console  kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib && cd ."
    RC Pass 1: command "rc /fo CMakeFiles\cmTC_d74e9.dir/manifest.res CMakeFiles\cmTC_d74e9.dir/manifest.rc" failed (exit code 0) with the following output:
    no such file or directory
    ninja: build stopped: subcommand failed.
    
    

  

  CMake will not be able to correctly generate this project.
Call Stack (most recent call first):
  CMakeLists.txt:7 (project)


-- Configuring incomplete, errors occurred!
ninja: build stopped: subcommand failed.
```
</details>

<details><summary>D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-rel-CMakeCache.txt.log</summary>

```
# This is the CMakeCache file.
# For build in directory: d:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel
# It was generated by CMake: D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe
# You can edit this file to change values found and used by cmake.
# If you do not want to change any of the values, simply exit the editor.
# If you do want to change a value, simply edit, save, and exit the editor.
# The syntax for the file is as follows:
# KEY:TYPE=VALUE
# KEY is the name of a variable in the cache.
# TYPE is a hint to GUIs for the type of VALUE, DO NOT EDIT TYPE!.
# VALUE is the current value for the KEY.

########################
# EXTERNAL cache entries
########################

//No help, variable specified on the command line.
BUILD_SHARED_LIBS:UNINITIALIZED=ON

//Path to a program.
CMAKE_AR:FILEPATH=C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/lib.exe

//Choose the type of build, options are: None Debug Release RelWithDebInfo
// MinSizeRel ...
CMAKE_BUILD_TYPE:STRING=Release

CMAKE_CROSSCOMPILING:STRING=OFF

//CXX compiler
CMAKE_CXX_COMPILER:FILEPATH=C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe

CMAKE_CXX_FLAGS:STRING=' /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP '

CMAKE_CXX_FLAGS_DEBUG:STRING='/MDd /Z7 /Ob0 /Od /RTC1 '

//Flags used by the CXX compiler during MINSIZEREL builds.
CMAKE_CXX_FLAGS_MINSIZEREL:STRING=/O1 /Ob1 /DNDEBUG

CMAKE_CXX_FLAGS_RELEASE:STRING='/MD /O2 /Oi /Gy /DNDEBUG /Z7 '

//Flags used by the CXX compiler during RELWITHDEBINFO builds.
CMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING=/O2 /Ob1 /DNDEBUG

//Libraries linked by default with all C++ applications.
CMAKE_CXX_STANDARD_LIBRARIES:STRING=kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib

CMAKE_C_FLAGS:STRING=' /nologo /DWIN32 /D_WINDOWS /utf-8 /MP '

CMAKE_C_FLAGS_DEBUG:STRING='/MDd /Z7 /Ob0 /Od /RTC1 '

CMAKE_C_FLAGS_RELEASE:STRING='/MD /O2 /Oi /Gy /DNDEBUG /Z7 '

//No help, variable specified on the command line.
CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION:UNINITIALIZED=ON

//Flags used by the linker during all build types.
CMAKE_EXE_LINKER_FLAGS:STRING=/machine:x64

//Flags used by the linker during DEBUG builds.
CMAKE_EXE_LINKER_FLAGS_DEBUG:STRING=/nologo    /debug /INCREMENTAL

//Flags used by the linker during MINSIZEREL builds.
CMAKE_EXE_LINKER_FLAGS_MINSIZEREL:STRING=/INCREMENTAL:NO

CMAKE_EXE_LINKER_FLAGS_RELEASE:STRING='/nologo /DEBUG /INCREMENTAL:NO /OPT:REF /OPT:ICF  '

//Flags used by the linker during RELWITHDEBINFO builds.
CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO:STRING=/debug /INCREMENTAL

//Enable/Disable output of build database during the build.
CMAKE_EXPORT_BUILD_DATABASE:BOOL=

//Enable/Disable output of compile commands during generation.
CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=

//No help, variable specified on the command line.
CMAKE_EXPORT_NO_PACKAGE_REGISTRY:UNINITIALIZED=ON

//No help, variable specified on the command line.
CMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY:UNINITIALIZED=ON

//No help, variable specified on the command line.
CMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY:UNINITIALIZED=ON

//Value Computed by CMake.
CMAKE_FIND_PACKAGE_REDIRECTS_DIR:STATIC=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel/CMakeFiles/pkgRedirects

//No help, variable specified on the command line.
CMAKE_INSTALL_BINDIR:STRING=bin

//No help, variable specified on the command line.
CMAKE_INSTALL_LIBDIR:STRING=lib

//Install path prefix, prepended onto install directories.
CMAKE_INSTALL_PREFIX:PATH=D:/A股急速交易系统/vcpkg/packages/nlohmann-json_x64-windows

//No help, variable specified on the command line.
CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP:UNINITIALIZED=TRUE

//Path to a program.
CMAKE_LINKER:FILEPATH=C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/link.exe

//No help, variable specified on the command line.
CMAKE_MAKE_PROGRAM:UNINITIALIZED=D:\A股急速交易系统\vcpkg\downloads\tools\ninja-1.13.2-windows\ninja.exe

//Flags used by the linker during the creation of modules during
// all build types.
...
Skipped 205 lines
...
VCPKG_TARGET_TRIPLET:STRING=x64-windows

//Trace calls to find_package()
VCPKG_TRACE_FIND_PACKAGE:BOOL=OFF

//Enables messages from the VCPKG toolchain for debugging purposes.
VCPKG_VERBOSE:BOOL=OFF

//(experimental) Automatically copy dependencies into the install
// target directory for executables. Requires CMake 3.14.
X_VCPKG_APPLOCAL_DEPS_INSTALL:BOOL=OFF

//(experimental) Add USES_TERMINAL to VCPKG_APPLOCAL_DEPS to force
// serialization.
X_VCPKG_APPLOCAL_DEPS_SERIALIZED:BOOL=OFF

//The directory which contains the installed libraries for each
// triplet
_VCPKG_INSTALLED_DIR:PATH=D:/A股急速交易系统/vcpkg_installed

//No help, variable specified on the command line.
_VCPKG_ROOT_DIR:UNINITIALIZED=D:/A股急速交易系统/vcpkg

//Value Computed by CMake
nlohmann_json_BINARY_DIR:STATIC=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel

//Value Computed by CMake
nlohmann_json_IS_TOP_LEVEL:STATIC=ON

//Value Computed by CMake
nlohmann_json_SOURCE_DIR:STATIC=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean


########################
# INTERNAL cache entries
########################

//ADVANCED property for variable: CMAKE_AR
CMAKE_AR-ADVANCED:INTERNAL=1
//This is the directory where this CMakeCache.txt was created
CMAKE_CACHEFILE_DIR:INTERNAL=d:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-rel
//Major version of cmake used to create the current loaded cache
CMAKE_CACHE_MAJOR_VERSION:INTERNAL=3
//Minor version of cmake used to create the current loaded cache
CMAKE_CACHE_MINOR_VERSION:INTERNAL=31
//Patch version of cmake used to create the current loaded cache
CMAKE_CACHE_PATCH_VERSION:INTERNAL=10
//Path to CMake executable.
CMAKE_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe
//Path to cpack program executable.
CMAKE_CPACK_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cpack.exe
//Path to ctest program executable.
CMAKE_CTEST_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/ctest.exe
//ADVANCED property for variable: CMAKE_CXX_COMPILER
CMAKE_CXX_COMPILER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS
CMAKE_CXX_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_DEBUG
CMAKE_CXX_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_MINSIZEREL
CMAKE_CXX_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_RELEASE
CMAKE_CXX_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_RELWITHDEBINFO
CMAKE_CXX_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_STANDARD_LIBRARIES
CMAKE_CXX_STANDARD_LIBRARIES-ADVANCED:INTERNAL=1
//Path to cache edit program executable.
CMAKE_EDIT_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake-gui.exe
//Executable file format
CMAKE_EXECUTABLE_FORMAT:INTERNAL=Unknown
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS
CMAKE_EXE_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_DEBUG
CMAKE_EXE_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_MINSIZEREL
CMAKE_EXE_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_RELEASE
CMAKE_EXE_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXPORT_BUILD_DATABASE
CMAKE_EXPORT_BUILD_DATABASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXPORT_COMPILE_COMMANDS
CMAKE_EXPORT_COMPILE_COMMANDS-ADVANCED:INTERNAL=1
//Name of external makefile project generator.
CMAKE_EXTRA_GENERATOR:INTERNAL=
//Name of generator.
CMAKE_GENERATOR:INTERNAL=Ninja
//Generator instance identifier.
CMAKE_GENERATOR_INSTANCE:INTERNAL=
//Name of generator platform.
CMAKE_GENERATOR_PLATFORM:INTERNAL=
//Name of generator toolset.
CMAKE_GENERATOR_TOOLSET:INTERNAL=
//Source directory with the top level CMakeLists.txt file for this
// project
CMAKE_HOME_DIRECTORY:INTERNAL=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean
//ADVANCED property for variable: CMAKE_LINKER
CMAKE_LINKER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS
CMAKE_MODULE_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_DEBUG
CMAKE_MODULE_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_MINSIZEREL
CMAKE_MODULE_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_RELEASE
CMAKE_MODULE_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MT
CMAKE_MT-ADVANCED:INTERNAL=1
//number of local generators
CMAKE_NUMBER_OF_MAKEFILES:INTERNAL=1
//Platform information initialized
CMAKE_PLATFORM_INFO_INITIALIZED:INTERNAL=1
//noop for ranlib
CMAKE_RANLIB:INTERNAL=:
//ADVANCED property for variable: CMAKE_RC_COMPILER
CMAKE_RC_COMPILER-ADVANCED:INTERNAL=1
CMAKE_RC_COMPILER_WORKS:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS
CMAKE_RC_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_DEBUG
CMAKE_RC_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_MINSIZEREL
CMAKE_RC_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_RELEASE
CMAKE_RC_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_RELWITHDEBINFO
CMAKE_RC_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//Path to CMake installation.
CMAKE_ROOT:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS
CMAKE_SHARED_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_DEBUG
CMAKE_SHARED_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL
CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_RELEASE
CMAKE_SHARED_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SKIP_INSTALL_RPATH
CMAKE_SKIP_INSTALL_RPATH-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SKIP_RPATH
CMAKE_SKIP_RPATH-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS
CMAKE_STATIC_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_DEBUG
CMAKE_STATIC_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_MINSIZEREL
CMAKE_STATIC_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_RELEASE
CMAKE_STATIC_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_STATIC_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_TOOLCHAIN_FILE
CMAKE_TOOLCHAIN_FILE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_VERBOSE_MAKEFILE
CMAKE_VERBOSE_MAKEFILE-ADVANCED:INTERNAL=1
//Install the dependencies listed in your manifest:
//\n    If this is off, you will have to manually install your dependencies.
//\n    See https://github.com/microsoft/vcpkg/tree/master/docs/specifications/manifests.md
// for more info.
//\n
VCPKG_MANIFEST_INSTALL:INTERNAL=OFF
//ADVANCED property for variable: VCPKG_VERBOSE
VCPKG_VERBOSE-ADVANCED:INTERNAL=1
//Making sure VCPKG_MANIFEST_MODE doesn't change
Z_VCPKG_CHECK_MANIFEST_MODE:INTERNAL=OFF
//Vcpkg root directory
Z_VCPKG_ROOT_DIR:INTERNAL=D:/A股急速交易系统/vcpkg

```
</details>

<details><summary>D:\A股急速交易系统\vcpkg\buildtrees\nlohmann-json\config-x64-windows-dbg-CMakeCache.txt.log</summary>

```
# This is the CMakeCache file.
# For build in directory: d:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg
# It was generated by CMake: D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe
# You can edit this file to change values found and used by cmake.
# If you do not want to change any of the values, simply exit the editor.
# If you do want to change a value, simply edit, save, and exit the editor.
# The syntax for the file is as follows:
# KEY:TYPE=VALUE
# KEY is the name of a variable in the cache.
# TYPE is a hint to GUIs for the type of VALUE, DO NOT EDIT TYPE!.
# VALUE is the current value for the KEY.

########################
# EXTERNAL cache entries
########################

//No help, variable specified on the command line.
BUILD_SHARED_LIBS:UNINITIALIZED=ON

//Path to a program.
CMAKE_AR:FILEPATH=C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/lib.exe

//Choose the type of build, options are: None Debug Release RelWithDebInfo
// MinSizeRel ...
CMAKE_BUILD_TYPE:STRING=Debug

CMAKE_CROSSCOMPILING:STRING=OFF

//CXX compiler
CMAKE_CXX_COMPILER:FILEPATH=C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe

CMAKE_CXX_FLAGS:STRING=' /nologo /DWIN32 /D_WINDOWS /utf-8 /GR /EHsc /MP '

CMAKE_CXX_FLAGS_DEBUG:STRING='/MDd /Z7 /Ob0 /Od /RTC1 '

//Flags used by the CXX compiler during MINSIZEREL builds.
CMAKE_CXX_FLAGS_MINSIZEREL:STRING=/O1 /Ob1 /DNDEBUG

CMAKE_CXX_FLAGS_RELEASE:STRING='/MD /O2 /Oi /Gy /DNDEBUG /Z7 '

//Flags used by the CXX compiler during RELWITHDEBINFO builds.
CMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING=/O2 /Ob1 /DNDEBUG

//Libraries linked by default with all C++ applications.
CMAKE_CXX_STANDARD_LIBRARIES:STRING=kernel32.lib user32.lib gdi32.lib winspool.lib shell32.lib ole32.lib oleaut32.lib uuid.lib comdlg32.lib advapi32.lib

CMAKE_C_FLAGS:STRING=' /nologo /DWIN32 /D_WINDOWS /utf-8 /MP '

CMAKE_C_FLAGS_DEBUG:STRING='/MDd /Z7 /Ob0 /Od /RTC1 '

CMAKE_C_FLAGS_RELEASE:STRING='/MD /O2 /Oi /Gy /DNDEBUG /Z7 '

//No help, variable specified on the command line.
CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION:UNINITIALIZED=ON

//Flags used by the linker during all build types.
CMAKE_EXE_LINKER_FLAGS:STRING=/machine:x64

//Flags used by the linker during DEBUG builds.
CMAKE_EXE_LINKER_FLAGS_DEBUG:STRING=/nologo    /debug /INCREMENTAL

//Flags used by the linker during MINSIZEREL builds.
CMAKE_EXE_LINKER_FLAGS_MINSIZEREL:STRING=/INCREMENTAL:NO

CMAKE_EXE_LINKER_FLAGS_RELEASE:STRING='/nologo /DEBUG /INCREMENTAL:NO /OPT:REF /OPT:ICF  '

//Flags used by the linker during RELWITHDEBINFO builds.
CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO:STRING=/debug /INCREMENTAL

//Enable/Disable output of build database during the build.
CMAKE_EXPORT_BUILD_DATABASE:BOOL=

//Enable/Disable output of compile commands during generation.
CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=

//No help, variable specified on the command line.
CMAKE_EXPORT_NO_PACKAGE_REGISTRY:UNINITIALIZED=ON

//No help, variable specified on the command line.
CMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY:UNINITIALIZED=ON

//No help, variable specified on the command line.
CMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY:UNINITIALIZED=ON

//Value Computed by CMake.
CMAKE_FIND_PACKAGE_REDIRECTS_DIR:STATIC=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg/CMakeFiles/pkgRedirects

//No help, variable specified on the command line.
CMAKE_INSTALL_BINDIR:STRING=bin

//No help, variable specified on the command line.
CMAKE_INSTALL_LIBDIR:STRING=lib

//Install path prefix, prepended onto install directories.
CMAKE_INSTALL_PREFIX:PATH=D:/A股急速交易系统/vcpkg/packages/nlohmann-json_x64-windows/debug

//No help, variable specified on the command line.
CMAKE_INSTALL_SYSTEM_RUNTIME_LIBS_SKIP:UNINITIALIZED=TRUE

//Path to a program.
CMAKE_LINKER:FILEPATH=C:/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/link.exe

//No help, variable specified on the command line.
...
Skipped 219 lines
...
X_VCPKG_APPLOCAL_DEPS_INSTALL:BOOL=OFF

//(experimental) Add USES_TERMINAL to VCPKG_APPLOCAL_DEPS to force
// serialization.
X_VCPKG_APPLOCAL_DEPS_SERIALIZED:BOOL=OFF

//The directory which contains the installed libraries for each
// triplet
_VCPKG_INSTALLED_DIR:PATH=D:/A股急速交易系统/vcpkg_installed

//No help, variable specified on the command line.
_VCPKG_ROOT_DIR:UNINITIALIZED=D:/A股急速交易系统/vcpkg

//Value Computed by CMake
nlohmann_json_BINARY_DIR:STATIC=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg

//Value Computed by CMake
nlohmann_json_IS_TOP_LEVEL:STATIC=ON

//Value Computed by CMake
nlohmann_json_SOURCE_DIR:STATIC=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean


########################
# INTERNAL cache entries
########################

//ADVANCED property for variable: CMAKE_AR
CMAKE_AR-ADVANCED:INTERNAL=1
//This is the directory where this CMakeCache.txt was created
CMAKE_CACHEFILE_DIR:INTERNAL=d:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/x64-windows-dbg
//Major version of cmake used to create the current loaded cache
CMAKE_CACHE_MAJOR_VERSION:INTERNAL=3
//Minor version of cmake used to create the current loaded cache
CMAKE_CACHE_MINOR_VERSION:INTERNAL=31
//Patch version of cmake used to create the current loaded cache
CMAKE_CACHE_PATCH_VERSION:INTERNAL=10
//Path to CMake executable.
CMAKE_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake.exe
//Path to cpack program executable.
CMAKE_CPACK_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cpack.exe
//Path to ctest program executable.
CMAKE_CTEST_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/ctest.exe
//ADVANCED property for variable: CMAKE_CXX_COMPILER
CMAKE_CXX_COMPILER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS
CMAKE_CXX_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_DEBUG
CMAKE_CXX_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_MINSIZEREL
CMAKE_CXX_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_RELEASE
CMAKE_CXX_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_FLAGS_RELWITHDEBINFO
CMAKE_CXX_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_STANDARD_LIBRARIES
CMAKE_CXX_STANDARD_LIBRARIES-ADVANCED:INTERNAL=1
//Path to cache edit program executable.
CMAKE_EDIT_COMMAND:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/bin/cmake-gui.exe
//Executable file format
CMAKE_EXECUTABLE_FORMAT:INTERNAL=Unknown
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS
CMAKE_EXE_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_DEBUG
CMAKE_EXE_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_MINSIZEREL
CMAKE_EXE_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_RELEASE
CMAKE_EXE_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXPORT_BUILD_DATABASE
CMAKE_EXPORT_BUILD_DATABASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_EXPORT_COMPILE_COMMANDS
CMAKE_EXPORT_COMPILE_COMMANDS-ADVANCED:INTERNAL=1
//Name of external makefile project generator.
CMAKE_EXTRA_GENERATOR:INTERNAL=
//Name of generator.
CMAKE_GENERATOR:INTERNAL=Ninja
//Generator instance identifier.
CMAKE_GENERATOR_INSTANCE:INTERNAL=
//Name of generator platform.
CMAKE_GENERATOR_PLATFORM:INTERNAL=
//Name of generator toolset.
CMAKE_GENERATOR_TOOLSET:INTERNAL=
//Source directory with the top level CMakeLists.txt file for this
// project
CMAKE_HOME_DIRECTORY:INTERNAL=D:/A股急速交易系统/vcpkg/buildtrees/nlohmann-json/src/v3.12.0-89fed620e6.clean
//ADVANCED property for variable: CMAKE_LINKER
CMAKE_LINKER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS
CMAKE_MODULE_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_DEBUG
CMAKE_MODULE_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_MINSIZEREL
CMAKE_MODULE_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_RELEASE
CMAKE_MODULE_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_MT
CMAKE_MT-ADVANCED:INTERNAL=1
//number of local generators
CMAKE_NUMBER_OF_MAKEFILES:INTERNAL=1
//Platform information initialized
CMAKE_PLATFORM_INFO_INITIALIZED:INTERNAL=1
//noop for ranlib
CMAKE_RANLIB:INTERNAL=:
//ADVANCED property for variable: CMAKE_RC_COMPILER
CMAKE_RC_COMPILER-ADVANCED:INTERNAL=1
CMAKE_RC_COMPILER_WORKS:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS
CMAKE_RC_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_DEBUG
CMAKE_RC_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_MINSIZEREL
CMAKE_RC_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_RELEASE
CMAKE_RC_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_RC_FLAGS_RELWITHDEBINFO
CMAKE_RC_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//Path to CMake installation.
CMAKE_ROOT:INTERNAL=D:/A股急速交易系统/vcpkg/downloads/tools/cmake-3.31.10-windows/cmake-3.31.10-windows-x86_64/share/cmake-3.31
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS
CMAKE_SHARED_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_DEBUG
CMAKE_SHARED_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL
CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_RELEASE
CMAKE_SHARED_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SKIP_INSTALL_RPATH
CMAKE_SKIP_INSTALL_RPATH-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_SKIP_RPATH
CMAKE_SKIP_RPATH-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS
CMAKE_STATIC_LINKER_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_DEBUG
CMAKE_STATIC_LINKER_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_MINSIZEREL
CMAKE_STATIC_LINKER_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_RELEASE
CMAKE_STATIC_LINKER_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_STATIC_LINKER_FLAGS_RELWITHDEBINFO
CMAKE_STATIC_LINKER_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_TOOLCHAIN_FILE
CMAKE_TOOLCHAIN_FILE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_VERBOSE_MAKEFILE
CMAKE_VERBOSE_MAKEFILE-ADVANCED:INTERNAL=1
//Install the dependencies listed in your manifest:
//\n    If this is off, you will have to manually install your dependencies.
//\n    See https://github.com/microsoft/vcpkg/tree/master/docs/specifications/manifests.md
// for more info.
//\n
VCPKG_MANIFEST_INSTALL:INTERNAL=OFF
//ADVANCED property for variable: VCPKG_VERBOSE
VCPKG_VERBOSE-ADVANCED:INTERNAL=1
//Making sure VCPKG_MANIFEST_MODE doesn't change
Z_VCPKG_CHECK_MANIFEST_MODE:INTERNAL=OFF
//Vcpkg root directory
Z_VCPKG_ROOT_DIR:INTERNAL=D:/A股急速交易系统/vcpkg

```
</details>

**Additional context**

<details><summary>vcpkg.json</summary>

```
{
  "name": "a-stock-fast-trading",
  "version-string": "0.1.0",
  "dependencies": [
    "nlohmann-json",
    "redis-plus-plus"
  ]
}

```
</details>
