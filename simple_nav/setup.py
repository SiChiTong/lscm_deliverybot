from setuptools import setup

package_name = 'simple_nav'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'demo_inspection = simple_nav.demo_inspection:main',
            'demo_security = simple_nav.demo_security:main',
        ],
    },
)
