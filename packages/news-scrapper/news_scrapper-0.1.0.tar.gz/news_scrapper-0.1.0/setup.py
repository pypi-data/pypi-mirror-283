from setuptools import setup, find_packages

setup(
    name='news_scrapper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            'news-scraper=news_scraper.scraper:main',
        ],
    },
    author='Aniruddha Kumar',
    author_email='foraniruddhakumar@gmail.com',
    description='A web scraper for Investopedia news headlines',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Demon-2-Angel/Daily_Financial_News_Automation',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
