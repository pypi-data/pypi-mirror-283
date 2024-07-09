from setuptools import setup, find_packages

setup(
    name='mykmeansproject',
    version='0.7', 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Gereken diğer paketler
    ],
    package_data={
        'mykmeansproject': ['yeni44-mac.out','yeni44-mac-arm64.out',"yeni44-mac-x86_64.out", 'yeni44-linux.out', 'yeni44-windows.exe'],
    },
    entry_points={
        'console_scripts': [
            
        ],
    },
    author="Vasfi Tataroglu",
    author_email="vtatarog@iu.edu",
    description="A package for running KMeans and GeoKMeans algorithms.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/mykmeansproject",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
