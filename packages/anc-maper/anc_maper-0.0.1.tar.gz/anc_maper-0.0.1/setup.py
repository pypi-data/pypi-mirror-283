import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anc-maper",
    version="0.0.1",
    author="ryo komatsu",
    author_email="r.y.o627b@gmail.com",
    description="Know the old names of prefectures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yorunotuki/anc-maper",
    project_urls={
        "Bug Tracker": "https://github.com/yorunotuki/anc-maper",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["anc_maper"],
    python_requires=">=3.12",
    install_requires = [
    'matplotlib>=3.9.0',
    'japanmap>=0.3.1'
    ],
    entry_points = {
        'console_scripts': [
            'anc-maper = anc_maper:main'
        ],
    },
)