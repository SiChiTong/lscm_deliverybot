from setuptools import setup
from setuptools import find_packages
from glob import glob

package_name = 'lift_contr'
submodule = 'lift_contr/submodules'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, submodule],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='u',
    maintainer_email='josefgstoettner@live.at',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lift_door = lift_contr.lift_door:main'
        ],
    },
)
