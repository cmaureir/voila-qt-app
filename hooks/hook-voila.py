from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('voila')
hiddenimports = collect_submodules('voila')
