import click
import time
from .ECSManager import ECSManager
from .VPCManager import VPCManager
from .ConfigManager import ConfigManager
from .ShellHelper import ShellHelper

class SqNetHelper:

    @staticmethod
    def setup(access_key, access_secret):
        config = ConfigManager()
        config.set_config(
            access_key=access_key,
            access_secret=access_secret
        )
        return "配置已保存"

    @staticmethod
    def list_instances():
        config = ConfigManager()
        if not config.is_configured():
            return "Error: 请先设置阿里云凭证"
        try:

            ecs_manager = ECSManager(config.access_key, config.access_secret, config.region)
            instances_result = ecs_manager.list_instances()

            if isinstance(instances_result, str) and instances_result.startswith('Error'):
                return instances_result

            if not isinstance(instances_result, dict):
                raise ValueError("Unexpected response from list_instances()")

            output = ["Available ECS Instances:"]
            for i, (instance_id, instance_info) in enumerate(instances_result.items(), start=1):
                public_ip = instance_info['PublicIpAddress'] or 'N/A'
                output.append(f"{i}. ID: {instance_id}, Name: {instance_info['Name']}, Public IP: {public_ip}, Status: {instance_info['Status']}")

            return "\n".join(output)
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def list_regions():
        config = ConfigManager()
        if not config.is_configured():
            return "Error: 请先设置阿里云凭证", None

        ecs_manager = ECSManager(config.access_key, config.access_secret, config.region)
        return ecs_manager.get_regions()


    @staticmethod
    def set_region(selected_region_id):

        config = ConfigManager()
        config.set_config(
            region=selected_region_id
        )

        ecs_manager = ECSManager(config.access_key, config.access_secret, config.region)
        zones = ecs_manager.get_zones()
        zone_id = zones[0]['ZoneId']
        config.set_config(
            zone_id=zone_id
        )

        SQLOG.info(f"zone_id: {zone_id}")

        vpcmanager = VPCManager(config.access_key, config.access_secret, config.region)

        security_group_id = None
        vpc_id = None
        vswitch_id = None

        if vpcmanager.is_security_group_exist(config.security_group_id):
            security_group_id = config.security_group_id
            SQLOG.info("发现安全组: ", security_group_id)
            pass
        else:
            security_group_id = vpcmanager.is_security_group_exist_with_name(config.security_group_name)
            if security_group_id:
                SQLOG.info("发现安全组: ", security_group_id)

        if security_group_id:
            vpc_id = vpcmanager.get_vpc_id_by_security_group_id(security_group_id)
            if vpc_id:
                SQLOG.info("发现专有网络: ", vpc_id)
                vswitch_id = vpcmanager.get_vswitche_id_by_vpc_id(vpc_id)
                if vswitch_id:
                    SQLOG.info("发现虚拟交换机: ", vswitch_id)
                else:
                    vswitch_id = vpcmanager.create_vswitch(vpc_id, zone_id) 
                    SQLOG.info("创建虚拟交换机成功: ", vswitch_id)

        if security_group_id and vpc_id and vswitch_id:
            pass 
        else:
            vpc_id = vpcmanager.is_vpc_exist_with_name(config.vpc_name)
            if not vpc_id:
                vpc_id = vpcmanager.create_vpc()
            if not vpc_id:
                SQLOG.info("创建专有网络失败！")
                return False

            SQLOG.info("创建专有网络成功: ", vpc_id)
            vswitch_id = vpcmanager.get_vswitche_id_by_vpc_id(vpc_id)
            if not vswitch_id:
                vswitch_id = vpcmanager.create_vswitch(vpc_id, zone_id) 
                pass
            if not vpc_id:
                SQLOG.info("创建虚拟交换机失败！")
                return False  

            SQLOG.info("创建虚拟交换机成功: ", vswitch_id)  
            security_group_id = vpcmanager.create_security_group(vpc_id)
            if not security_group_id:
                SQLOG.info("创建安全组失败！")
                return False
            SQLOG.info("创建安全组成功: ", security_group_id)

        if security_group_id:
            vpcmanager.add_security_group_rule(security_group_id)
                
        if security_group_id and vpc_id and vswitch_id:
            config.set_config(
                security_group_id=security_group_id,
                vpc_id=vpc_id,
                vswitch_id=vswitch_id
            )
            pass


        return True

    @staticmethod
    def create_instance():

        config = ConfigManager()
        if not config.is_configured():
            SQLOG.info("请先设置阿里云凭证")
            return None

        ecs_manager = ECSManager(config.access_key, config.access_secret, config.region)
        instance_details = ecs_manager.create_instance(config)

        instance_id = None
        if instance_details is None:
            SQLOG.info("创建实例失败")
            return None

        instance_id = instance_details['InstanceId']
        if instance_id is None:
            SQLOG.info("创建实例失败!")
            return None
        
        SQLOG.info("创建实例成功: ", instance_id)
        time.sleep(2) 
        # ECS绑定密码

        ret = ecs_manager.reset_instance_password(instance_id, config.instance_login_password)
        if not ret:
            SQLOG.info("设置实例密码失败")
            return None
        SQLOG.info("设置实例密码成功!")
        ssh_attach_ret = ecs_manager.attach_key_pair(instance_id, config.key_pair_name)
        if ssh_attach_ret :
            SQLOG.info("绑定ssh成功")
            pass

        # 分配公网 IP
        hostname = ecs_manager.allocate_public_ip(instance_id)
        if hostname is None:
            SQLOG.info("分配公网 IP 失败")
            return None
        SQLOG.info(f"分配公网IP成功: {hostname}")
        # 启动 ECS 实例
        ecs_manager.start_instance(instance_id)

        # 等待实例状态为 Running
        ecs_manager.wait_instance_status(instance_id, 'Running')
        SQLOG.info(f"Instance ID: {instance_id}, Hostname: {hostname}, password: {config.instance_login_password}")
        time.sleep(5)

        # 执行shell脚本
        command_array = ["wget https://get.vpnsetup.net -O vpn.sh && sudo VPN_IPSEC_PSK='"]
        command_array.append(config.vpn_psk)
        command_array.append("' VPN_USER='")
        command_array.append(config.vpn_name)
        command_array.append("' VPN_PASSWORD='")
        command_array.append(config.vpn_password)
        command_array.append("' sh vpn.sh")
        shell_script = "".join(command_array)
        

        
        file_path = None
        shell_result = False

        if ssh_attach_ret:
            # shell_result = ShellHelper.ssh_connect_and_execute_with_key(hostname, 'root', config.instance_login_password, shell_script)
            # if shell_result:
            #     time.sleep(1)
            #     remote_file_path = "/root/vpnclient.mobileconfig"
            #     local_file_path = "./vpnclient.mobileconfig"
            #     file_path = ShellHelper.ssh_download_file_with_password(hostname, 'root', config.instance_login_password, remote_file_path, local_file_path)
            # else:
            #     SQLOG.info("执行shell脚本失败")
            #     SQLOG.info(shell_script)
            pass
        else:
            shell_result = ShellHelper.ssh_connect_and_execute_with_password(hostname, 'root', config.instance_login_password, shell_script)
            if shell_result:
                time.sleep(1)
                remote_file_path = "/root/vpnclient.mobileconfig"
                local_file_path = "./vpnclient.mobileconfig"
                file_path = ShellHelper.ssh_download_file_with_password(hostname, 'root', config.instance_login_password, remote_file_path, local_file_path)
            else:
                SQLOG.info("执行shell脚本失败")
                SQLOG.info(shell_script)

        if shell_result:
            SQLOG.info(f"IP 地址: {hostname}")
            SQLOG.info(f"VPN Name: {config.vpn_name}")
            SQLOG.info(f"VPN Password: {config.vpn_password}")
            SQLOG.info(f"VPN PSK: {config.vpn_psk}")
            pass

        return f"Instance ID: {instance_id}, Hostname: {hostname}"
        
    @staticmethod
    def delete_instance():
        config = ConfigManager()
        if not config.is_configured():
            return "Error: 请先设置阿里云凭证", None

        try:
            ecs_manager = ECSManager(config.access_key, config.access_secret, config.region)
            instances_result = ecs_manager.list_instances()

            if isinstance(instances_result, str) and instances_result.startswith('Error'):
                return instances_result, None

            if not isinstance(instances_result, dict):
                raise ValueError("Unexpected response from list_instances()")

            output = ["Available ECS Instances:"]
            instances_choices = []
            for i, (instance_id, instance_info) in enumerate(instances_result.items(), start=1):
                instances_choices.append(instance_id)
                public_ip = instance_info['PublicIpAddress'] or 'N/A'
                output.append(f"{i}. ID: {instance_id}, Name: {instance_info['Name']}, Public IP: {public_ip}, Status: {instance_info['Status']}")

            return "\n".join(output), instances_choices

        except Exception as e:
            return f"Error: {str(e)}", None

    @staticmethod
    def confirm_delete_instance(choice, instances_choices):
        if choice < 1 or choice > len(instances_choices):
            return "Invalid choice. Please enter a valid number."

        instance_id_to_delete = instances_choices[choice - 1]
        config = ConfigManager()
        ecs_manager = ECSManager(config.access_key, config.access_secret, config.region)
        return ecs_manager.delete_instance(instance_id_to_delete)