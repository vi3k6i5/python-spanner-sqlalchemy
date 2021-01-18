# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
    name="sqlalchemy-spanner",
    version='0.1',
    description="SQLAlchemy dialect integrated into Spanner database",
    author='QLogic LLC',
    author_email='cloud-spanner-developers@googlegroups.com',
    packages=['spanner'],
    classifiers=[
        "Intended Audience :: Developers",
    ],
    install_requires=[
        'sqlalchemy>=1.1.13',
        'google-cloud-spanner==3.0.0'
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'spanner = spanner.sqlalchemy_spanner:SpannerDialect'
        ]
    }
)