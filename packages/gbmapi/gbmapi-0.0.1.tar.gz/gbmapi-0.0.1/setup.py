import os
import setuptools

about = {}
current_dir = os.path.abspath(os.path.dirname(__file__))
package_dir = 'gbmapi'

with open(os.path.join(current_dir, package_dir, "__version__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)

package = about["__package__"]

packages = setuptools.find_packages(
    exclude=["contrib", "docs", "tests"],
)

version = os.environ.get('RELEASE_VERSION', about["__version__"])

setuptools.setup(
    name=package,  # installation
    version=version,
    author=about["__author__"],
    author_email=about["__author__"],
    description=about["__description__"],
    long_description=open('readme.rst', 'r', encoding='utf-8').read(),
    long_description_content_type="text/x-rst",
    url=about["__url__"],
    project_urls={
        "Documentation": about["__docs_url__"],
        "Source": about["__url__"],
        # "Changelog": about["__change_log_url__"],
    },
    license=about["__license__"],
    keywords=[
        'gbm'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    python_requires='>=3.11',
    package_dir={package: package_dir},
    packages=packages,
    package_data={
        package: [
            "markdown_styles/*",
            "schemas/*",
            'images/*',
        ],
    },
    install_requires=[
        'requests',
        'pyotp'
    ],
    extras_require={
        'test': [
            'coverage',
            'pytest',
        ]
    }
)
