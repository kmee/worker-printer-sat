# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="worker-printer",
    version="12.0.1",
    description="Base Odoo project with brazilian localization",
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author="KMEE",
    author_email="suporte@kmee.com.br",
    url="kmee.com.br",
    packages=find_packages(),
    install_requires=[
        'cerberus>=1.3.2',
        'future>=0.18.2',
        'satcfe>=2.1',
        'satcomum>=2.2',
        'satextrato>=0.4',
        'unidecode>=1.2.0',
        'PyESCPOS>=0.4',
        'redis',
        'rq'
    ]
)
