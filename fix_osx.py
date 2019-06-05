import os
import sys
import glob
import shutil
import importlib


def patch_osx_app():
    """Patch .app to copy missing data and link some libs.
    See https://github.com/pyinstaller/pyinstaller/issues/2276
    """

    app_path = sys.argv[1]

    import PyQt5

    qtwe_core_dir = PyQt5.__path__[0] + '/Qt/lib/QtWebEngineCore.framework'

    # Copy QtWebEngineProcess.app
    proc_app = 'QtWebEngineProcess.app'
    if not os.path.exists(os.path.join(app_path, 'Contents', 'MacOS', proc_app)):
        shutil.copytree(os.path.join(qtwe_core_dir, 'Helpers', proc_app),
                        os.path.join(app_path, 'Contents', 'MacOS', proc_app))

    # Copy resources
    for f in glob.glob(os.path.join(qtwe_core_dir, 'Resources', '*')):
        dest = os.path.join(app_path, 'Contents', 'Resources')
        dest = os.path.join(dest, os.path.basename(f))
        if os.path.isdir(f):
            if not os.path.exists(dest):
                shutil.copytree(f, dest)
        else:
            if not os.path.exists(dest):
                shutil.copy(f, dest)

    # Link dependencies
    for lib in ['QtCore', 'QtWebEngineCore', 'QtQuick', 'QtQml', 'QtNetwork',
                'QtGui', 'QtWebChannel', 'QtPositioning']:
        dest = os.path.join(app_path, lib + '.framework', 'Versions', '5')
        os.makedirs(dest, exist_ok=True)
        if not os.path.join(os.path.join(dest, lib)):
            os.symlink(os.path.join(os.pardir, os.pardir, os.pardir, 'Contents',
                                    'MacOS', lib),
                       os.path.join(dest, lib))

    from voila import paths, __path__
    path = os.path.abspath(os.path.join(__path__[0], '..', 'share', 'jupyter'))

    if not os.path.exists(os.path.join(path, 'voila')):
        for path in paths.jupyter_path():
            print(path)
            if os.path.exists(os.path.join(path, 'voila')):
                break
        else:
            raise ValueError("Could not determine jupyter folder to use")

    print("Copying files from " + path)

    share_dir = os.path.join(app_path, 'Contents', 'MacOS', 'share')

    if not os.path.exists(os.path.join(share_dir, 'jupyter')):
        print('making ' + os.path.join(share_dir, 'jupyter'))
        os.makedirs(os.path.join(share_dir, 'jupyter'))
        for sub in ['nbextensions', 'voila']:
            print('copying ' + os.path.join(path, sub))
            shutil.copytree(os.path.join(path, sub), os.path.join(share_dir, 'jupyter', sub))


patch_osx_app()
