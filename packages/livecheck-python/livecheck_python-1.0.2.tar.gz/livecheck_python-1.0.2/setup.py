import setuptools

VERSION = "1.0.2"

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='livecheck_python',
    version=VERSION,
    author='Dinh Tuan Tran',
    author_email='tuan.t.d@ieee.org',
    description='Check Program Bugs Anywhere - Track Your Logs On-the-Go',
    keywords='debug, track, exception, log, plot, graph, smartphone, realtime, machine learning, deep learning, computer vision',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://livecheck.dev',
    project_urls={
        'Documentation': 'https://livecheck.dev/help',
        'Bug Reports': 'https://github.com/dinhtuantran/livecheck_python/issues',
        'Source Code': 'https://github.com/dinhtuantran/livecheck_python',
        # 'Funding': '',
    },
    packages=['livecheck_python'],
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6.7',
    install_requires=[
        'pytz',
        'requests'
    ],
)
