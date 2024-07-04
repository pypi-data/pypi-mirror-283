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

from generated.apps.models.v1_app_service_setup_image_body import V1AppServiceSetupImageBody  # noqa: E501

class TestV1AppServiceSetupImageBody(unittest.TestCase):
    """V1AppServiceSetupImageBody unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> V1AppServiceSetupImageBody:
        """Test V1AppServiceSetupImageBody
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `V1AppServiceSetupImageBody`
        """
        model = V1AppServiceSetupImageBody()  # noqa: E501
        if include_optional:
            return V1AppServiceSetupImageBody(
                setup_image = generated.apps.models.image_setting.image setting(
                    repository = '', 
                    tag = '', 
                    digest = '', 
                    basic_auth = generated.apps.models.v1_basic_auth.v1BasicAuth(
                        username = generated.apps.models.v1_value_from_secret.v1ValueFromSecret(
                            name = '', 
                            key = '', ), 
                        password = generated.apps.models.v1_value_from_secret.v1ValueFromSecret(
                            name = '', 
                            key = '', ), ), )
            )
        else:
            return V1AppServiceSetupImageBody(
                setup_image = generated.apps.models.image_setting.image setting(
                    repository = '', 
                    tag = '', 
                    digest = '', 
                    basic_auth = generated.apps.models.v1_basic_auth.v1BasicAuth(
                        username = generated.apps.models.v1_value_from_secret.v1ValueFromSecret(
                            name = '', 
                            key = '', ), 
                        password = generated.apps.models.v1_value_from_secret.v1ValueFromSecret(
                            name = '', 
                            key = '', ), ), ),
        )
        """

    def testV1AppServiceSetupImageBody(self):
        """Test V1AppServiceSetupImageBody"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
