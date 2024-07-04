# Copyright (c) 2024 Xingchen Song (sxc19@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from tn.english.normalizer import Normalizer
from tn.english.test.utils import parse_test_case


class TestNormalizer:

    normalizer = Normalizer(overwrite_cache=True)
    cases = parse_test_case('data/normalizer.txt')

    @pytest.mark.parametrize("written, spoken", cases)
    def test_normalizer(self, written, spoken):
        assert self.normalizer.normalize(written) == spoken
