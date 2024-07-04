# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ModifyWorkspaceAttributesReq:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'ad_info': 'AdDomainInfo',
        'ad_domains': 'AdDomain',
        'access_mode': 'str',
        'dedicated_subnets': 'str',
        'subnet_ids': 'list[str]',
        'internet_access_port': 'str',
        'enterprise_id': 'str',
        'is_send_email': 'bool',
        'dc_vnc_ip': 'str',
        'authorized_collect_log': 'bool',
        'authorized_hda_upgrade': 'bool',
        'apply_dedicated_standby_network_param': 'ApplyDedicatedStandbyNetworkParam'
    }

    attribute_map = {
        'ad_info': 'ad_info',
        'ad_domains': 'ad_domains',
        'access_mode': 'access_mode',
        'dedicated_subnets': 'dedicated_subnets',
        'subnet_ids': 'subnet_ids',
        'internet_access_port': 'internet_access_port',
        'enterprise_id': 'enterprise_id',
        'is_send_email': 'is_send_email',
        'dc_vnc_ip': 'dc_vnc_ip',
        'authorized_collect_log': 'authorized_collect_log',
        'authorized_hda_upgrade': 'authorized_hda_upgrade',
        'apply_dedicated_standby_network_param': 'apply_dedicated_standby_network_param'
    }

    def __init__(self, ad_info=None, ad_domains=None, access_mode=None, dedicated_subnets=None, subnet_ids=None, internet_access_port=None, enterprise_id=None, is_send_email=None, dc_vnc_ip=None, authorized_collect_log=None, authorized_hda_upgrade=None, apply_dedicated_standby_network_param=None):
        """ModifyWorkspaceAttributesReq

        The model defined in huaweicloud sdk

        :param ad_info: 
        :type ad_info: :class:`huaweicloudsdkworkspace.v2.AdDomainInfo`
        :param ad_domains: 
        :type ad_domains: :class:`huaweicloudsdkworkspace.v2.AdDomain`
        :param access_mode: 接入模式。 - INTERNET：互联网接入。 - DEDICATED：专线接入。 - BOTH：代表两种接入方式都支持。
        :type access_mode: str
        :param dedicated_subnets: 专线接入网段列表，多个网段信息用分号隔开，列表长度不超过5。
        :type dedicated_subnets: str
        :param subnet_ids: 子网的网络ID列表。
        :type subnet_ids: list[str]
        :param internet_access_port: 互联网接入端口。
        :type internet_access_port: str
        :param enterprise_id: 企业ID。
        :type enterprise_id: str
        :param is_send_email: 桌面退订是否发送邮件通知。
        :type is_send_email: bool
        :param dc_vnc_ip: 开通专线访问VNC功能，如果传入的是default则自动创建，如果传入的自定义的dc_vnc_ip则直接使用，如果传入的是close表示关闭自定义VNC
        :type dc_vnc_ip: str
        :param authorized_collect_log: 是否授权收集日志。
        :type authorized_collect_log: bool
        :param authorized_hda_upgrade: 是否授权hda升级。
        :type authorized_hda_upgrade: bool
        :param apply_dedicated_standby_network_param: 
        :type apply_dedicated_standby_network_param: :class:`huaweicloudsdkworkspace.v2.ApplyDedicatedStandbyNetworkParam`
        """
        
        

        self._ad_info = None
        self._ad_domains = None
        self._access_mode = None
        self._dedicated_subnets = None
        self._subnet_ids = None
        self._internet_access_port = None
        self._enterprise_id = None
        self._is_send_email = None
        self._dc_vnc_ip = None
        self._authorized_collect_log = None
        self._authorized_hda_upgrade = None
        self._apply_dedicated_standby_network_param = None
        self.discriminator = None

        if ad_info is not None:
            self.ad_info = ad_info
        if ad_domains is not None:
            self.ad_domains = ad_domains
        if access_mode is not None:
            self.access_mode = access_mode
        if dedicated_subnets is not None:
            self.dedicated_subnets = dedicated_subnets
        if subnet_ids is not None:
            self.subnet_ids = subnet_ids
        if internet_access_port is not None:
            self.internet_access_port = internet_access_port
        if enterprise_id is not None:
            self.enterprise_id = enterprise_id
        if is_send_email is not None:
            self.is_send_email = is_send_email
        if dc_vnc_ip is not None:
            self.dc_vnc_ip = dc_vnc_ip
        if authorized_collect_log is not None:
            self.authorized_collect_log = authorized_collect_log
        if authorized_hda_upgrade is not None:
            self.authorized_hda_upgrade = authorized_hda_upgrade
        if apply_dedicated_standby_network_param is not None:
            self.apply_dedicated_standby_network_param = apply_dedicated_standby_network_param

    @property
    def ad_info(self):
        """Gets the ad_info of this ModifyWorkspaceAttributesReq.

        :return: The ad_info of this ModifyWorkspaceAttributesReq.
        :rtype: :class:`huaweicloudsdkworkspace.v2.AdDomainInfo`
        """
        return self._ad_info

    @ad_info.setter
    def ad_info(self, ad_info):
        """Sets the ad_info of this ModifyWorkspaceAttributesReq.

        :param ad_info: The ad_info of this ModifyWorkspaceAttributesReq.
        :type ad_info: :class:`huaweicloudsdkworkspace.v2.AdDomainInfo`
        """
        self._ad_info = ad_info

    @property
    def ad_domains(self):
        """Gets the ad_domains of this ModifyWorkspaceAttributesReq.

        :return: The ad_domains of this ModifyWorkspaceAttributesReq.
        :rtype: :class:`huaweicloudsdkworkspace.v2.AdDomain`
        """
        return self._ad_domains

    @ad_domains.setter
    def ad_domains(self, ad_domains):
        """Sets the ad_domains of this ModifyWorkspaceAttributesReq.

        :param ad_domains: The ad_domains of this ModifyWorkspaceAttributesReq.
        :type ad_domains: :class:`huaweicloudsdkworkspace.v2.AdDomain`
        """
        self._ad_domains = ad_domains

    @property
    def access_mode(self):
        """Gets the access_mode of this ModifyWorkspaceAttributesReq.

        接入模式。 - INTERNET：互联网接入。 - DEDICATED：专线接入。 - BOTH：代表两种接入方式都支持。

        :return: The access_mode of this ModifyWorkspaceAttributesReq.
        :rtype: str
        """
        return self._access_mode

    @access_mode.setter
    def access_mode(self, access_mode):
        """Sets the access_mode of this ModifyWorkspaceAttributesReq.

        接入模式。 - INTERNET：互联网接入。 - DEDICATED：专线接入。 - BOTH：代表两种接入方式都支持。

        :param access_mode: The access_mode of this ModifyWorkspaceAttributesReq.
        :type access_mode: str
        """
        self._access_mode = access_mode

    @property
    def dedicated_subnets(self):
        """Gets the dedicated_subnets of this ModifyWorkspaceAttributesReq.

        专线接入网段列表，多个网段信息用分号隔开，列表长度不超过5。

        :return: The dedicated_subnets of this ModifyWorkspaceAttributesReq.
        :rtype: str
        """
        return self._dedicated_subnets

    @dedicated_subnets.setter
    def dedicated_subnets(self, dedicated_subnets):
        """Sets the dedicated_subnets of this ModifyWorkspaceAttributesReq.

        专线接入网段列表，多个网段信息用分号隔开，列表长度不超过5。

        :param dedicated_subnets: The dedicated_subnets of this ModifyWorkspaceAttributesReq.
        :type dedicated_subnets: str
        """
        self._dedicated_subnets = dedicated_subnets

    @property
    def subnet_ids(self):
        """Gets the subnet_ids of this ModifyWorkspaceAttributesReq.

        子网的网络ID列表。

        :return: The subnet_ids of this ModifyWorkspaceAttributesReq.
        :rtype: list[str]
        """
        return self._subnet_ids

    @subnet_ids.setter
    def subnet_ids(self, subnet_ids):
        """Sets the subnet_ids of this ModifyWorkspaceAttributesReq.

        子网的网络ID列表。

        :param subnet_ids: The subnet_ids of this ModifyWorkspaceAttributesReq.
        :type subnet_ids: list[str]
        """
        self._subnet_ids = subnet_ids

    @property
    def internet_access_port(self):
        """Gets the internet_access_port of this ModifyWorkspaceAttributesReq.

        互联网接入端口。

        :return: The internet_access_port of this ModifyWorkspaceAttributesReq.
        :rtype: str
        """
        return self._internet_access_port

    @internet_access_port.setter
    def internet_access_port(self, internet_access_port):
        """Sets the internet_access_port of this ModifyWorkspaceAttributesReq.

        互联网接入端口。

        :param internet_access_port: The internet_access_port of this ModifyWorkspaceAttributesReq.
        :type internet_access_port: str
        """
        self._internet_access_port = internet_access_port

    @property
    def enterprise_id(self):
        """Gets the enterprise_id of this ModifyWorkspaceAttributesReq.

        企业ID。

        :return: The enterprise_id of this ModifyWorkspaceAttributesReq.
        :rtype: str
        """
        return self._enterprise_id

    @enterprise_id.setter
    def enterprise_id(self, enterprise_id):
        """Sets the enterprise_id of this ModifyWorkspaceAttributesReq.

        企业ID。

        :param enterprise_id: The enterprise_id of this ModifyWorkspaceAttributesReq.
        :type enterprise_id: str
        """
        self._enterprise_id = enterprise_id

    @property
    def is_send_email(self):
        """Gets the is_send_email of this ModifyWorkspaceAttributesReq.

        桌面退订是否发送邮件通知。

        :return: The is_send_email of this ModifyWorkspaceAttributesReq.
        :rtype: bool
        """
        return self._is_send_email

    @is_send_email.setter
    def is_send_email(self, is_send_email):
        """Sets the is_send_email of this ModifyWorkspaceAttributesReq.

        桌面退订是否发送邮件通知。

        :param is_send_email: The is_send_email of this ModifyWorkspaceAttributesReq.
        :type is_send_email: bool
        """
        self._is_send_email = is_send_email

    @property
    def dc_vnc_ip(self):
        """Gets the dc_vnc_ip of this ModifyWorkspaceAttributesReq.

        开通专线访问VNC功能，如果传入的是default则自动创建，如果传入的自定义的dc_vnc_ip则直接使用，如果传入的是close表示关闭自定义VNC

        :return: The dc_vnc_ip of this ModifyWorkspaceAttributesReq.
        :rtype: str
        """
        return self._dc_vnc_ip

    @dc_vnc_ip.setter
    def dc_vnc_ip(self, dc_vnc_ip):
        """Sets the dc_vnc_ip of this ModifyWorkspaceAttributesReq.

        开通专线访问VNC功能，如果传入的是default则自动创建，如果传入的自定义的dc_vnc_ip则直接使用，如果传入的是close表示关闭自定义VNC

        :param dc_vnc_ip: The dc_vnc_ip of this ModifyWorkspaceAttributesReq.
        :type dc_vnc_ip: str
        """
        self._dc_vnc_ip = dc_vnc_ip

    @property
    def authorized_collect_log(self):
        """Gets the authorized_collect_log of this ModifyWorkspaceAttributesReq.

        是否授权收集日志。

        :return: The authorized_collect_log of this ModifyWorkspaceAttributesReq.
        :rtype: bool
        """
        return self._authorized_collect_log

    @authorized_collect_log.setter
    def authorized_collect_log(self, authorized_collect_log):
        """Sets the authorized_collect_log of this ModifyWorkspaceAttributesReq.

        是否授权收集日志。

        :param authorized_collect_log: The authorized_collect_log of this ModifyWorkspaceAttributesReq.
        :type authorized_collect_log: bool
        """
        self._authorized_collect_log = authorized_collect_log

    @property
    def authorized_hda_upgrade(self):
        """Gets the authorized_hda_upgrade of this ModifyWorkspaceAttributesReq.

        是否授权hda升级。

        :return: The authorized_hda_upgrade of this ModifyWorkspaceAttributesReq.
        :rtype: bool
        """
        return self._authorized_hda_upgrade

    @authorized_hda_upgrade.setter
    def authorized_hda_upgrade(self, authorized_hda_upgrade):
        """Sets the authorized_hda_upgrade of this ModifyWorkspaceAttributesReq.

        是否授权hda升级。

        :param authorized_hda_upgrade: The authorized_hda_upgrade of this ModifyWorkspaceAttributesReq.
        :type authorized_hda_upgrade: bool
        """
        self._authorized_hda_upgrade = authorized_hda_upgrade

    @property
    def apply_dedicated_standby_network_param(self):
        """Gets the apply_dedicated_standby_network_param of this ModifyWorkspaceAttributesReq.

        :return: The apply_dedicated_standby_network_param of this ModifyWorkspaceAttributesReq.
        :rtype: :class:`huaweicloudsdkworkspace.v2.ApplyDedicatedStandbyNetworkParam`
        """
        return self._apply_dedicated_standby_network_param

    @apply_dedicated_standby_network_param.setter
    def apply_dedicated_standby_network_param(self, apply_dedicated_standby_network_param):
        """Sets the apply_dedicated_standby_network_param of this ModifyWorkspaceAttributesReq.

        :param apply_dedicated_standby_network_param: The apply_dedicated_standby_network_param of this ModifyWorkspaceAttributesReq.
        :type apply_dedicated_standby_network_param: :class:`huaweicloudsdkworkspace.v2.ApplyDedicatedStandbyNetworkParam`
        """
        self._apply_dedicated_standby_network_param = apply_dedicated_standby_network_param

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
        if not isinstance(other, ModifyWorkspaceAttributesReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
