from setuptools import setup, find_packages


setup(
    name='itba_microservices_rabbitmq_connectors',
    version='0.1.6',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'pydantic==2.7.1',
        'pika==1.3.2',
    ],
    author='Gonzalo Beade',
    author_email='gbeade@itba.edu.ar',
    description="""
        A queues utility package for ITBA Microservices course.
    """,
    url='https://gitlab.com/gbeade/microservices',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
