from setuptools import setup, find_packages

setup(
    name='TechSolve_manim',
    version='0.0.1',
    description='A library with essential elements for technical diagrams.',
    long_description=(
        'TechSolve_manim is a powerful library designed to simplify the creation '
        'of technical diagrams using the Manim animation engine. Whether you are '
        'an engineer, educator, or developer, this library provides a collection '
        'of fundamental components that will help you build clear and professional '
        'technical diagrams with ease.'
    ),
    long_description_content_type='text/plain',
    author='LLlBiDKiCLLb',
    author_email='LLlBiDKiCLLb@gmail.com',
    url='https://github.com/romasenkevich/TechSolve_manim',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'manim',
        'fonttools'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
    ],
    keywords='technical diagrams manim visualization',
    python_requires='>=3.6',
)
