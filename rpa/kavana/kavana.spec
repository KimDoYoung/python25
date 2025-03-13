a = Analysis(
    ['kavana.py'],
    pathex=[],
    hiddenimports=[
        'multiprocessing',
        'multiprocessing.util',
        'multiprocessing.connection',
        'multiprocessing.pool',
        'multiprocessing.sharedctypes',
        'yaml',
        'numpy._core',
        'numpy._core._dtype',
        'numpy._core._methods',
        'numpy._core.multiarray',
        'numpy._core.numeric',
        'numpy._core.numerictypes',
        'numpy._core.overrides',
        'numpy._core.umath',
        'cv2'
    ],
    datas=[
        ('lib/core/', 'lib/core/'),
        ('lib/actions/', 'lib/actions/'),
        ('lib/utils/', 'lib/utils/'),
    ]
)
