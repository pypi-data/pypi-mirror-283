from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = ''
    header_count = 0
    for line in fh:
        if line.startswith('##'):
            header_count += 1
        if header_count < 2:
            long_description += line
        else:
            break

setup(
    author='wangc372',
    author_email='3305277792@qq.com',
    classifiers=[
        # Python 3.8 is minimally supported
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    description='User Gym: A collection of user-defined gym environment',
    install_requires=['gymnasium >= 0.21.0'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='user_openAI',
    packages=[package for package in find_packages()
              if package.startswith('user_openAI')],
    python_requires='>=3.8',
    version='0.0.2',
    zip_safe=False,
)
