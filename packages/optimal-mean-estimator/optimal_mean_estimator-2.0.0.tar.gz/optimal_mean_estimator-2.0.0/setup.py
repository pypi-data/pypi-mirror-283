 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sun Jun  9 01:35:07 2024

@author: Bennjamin Schulz

Copyright (c) <2024> <Benjamin Schulz>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use,copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software,and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
name='optimal_mean_estimator',
version='2.0.0',
author='Benjamin Schulz',
description='a Python implementation of the optimal subgaussian mean estimator that was published by Lee and Valiant at https://arxiv.org/abs/2011.08384',
long_description=long_description,
long_description_content_type='text/markdown',
url="https://github.com/bschulz81/optimal_mean_estimator/tree/main",
license="MIT License",
packages=['optimal_mean_estimator'],
install_requires=['numpy', 'scipy'],
keywords='statistics, estimator, mean',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.7',
)
