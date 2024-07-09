from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as file:
	long_description = file.read()

setup(
	name="amplabs",
	packages=find_packages(),
		package_data={'amplabs': ['config.yaml', 'assets/*']},
	version="0.2.0",
	description="One of the AmpLabs product to create high end plots for your data",
	author="Amplabs",
	install_requires=[
		"pandas==2.2.1",
		"plotly==5.22.0",
		"dash==2.16.1",
		"dash-bootstrap-components==1.5.0",
		"pyyaml==6.0",
		"dash-mantine-components==0.14.3",
		"dash-iconify==0.1.2",
	],
	readme="README.md",
	long_description=long_description,
	long_description_content_type="text/markdown",
	include_package_data=True,
)
