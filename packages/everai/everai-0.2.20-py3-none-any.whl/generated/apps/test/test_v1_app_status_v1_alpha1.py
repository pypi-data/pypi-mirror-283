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

from generated.apps.models.v1_app_status_v1_alpha1 import V1AppStatusV1Alpha1  # noqa: E501

class TestV1AppStatusV1Alpha1(unittest.TestCase):
    """V1AppStatusV1Alpha1 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> V1AppStatusV1Alpha1:
        """Test V1AppStatusV1Alpha1
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `V1AppStatusV1Alpha1`
        """
        model = V1AppStatusV1Alpha1()  # noqa: E501
        if include_optional:
            return V1AppStatusV1Alpha1(
                desired_worker = 56,
                ready_worker = 56,
                events = generated.apps.models.v1_event.v1Event(
                    type = '', 
                    message = '', 
                    from = '', 
                    create_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ),
                status = 'STATUS_UNSPECIFIED'
            )
        else:
            return V1AppStatusV1Alpha1(
        )
        """

    def testV1AppStatusV1Alpha1(self):
        """Test V1AppStatusV1Alpha1"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
