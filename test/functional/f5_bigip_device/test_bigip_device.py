# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import pytest
from pytest import symbols

from heatclient.exc import HTTPException

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def test_create_complete(HeatStack):
    hc, stack = HeatStack(
        os.path.join(TEST_DIR, 'success.yaml'),
        'success_test',
        parameters={
            'bigip_ip': symbols.bigip_ip,
            'bigip_un': symbols.bigip_un,
            'bigip_pw': symbols.bigip_pw
        }
    )


def test_create_failed_bad_ip(HeatStack):
    hc, stack = HeatStack(
        os.path.join(TEST_DIR, 'bad_ip.yaml'),
        'bad_ip_test',
        expect_fail=True
    )
    assert 'ConnectionError' in stack.stack_status_reason


def test_create_failed_bad_password(HeatStack):
    hc, stack = HeatStack(
        os.path.join(TEST_DIR, 'bad_password.yaml'),
        'bad_password_test',
        parameters={
            'bigip_ip': symbols.bigip_ip,
            'bigip_un': symbols.bigip_un,
            'bigip_pw': 'bad_password'
        },
        expect_fail=True
    )
    assert 'BigIPConnectionFailed' in stack.stack_status_reason
    assert 'Authorization Required for uri' in stack.stack_status_reason


def test_create_bad_property(HeatStack):
    with pytest.raises(HTTPException) as ex:
        HeatStack(
            os.path.join(TEST_DIR, 'bad_property.yaml'),
            'bad_property',
            parameters={
                'bigip_ip': symbols.bigip_ip,
                'bigip_un': symbols.bigip_un,
                'bigip_pw': symbols.bigip_pw
            },
            expect_fail=True
        )
    assert 'Unknown Property bad_extra_prop' in ex.value.message
