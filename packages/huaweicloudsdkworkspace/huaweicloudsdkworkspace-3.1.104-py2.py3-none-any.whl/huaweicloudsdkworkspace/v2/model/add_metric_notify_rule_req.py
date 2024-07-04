# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class AddMetricNotifyRuleReq:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'metric_name': 'str',
        'threshold': 'int',
        'comparison_operator': 'str',
        'interval': 'int',
        'enable': 'bool',
        'notify_object': 'str'
    }

    attribute_map = {
        'metric_name': 'metric_name',
        'threshold': 'threshold',
        'comparison_operator': 'comparison_operator',
        'interval': 'interval',
        'enable': 'enable',
        'notify_object': 'notify_object'
    }

    def __init__(self, metric_name=None, threshold=None, comparison_operator=None, interval=None, enable=None, notify_object=None):
        """AddMetricNotifyRuleReq

        The model defined in huaweicloud sdk

        :param metric_name: 统计指标名称，目前仅支持固定值：desktop_idle_duration 同一指标的规则不允许重复 * &#x60;desktop_idle_duration&#x60; -  桌面空闲时长, 仅允许设置 &#39;&gt;&#x3D;&#39; threshold
        :type metric_name: str
        :param threshold: 规则配置-阈值(天)
        :type threshold: int
        :param comparison_operator: 统计指标对应的统计值和threshold进行比较的条件 * &#x60;&gt;&#x3D;&#x60; -  统计指标大于等于threshold时触发 * &#x60;&gt;&#x60; -   统计指标大于threshold时触发 * &#x60;&#x3D;&#x60; -  统计指标等于threshold时触发 * &#x60;&lt;&#x3D;&#x60; -  统计指标小于等于threshold时触发 * &#x60;&lt;&#x60; -  统计指标小于threshold时触发
        :type comparison_operator: str
        :param interval: 触发通知后；下次通知的间隔时间;默认每天一次
        :type interval: int
        :param enable: 启禁用规则 true:启用 false:禁用
        :type enable: bool
        :param notify_object: 通知对象;smn的主题urn
        :type notify_object: str
        """
        
        

        self._metric_name = None
        self._threshold = None
        self._comparison_operator = None
        self._interval = None
        self._enable = None
        self._notify_object = None
        self.discriminator = None

        self.metric_name = metric_name
        if threshold is not None:
            self.threshold = threshold
        self.comparison_operator = comparison_operator
        if interval is not None:
            self.interval = interval
        self.enable = enable
        self.notify_object = notify_object

    @property
    def metric_name(self):
        """Gets the metric_name of this AddMetricNotifyRuleReq.

        统计指标名称，目前仅支持固定值：desktop_idle_duration 同一指标的规则不允许重复 * `desktop_idle_duration` -  桌面空闲时长, 仅允许设置 '>=' threshold

        :return: The metric_name of this AddMetricNotifyRuleReq.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """Sets the metric_name of this AddMetricNotifyRuleReq.

        统计指标名称，目前仅支持固定值：desktop_idle_duration 同一指标的规则不允许重复 * `desktop_idle_duration` -  桌面空闲时长, 仅允许设置 '>=' threshold

        :param metric_name: The metric_name of this AddMetricNotifyRuleReq.
        :type metric_name: str
        """
        self._metric_name = metric_name

    @property
    def threshold(self):
        """Gets the threshold of this AddMetricNotifyRuleReq.

        规则配置-阈值(天)

        :return: The threshold of this AddMetricNotifyRuleReq.
        :rtype: int
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Sets the threshold of this AddMetricNotifyRuleReq.

        规则配置-阈值(天)

        :param threshold: The threshold of this AddMetricNotifyRuleReq.
        :type threshold: int
        """
        self._threshold = threshold

    @property
    def comparison_operator(self):
        """Gets the comparison_operator of this AddMetricNotifyRuleReq.

        统计指标对应的统计值和threshold进行比较的条件 * `>=` -  统计指标大于等于threshold时触发 * `>` -   统计指标大于threshold时触发 * `=` -  统计指标等于threshold时触发 * `<=` -  统计指标小于等于threshold时触发 * `<` -  统计指标小于threshold时触发

        :return: The comparison_operator of this AddMetricNotifyRuleReq.
        :rtype: str
        """
        return self._comparison_operator

    @comparison_operator.setter
    def comparison_operator(self, comparison_operator):
        """Sets the comparison_operator of this AddMetricNotifyRuleReq.

        统计指标对应的统计值和threshold进行比较的条件 * `>=` -  统计指标大于等于threshold时触发 * `>` -   统计指标大于threshold时触发 * `=` -  统计指标等于threshold时触发 * `<=` -  统计指标小于等于threshold时触发 * `<` -  统计指标小于threshold时触发

        :param comparison_operator: The comparison_operator of this AddMetricNotifyRuleReq.
        :type comparison_operator: str
        """
        self._comparison_operator = comparison_operator

    @property
    def interval(self):
        """Gets the interval of this AddMetricNotifyRuleReq.

        触发通知后；下次通知的间隔时间;默认每天一次

        :return: The interval of this AddMetricNotifyRuleReq.
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this AddMetricNotifyRuleReq.

        触发通知后；下次通知的间隔时间;默认每天一次

        :param interval: The interval of this AddMetricNotifyRuleReq.
        :type interval: int
        """
        self._interval = interval

    @property
    def enable(self):
        """Gets the enable of this AddMetricNotifyRuleReq.

        启禁用规则 true:启用 false:禁用

        :return: The enable of this AddMetricNotifyRuleReq.
        :rtype: bool
        """
        return self._enable

    @enable.setter
    def enable(self, enable):
        """Sets the enable of this AddMetricNotifyRuleReq.

        启禁用规则 true:启用 false:禁用

        :param enable: The enable of this AddMetricNotifyRuleReq.
        :type enable: bool
        """
        self._enable = enable

    @property
    def notify_object(self):
        """Gets the notify_object of this AddMetricNotifyRuleReq.

        通知对象;smn的主题urn

        :return: The notify_object of this AddMetricNotifyRuleReq.
        :rtype: str
        """
        return self._notify_object

    @notify_object.setter
    def notify_object(self, notify_object):
        """Sets the notify_object of this AddMetricNotifyRuleReq.

        通知对象;smn的主题urn

        :param notify_object: The notify_object of this AddMetricNotifyRuleReq.
        :type notify_object: str
        """
        self._notify_object = notify_object

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AddMetricNotifyRuleReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
