
:: "c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"

IF NOT EXIST "libmseed" (
    tar -xzf libmseed-2.19.6.tar.gz --exclude=doc --exclude=test --exclude=example
) ELSE (
    ECHO libmseed found
)
