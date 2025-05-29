from setuptools import setup

setup(
    name="protopost-agent",
    version="0.0.0",
    packages=["protopost_agent"],
    install_requires=[
        "langchain",
        "protopost @ git+https://github.com/tehzevo/protopost-python.git#egg=protopost"
    ],
    entry_points={
        "console_scripts": [
            "protopost-agent = protopost_agent.run:main",
        ],
    },
)