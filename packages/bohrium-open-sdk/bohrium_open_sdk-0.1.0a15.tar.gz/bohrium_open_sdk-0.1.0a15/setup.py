import os

from setuptools import find_packages, setup


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="bohrium-open-sdk",
    version="0.1.0-alpha.15",
    author="Bohrium Team",
    url="https://bohrium.dp.tech/developer",
    description="bohrium-open-sdk",
    long_description_content_type="text/markdown",  # file format
    packages=find_packages("src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={"": "src"},  # find_packages define code directory
    package_data={
        # include .txt all of them
        "": ["*.txt"]
    },
    install_requires=[
        "httpx==0.27.0",
        "requests==2.32.3",
        "tqdm==4.66.4",
        "distro==1.9.0",
        "python-dotenv==1.0.0",
        "glom==23.5.0",
        "pytest==8.2.2",
        "gradio-materialviewer==0.0.4",
        "gradio-mapping==0.0.2",
        "gradio-perturbation-graph==0.0.1",
        "gradio-fep-result-table==0.0.1",
        "gradio-fep-pair-table==0.0.1",
        "gradio-dp-project==0.0.1",
        "gradio-dp-machine==0.0.1",
        "dp-sequence-editor==0.0.1",
        "gradio-uni-view==0.0.2",
        "dp-launching-app==0.1.0-alpha.1"
    ],
    python_requires=">=3.8",
    entry_points={},
)
