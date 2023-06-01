from setuptools import setup

package_name = "simple_nav"
submodule = "simple_nav/submodules"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name, submodule],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="u",
    maintainer_email="josefgstoettner@live.at",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "demo_inspection = simple_nav.demo_inspection:main",
            "demo_security = simple_nav.demo_security:main",
            "demo_gui = simple_nav.demo_gui:main",
            "demo_gui_sim = simple_nav.demo_gui_sim:main",
            "gui_door_sim = simple_nav.gui_door_sim:main",
            "gui_door = simple_nav.gui_door:main",
            "gui_medizine = simple_nav.gui_medizine:main",
        ],
    },
)
