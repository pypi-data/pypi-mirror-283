from setuptools import setup, find_packages

setup(
    name='koros-python-payments',
    version='1.0.0',
    author='Kevin Ongulu',
    author_email='kevinongulu@gmail.com',
    description='A python package for connecting to payments platforms like MPESA,PayPal,RazorPay',
    #packages=find_packages(),
    packages = ['mpesa','paypal'], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests', #requests>=2.26.0
        'python-dotenv',
        'pycryptodome'
    ],
    python_requires='>=3.6',
)