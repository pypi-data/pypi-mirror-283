import setuptools

setuptools.setup(
	name = "TP-Frida",
	version = "2024.7.7",
	author = "TP Cyber Security",
	license = "MIT",
	author_email = "tpcybersec2023@gmail.com",
	description = "",
	long_description = open("README.md").read(),
	long_description_content_type = "text/markdown",
	install_requires = open("requirements.txt").read().split(),
	url = "https://github.com/truocphan/TP-Frida",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 2",
	],
	entry_points = {
		"console_scripts": [
			"TP-Frida = TP_Frida:main"
		]
	},
)