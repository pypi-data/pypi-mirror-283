from setuptools import setup, find_packages

setup(
    name='mkdocs-src-links-corrector',
    version='0.0.3',
    description='An MkDocs plugin',
    long_description='An MkDocs plugin that automagically fixes images src links',
    keywords='mkdocs',
    url='https://github.com/barmidrol/mkdocs-src-links-corrector',
    author='Siarhei Padlozny',
    author_email='barmidrol@gmail.com',
    license='MIT',
    python_requires='>=3.4',
    install_requires=[
        'mkdocs>=1.2.3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
        entry_points={
        'mkdocs.plugins': [
            'img_src_corrector = mkdocs_src_links_corrector.plugin:ImgSrcPlugin',
        ]
    }
)
