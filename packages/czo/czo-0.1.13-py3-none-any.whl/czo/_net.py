import ipaddress
from ipaddress import IPv4Address, IPv6Address
from time import sleep
from typing import Any, Generator


class NetLib:

    @staticmethod
    def cidr(address: str, netmask_or_prefix: int | str) -> dict[str, Any] | ValueError:
        """
        根据指定的网络和前缀长度计算CIDR信息。

        Args:
        - network: 字符串，指定的网络地址，可以是IPv4或IPv6格式。
        - prefix: 整数，网络的前缀长度。

        Returns:
        - 字典，包含CIDR信息，包括主机数量、地址范围、网络地址、广播地址和子网掩码。
        - 如果参数无效，返回ValueError异常。

        Examples:
        >>> print(Net.cidr('192.168.1.0', 24))

        >>> print(Net.cidr('240e::0', 64))
        """

        try:
            ip_type: ipaddress.IPv6Network | ipaddress.IPv4Network = ipaddress.IPv6Network if ':' in address else ipaddress.IPv4Network
            cidr = ip_type(f'{address}/{netmask_or_prefix}')

            # 输出网络地址、子网掩码、广播地址等信息
            host_count = cidr.num_addresses - 2
            range = str(cidr.network_address + 1) + '-' + \
                str(cidr.broadcast_address - 1)
            network_address = str(cidr.network_address)
            broadcast_address = str(cidr.broadcast_address)
            netmask = str(cidr.netmask)
            prefixlen = cidr.prefixlen

            return {'host_count': host_count, 'range': range, 'network_address': network_address, 'broadcast_address': broadcast_address, 'prefixlen': prefixlen, 'netmask': netmask}

        except ValueError as e:
            return e

    @staticmethod
    def ipaddress_generator(number: int, max: int | None = None, is_ipv6: bool = False,  **kwargs) -> Generator[list[str], Any, None]:
        """
        生成指定数量的IP地址序列。

        Args:
        - number: 每次生成的IP地址数量。
        - max: 生成IP地址的最大数量, 为空时使用 number。
        - is_ipv6: 是否生成IPv6地址，默认生成IPv4地址。
        - **kwargs: 可选参数，用于指定IP地址的a、b、c、d、e、f、g、h初始值。

        Returns:
        - Generator: 生成器，每次返回number个IP地址组成的列表，直到生成max个IP地址为止。

        Examples:
        >>> for i in NetLib.ipaddress_generator(10, max=100):
        ...    print(";".join(map(lambda x: f"http://{x}", i)))

        >>> ip_list = [ip for sublist in NetLib.ipaddress_generator(10, a=100) for ip in sublist]

        """
        a: int = kwargs.get("a", 1)
        b: int = kwargs.get("b", 1)
        c: int = kwargs.get("c", 1)
        d: int = kwargs.get("d", 1)
        e: int = kwargs.get("e", 1)
        f: int = kwargs.get("f", 1)
        g: int = kwargs.get("g", 1)
        h: int = kwargs.get("h", 1)

        if max is None:
            max = number

        if is_ipv6 is False:
            a_range: int = 256
            b_range: int = 256
            c_range: int = 256
            d_range: int = 255
            ip_list: list = []
            count: int = 0
            for _ in range(1, max+1):
                ip_list.append(ipaddress.IPv4Address(
                    f"{a}.{b}.{c}.{d}").compressed)
                count += 1
                d += 1

                if d == d_range:
                    d = 1
                    c = c+1
                    if c == c_range:
                        c = 1
                        b = b+1
                        if b == b_range:
                            b = 1
                            a = a+1
                            if a == a_range:
                                a = 1

                if len(ip_list) % number == 0:
                    yield ip_list
                    ip_list = []
                if max == count and len(ip_list) != 0:
                    yield ip_list
        else:
            a_range: int = 65536
            b_range: int = 65536
            c_range: int = 65536
            d_range: int = 65536
            e_range: int = 65536
            f_range: int = 65536
            g_range: int = 65536
            h_range: int = 65536
            ip_list: list = []
            count: int = 0
            for _ in range(1, max+1):
                ip_list.append(ipaddress.IPv6Address(
                    f"{a:04x}:{b:04x}:{c:04x}:{d:04x}:{e:04x}:{f:04x}:{g:04x}:{h:04x}").compressed)
                count += 1
                h += 1

                if h == h_range:
                    h = 1
                    g = g+1
                    if g == g_range:
                        g = 1
                        f = f+1
                        if f == f_range:
                            f = 1
                            e = e+1
                            if e == e_range:
                                e = 1
                                d = d+1
                                if d == d_range:
                                    d = 1
                                    c = c+1
                                    if c == c_range:
                                        c = 1
                                        b = b+1
                                        if b == b_range:
                                            b = 1
                                            a = a+1
                                            if a == a_range:
                                                a = 1

                if len(ip_list) % number == 0:
                    yield ip_list
                    ip_list = []
                if max == count and len(ip_list) != 0:
                    yield ip_list

    @staticmethod
    def generate_ip_list(number: int, is_ipv6: bool = False, v6_exploded: bool = False, **kwargs) -> list[str]:
        """
        生成指定数量的IP地址字符串列表。

        Args:
        - number: 生成IP地址的数量。
        - is_ipv6: 指示是否生成IPv6地址。
        - v6_exploded: 指示生成的IPv6地址是否以展开格式表示。
        - kwargs: 可以提供额外的参数来定制IPv4或IPv6地址的起始值。

        Returns:
        - 一个包含生成的IP地址字符串的列表。

        Examples:
        >>> v4 = {
            "a": 192,
            "b": 168,
            "c": 1,
            "d": 1,
        }
        >>> print((NetLib.generate_ip_list(3, **v4)))


        >>> v6 = {
            "a": "240e",
            "b": "c0a8",
            "c": "1",
            "d": "1",
            "e": "1",
            "f": "1",
            "g": "1",
            "h": "1",
        }
        >>> print((NetLib.generate_ip_list(3, True, **v6)))

        """
        if is_ipv6:
            # 初始化IPv6的各个段的默认值
            a: int = int(kwargs.get("a", "2001"), 16)
            b: int = int(kwargs.get("b", "db8"), 16)
            c: int = int(kwargs.get("c", "0"), 16)
            d: int = int(kwargs.get("d", "42"), 16)
            e: int = int(kwargs.get("e", "0"), 16)
            f: int = int(kwargs.get("f", "8a2e"), 16)
            g: int = int(kwargs.get("g", "370"), 16)
            h: int = int(kwargs.get("h", "1"), 16)

            # 计算IPv6地址
            ipv6 = (a * 2 ** 112) + (b * 2 ** 96) + (c * 2 ** 80) + (d * 2 ** 64) + \
                (e * 2 ** 48) + (f * 2 ** 32) + \
                (g * 2 ** 16) + (h * 2 ** 0)

            # 根据参数生成对应的IP地址列表并返回
            if v6_exploded:
                return [ipaddress.IPv6Address(ipv6 + i).exploded for i in range(number)]
            return [ipaddress.IPv6Address(ipv6 + i).compressed for i in range(number)]

        # 初始化IPv4的各个字节的默认值
        a: int = kwargs.get("a", 1)
        b: int = kwargs.get("b", 0)
        c: int = kwargs.get("c", 0)
        d: int = kwargs.get("d", 1)
        # 计算IPv4地址
        ipv4 = (a * 2 ** 24) + (b * 2 ** 16) + (c * 2 ** 8) + (d * 2 ** 0)
        return [ipaddress.IPv4Address(ipv4 + i).compressed for i in range(number)]

    @staticmethod
    def ip_in_subnet(ip_str, subnet_str):
        """
        Examples:
        >>> ip = '2a00::110:133'
        >>> subnet = '2a00::110:0/120'

        >>> if ip_in_subnet(ip, subnet):
        ...     print(f"{ip} 在子网 {subnet} 内")
        ... else:
        ...     print(f"{ip} 不在子网 {subnet} 内")
        ...
        """

        # 将 IP 地址和子网掩码字符串转换为 IPv4Network 对象
        ip_network = ipaddress.ip_network(subnet_str)
        # 将 IP 地址字符串转换为 IPv4Address 对象
        ip_address = ipaddress.ip_address(ip_str)
        # 判断 IP 地址是否在子网内
        return ip_address in ip_network

    @staticmethod
    def ipv6_in_range(ip_str, start_str, end_str):
        """
        Examples:
        >>> ip = '2a00::110:133'
        >>> start = '2a00::110:13'
        >>> end = '2a00::110:133'

        >>> if ipv6_in_range(ip, start, end):
        ...    print(f"{ip} 在范围 {start} - {end} 内")
        ... else:
        ...    print(f"{ip} 不在范围 {start} - {end} 内")
        ...
        """

        # 将起始和结束地址字符串转换为 IPv6Address 对象
        start_address = ipaddress.ip_address(start_str)
        end_address = ipaddress.ip_address(end_str)
        # 将要判断的地址字符串转换为 IPv6Address 对象
        ip_address = ipaddress.ip_address(ip_str)
        # 判断地址是否在范围内
        return start_address <= ip_address <= end_address

        # 示例用法

    @staticmethod
    def mac_generator(number: int, max: int = 10, **kwargs) -> Generator[list, Any, None]:
        """
        生成MAC地址
        """
        a: int = kwargs.get("a", 255)
        b: int = kwargs.get("b", 255)
        c: int = kwargs.get("c", 255)
        d: int = kwargs.get("d", 1)
        e: int = kwargs.get("e", 1)
        f: int = kwargs.get("f", 1)
        a_range: int = 256
        b_range: int = 256
        c_range: int = 256
        d_range: int = 256
        e_range: int = 256
        f_range: int = 256
        count = 0
        mac_list = []
        for _ in range(1, max+1):
            mac_list.append(f"{a:02x}:{b:02x}:{c:02x}:{d:02x}:{e:02x}:{f:02x}")
            count += 1
            f += 1
            if f == f_range:
                f = 1
                e = e+1
                if e == e_range:
                    e = 1
                    d = d+1
                    if d == d_range:
                        d = 1
                        c = c+1
                        if c == c_range:
                            c = 1
                            b = b+1
                            if b == b_range:
                                b = 1
                                a = a+1
                                if a == a_range:
                                    a = 1
            if len(mac_list) % number == 0:
                yield mac_list
                mac_list = []
            if max == count and len(mac_list) != 0:
                yield mac_list
