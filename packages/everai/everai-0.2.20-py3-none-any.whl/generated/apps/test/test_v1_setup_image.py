# coding: utf-8

"""
    everai/apps/v1/worker.proto

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: version not set
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from generated.apps.models.v1_setup_image import V1SetupImage  # noqa: E501

class TestV1SetupImage(unittest.TestCase):
    """V1SetupImage unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> V1SetupImage:
        """Test V1SetupImage
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `V1SetupImage`
        """
        model = V1SetupImage()  # noqa: E501
        if include_optional:
            return V1SetupImage(
                repository = '',
                tag = '',
                digest = '',
                basic_auth = generated.apps.models.v1_basic_auth.v1BasicAuth(
                    username = generated.apps.models.v1_value_from_secret.v1ValueFromSecret(
                        name = '', 
                        key = '', ), 
                    password = generated.apps.models.v1_value_from_secret.v1ValueFromSecret(
                        name = '', 
                        key = '', ), )
            )
        else:
            return V1SetupImage(
                repository = '',
        )
        """

    def testV1SetupImage(self):
        """Test V1SetupImage"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
