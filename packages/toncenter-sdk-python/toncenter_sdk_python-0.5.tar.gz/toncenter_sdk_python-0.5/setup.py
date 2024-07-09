from setuptools import setup

setup(name='toncenter_sdk_python',
      version='0.5',
      description='TONCENTER SDK FOR PYTHON',
      packages=[
            'toncenter_sdk', 
            'toncenter_sdk/cfgs', 
            'toncenter_sdk/datas', 
            'toncenter_sdk/sides', 
            'toncenter_sdk/V2', 
            'toncenter_sdk/V3'
      ],
      author_email='dev.nevermore696@gmail.com',
      zip_safe=False)