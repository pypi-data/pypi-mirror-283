from setuptools import setup, find_packages

setup(
    name='wonder-diffusion-sdk',
    version='0.0.7',
    description='Python SDK for common Wonder diffusion models',
    long_description='''
    Version 0.0.7:
      - AutoencoderTiny model added as an optimization.

    Version 0.0.6:
      - !! Scheduler Config added. Model config scheduler parameter changed. THIS IS A BREAKING CHANGE.
      - Refactor for better controlnet and lora usage.

    Version 0.0.5:
      - ControlNet added.
      - Lora usage added.

    Version 0.0.3:
      - Lightning model added.
      - **kwargs** for schedulers added.
    ''',
    author='basri',
    author_email='basri@wonder.co',
    packages=find_packages(),
    install_requires=[
        'diffusers==0.26.3'
    ],
)
