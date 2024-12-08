from setuptools import setup

setup(
  name="bananopie",
  url="https://github.com/jetstream0/bananopie",
  author="John Doe",
  author_email="prussia@prussia.dev",
  packages=["bananopie"],
  install_requires=["requests", "ed25519_blake2b"],
  version="0.1.4",
  license="MIT",
  description="A python library to simplify sending and receiving Banano. Also a RPC wrapper.",
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown',
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.5"
)
