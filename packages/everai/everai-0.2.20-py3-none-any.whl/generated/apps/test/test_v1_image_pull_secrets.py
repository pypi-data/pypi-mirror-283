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

from generated.apps.models.v1_image_pull_secrets import V1ImagePullSecrets  # noqa: E501

class TestV1ImagePullSecrets(unittest.TestCase):
    """V1ImagePullSecrets unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> V1ImagePullSecrets:
        """Test V1ImagePullSecrets
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `V1ImagePullSecrets`
        """
        model = V1ImagePullSecrets()  # noqa: E501
        if include_optional:
            return V1ImagePullSecrets(
                username = generated.apps.models.v1_value_from.v1ValueFrom(
                    secret_key_ref = generated.apps.models.v1_key_reference.v1KeyReference(
                        name = '', 
                        key = '', ), 
                    config_map_key_ref = generated.apps.models.v1_key_reference.v1KeyReference(
                        name = '', 
                        key = '', ), ),
                password = generated.apps.models.v1_value_from.v1ValueFrom(
                    secret_key_ref = generated.apps.models.v1_key_reference.v1KeyReference(
                        name = '', 
                        key = '', ), 
                    config_map_key_ref = generated.apps.models.v1_key_reference.v1KeyReference(
                        name = '', 
                        key = '', ), )
            )
        else:
            return V1ImagePullSecrets(
        )
        """

    def testV1ImagePullSecrets(self):
        """Test V1ImagePullSecrets"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
