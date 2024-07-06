import sys
from setuptools import setup, find_packages
import io

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False

except ImportError:
    bdist_wheel = None

with io.open("README.md", encoding="utf-8") as h:
    long_description = h.read()

if sys.version_info < (3, 0):
    sys.exit("Sorry, Python < 3.0 is not supported")

requirements = ["numpy", "tqdm", "requests", "portalocker", "opencv-python"]

setup(
    name="ncnn-riscv-wheel",
    version="1.0.20240706",
    author="nihui",
    author_email="nihuini@tencent.com",
    maintainer="per1cycle",
    maintainer_email="pericycle.cc@gmail.com",
    description="ncnn is a high-performance neural network inference framework optimized for the mobile platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/per1cycle/ncnn-riscv-wheel",
    classifiers=[
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    license="BSD-3",
    python_requires=">=3.5",
    packages=find_packages(),
    package_dir={"": "."},
    package_data={"ncnn": ["ncnn.cpython-311-riscv64-linux-gnu.so"]},
    install_requires=requirements,
    cmdclass={"bdist_wheel": bdist_wheel},
)
