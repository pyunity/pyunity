from setuptools import setup, Distribution

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

setup(
    name="hpp-fcl",
    version="2.3.5",
    description="An extension of the Flexible Collision Library",
    python_requires=">=3.7",
    install_requires=["numpy"],
    packages=["hppfcl"],
    package_data={"hppfcl": ["*.dll", "hppfcl.lib", "hppfcl.cp*.pyd", "__init__.pyi"]},
    url="https://github.com/rayzchen/hpp-fcl",
    distclass=BinaryDistribution
)
