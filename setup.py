import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    packages = fh.read().splitlines()

setuptools.setup(
    name="netbox-rbac",
    version="1.0.13",
    author="Eric Busto",
    author_email="ebusto@nvidia.com",
    description="Opinionated RBAC for NetBox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebusto/netbox-rbac",
    packages=setuptools.find_packages(),
    install_requires=packages,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
