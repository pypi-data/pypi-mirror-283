from setuptools import setup, find_packages

setup(
    name='MathRocket', 
    version='0.2',  

    description='Uma biblioteca Python para simulação e cálculo de trajetórias de foguetes, com suporte para calcular massa, empuxo e tempo de queima.',
    long_description='A biblioteca Python "MathRocket" é projetada para facilitar a simulação e o cálculo de trajetórias de foguetes em ambientes de modelagem física e engenharia. Com "MathRocket", desenvolvedores podem calcular dinamicamente a aceleração, impulso e outras características essenciais de foguetes através de uma interface simples e intuitiva. Esta biblioteca é ideal para projetos que envolvem análise de desempenho de lançamentos, estudos de física aplicada e simulações educacionais, oferecendo uma maneira eficiente e precisa de explorar o comportamento de sistemas de propulsão espacial.',  
    long_description_content_type='text/markdown',  

    author='Unoxys',

    url='https://github.com/Uno13x/MathRocket',

    license='MIT',

    keywords='python, física, Foguete, Rocket, rocket, physic, Physics, Physic, mass, Mass',

    packages=find_packages(),

    install_requires=[
        "numpy",
        "matplotlib",
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
