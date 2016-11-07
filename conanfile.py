import os
from conans import ConanFile, tools

class TableauSDK(ConanFile):
    name = 'TableauSDK'
    version = '1.0'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/RussTheAerialist/conan-tableau-sdk'
    license = 'MIT'

    def _source_macos(self):
        download_url = "https://downloads.tableau.com/tssoftware/Tableau-SDK-10-1-1.dmg"
        tools.download(download_url, 'tableausdk.dmg')
        try:
            self.run('hdiutil attach -mountpoint /Volumes/sdk tableausdk.dmg')
            self.run('cp -R /Volumes/sdk/Frameworks/*.framework .')
        finally:
            self.run('hdiutil detach /Volumes/sdk')

    def _source_windows(self):
        name_part = 'Tableau-SDK-C-Java-64Bit-10-1-1'
        zip_name = 'tableausdk.zip'
        download_url = "https://downloads.tableau.com/tssoftware/{}.zip".format(name_part)
        tools.download(download_url, zip_name)
        tools.unzip(zip_name, 'tableausdk')
        os.unlink(zip_name)

    def source(self):
        source_function_name = '_source_{}'.format(self.settings.os)
        func = getattr(self, source_function_name.lower(), None)
        if func is not None:
            func()
        else:
            print('unknown operating system {}'.format(source_function_name))

    def build(self):
       pass  # prebuilt binaries

    def _package_macos(self):
        self.copy('*.framework/*', dst='lib')
        self.copy('*/framework/Tableau*', dst='lib')
        self.copy('*.h', dst='include/TableauCommon', src='TableauCommon.framework/Versions/Current/Headers')
        self.copy('*.h', dst='include/TableauExtract', src='TableauExtract.framework/Versions/Current/Headers')

    def _package_windows(self):
        self.copy('*.h', dst='include', src='tableausdk/include')
        self.copy('*.lib', dst='lib', src='tableausdk/lib')

    def package(self):
        package_function_name = '_package_{}'.format(self.settings.os)
        func = getattr(self, package_function_name.lower(), None)
        if func is not None:
            func()
        else:
            print('unknown operating system {}'.format(package_function_name))
        pass

    def package_info(self):
        if self.settings.os == 'Macos':
            self.cpp_info.exelinkflags.append("-F${CONAN_TABLEAUSDK_ROOT}/lib")
            self.cpp_info.exelinkflags.append("-framework TableauCommon")
            self.cpp_info.exelinkflags.append("-framework TableauExtract")

            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        else:
            self.cpp_info.libs=['TableauExtract', 'TableauCommon']
