import json
import time
import base64
import paramiko
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkecs.request.v20140526.CreateInstanceRequest import CreateInstanceRequest
from aliyunsdkecs.request.v20140526.StartInstanceRequest import StartInstanceRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.StopInstanceRequest import StopInstanceRequest
from aliyunsdkecs.request.v20140526.DeleteInstanceRequest import DeleteInstanceRequest
from aliyunsdkecs.request.v20140526.CreateCommandRequest import CreateCommandRequest
from aliyunsdkecs.request.v20140526.InvokeCommandRequest import InvokeCommandRequest
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
# from aliyunsdkecs.request.v20140526.DescribeZoneInfoRequest import DescribeZoneInfoRequest
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
from aliyunsdkecs.request.v20140526.AllocatePublicIpAddressRequest import AllocatePublicIpAddressRequest
from aliyunsdkecs.request.v20140526.DescribeAvailableResourceRequest import DescribeAvailableResourceRequest
from aliyunsdkecs.request.v20140526.ModifyInstanceAttributeRequest import ModifyInstanceAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest, DescribePriceRequest
from aliyunsdkecs.request.v20140526 import AttachKeyPairRequest

from aliyunsdkecs.request.v20140526 import CreateImageRequest, DescribeImagesRequest, DeleteImageRequest

from .ConfigManager import ConfigManager

class ECSManager:

    def __init__(self, access_key, access_secret, region):
        self.client = AcsClient(access_key, access_secret, region)

    def get_regions(self):
        try:
            describe_regions_request = DescribeRegionsRequest()
            describe_regions_request.set_action_name('DescribeRegions')
            describe_regions_response = self.client.do_action_with_exception(describe_regions_request)
            # print(json.loads(describe_regions_response))
            regions = json.loads(describe_regions_response)['Regions']['Region']
            if not regions:
                return {}
            return regions
        except Exception as e:
            print(f"get_regions: {str(e)}")
            return None

    def get_zones(self):
        try:
            describe_regions_request = DescribeZonesRequest()
            describe_regions_request.set_action_name('DescribeZones')
            describe_regions_response = self.client.do_action_with_exception(describe_regions_request)

            zones = json.loads(describe_regions_response)['Zones']['Zone']

            if not zones:
                return {}

            return zones

        except Exception as e:
            print(f"get_zones: {str(e)}")
            return None

    def list_instances(self):
        try:
            describe_instances_request = DescribeInstancesRequest()
            describe_instances_request.set_PageSize(10)
            describe_instances_response = self.client.do_action_with_exception(describe_instances_request)
            instances = json.loads(describe_instances_response)['Instances']['Instance']

            if not instances:
                return {}

            instance_dict = {}
            for instance in instances:
                instance_id = instance['InstanceId']
                instance_dict[instance_id] = {
                    'Name': instance['InstanceName'],
                    'Status': instance['Status'],
                    'PublicIpAddress': 'N/A'
                }
                if instance.get('PublicIpAddress', {}).get('IpAddress', ['']):
                    instance_dict[instance_id]['PublicIpAddress'] = instance.get('PublicIpAddress', {}).get('IpAddress', [''])[0]  # 获取公网IP
            return instance_dict

        except Exception as e:
            print(f"list_instances Error: {str(e)}")
            return None

    def create_instance(self, config):

        request = CreateInstanceRequest()
        request.set_InstanceType(config.instance_type)
        request.set_ImageId(config.image_id)
        request.set_SecurityGroupId(config.security_group_id)
        request.set_VSwitchId(config.vswitch_id)
        time_str = time.strftime('%m%d-%H-%M-%S', time.localtime())
        instance_name = config.instance_name + f"{time_str}"
        request.set_InstanceName(instance_name)
        request.set_InternetChargeType(config.internet_charge_type)
        # request.set_IoOptimized('optimized')
        request.set_SystemDiskCategory(config.instance_disk_category)
        request.set_SystemDiskSize(config.instance_disk_size)  
        request.set_InternetMaxBandwidthOut(config.internet_bandwidth_out)  
        request.set_InternetMaxBandwidthIn(config.internet_bandwidth_in)  
        try:
            response = self.client.do_action_with_exception(request)
            instance_details = json.loads(response)
            return instance_details

        except Exception as e:
            print(f"create_instance Error: {str(e)}")
            return None

    def start_instance(self, instance_id):
        try:
            request = StartInstanceRequest()
            request.set_InstanceId(instance_id)
            response = self.client.do_action_with_exception(request)
            return f"Starting instance {instance_id}..."
        
        except Exception as e:
            return f"Error starting instance {instance_id}: {str(e)}"

    def stop_instance(self, instance_id):
        print(f"stop_instance ...")   
        try:
            request = StopInstanceRequest()
            request.set_InstanceId(instance_id)
            response = self.client.do_action_with_exception(request)
            return f"Stopping instance {instance_id}..."
        
        except Exception as e:
            return f"Error stopping instance {instance_id}: {str(e)}"

    def delete_instance(self, instance_id):
        try:
            instance_status = self.get_instance_status(instance_id)
            if instance_status == 'Stopped':
                print(f"Instance {instance_id} is already stopped.")    
            elif instance_status == 'Stopping':
                time.sleep(3) 
                print(f"Instance {instance_id} is Stopping ...")    
            elif instance_status == 'Running':
                self.stop_instance(instance_id)  
                time.sleep(3) 
            # 等待实例停止

            self.wait_instance_status(instance_id, 'Stopped')

            # 删除ECS实例
            request = DeleteInstanceRequest()
            request.set_InstanceId(instance_id)
            response = self.client.do_action_with_exception(request)
            return f"Deleting instance {instance_id}..."
        
        except Exception as e:
            return f"Error deleting instance {instance_id}: {str(e)}"

    def allocate_public_ip(self, instance_id):
        request = AllocatePublicIpAddressRequest()
        request.set_accept_format('json')
        request.set_InstanceId(instance_id)

        try:
            response = self.client.do_action_with_exception(request)
            result = json.loads(response)
            return result['IpAddress']

        except (ClientException, ServerException) as e:
            print(f"Error allocating public IP: {str(e)}")
            return None

    def get_available_disk_categories(self, region_id, instance_type):
        request = DescribeAvailableResourceRequest()
        request.set_accept_format('json')
        request.set_DestinationResource("SystemDisk")
        request.set_InstanceType(instance_type)
        
        # 使用 add_query_param 方法设置 RegionId
        request.add_query_param('RegionId', region_id)
        
        try:
            response = self.client.do_action_with_exception(request)
            resources = json.loads(response)
            
            available_categories = []
            for resource in resources.get('AvailableZones', []):
                for available_resource in resource.get('AvailableResources', []):
                    for support_resource in available_resource.get('SupportedResources', []):
                        if support_resource.get('Value'):
                            available_categories.append(support_resource['Value'])
            
            return list(set(available_categories))  # 去重
        except Exception as e:
            print(f"Error querying available resources: {str(e)}")
            return []

    def attach_key_pair(instance_id, key_pair_name):
        
        # 创建请求对象
        request = AttachKeyPairRequest.AttachKeyPairRequest()
        
        # 设置参数
        request.set_InstanceIds([instance_id])  # 可以是单个实例ID，也可以是多个实例ID的列表
        request.set_KeyPairName(key_pair_name)
        try:
            # 发送请求
            response = self.client.do_action_with_exception(request)
            return True
        except Exception as e:
            print(f"绑定SSH密钥时发生错误: {str(e)}")
            return False

    def reset_instance_password(self, instance_id, new_password):
        request = ModifyInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_InstanceId(instance_id)
        request.set_Password(new_password)

        try:
            response = self.client.do_action_with_exception(request)
            return new_password
        except Exception as e:
            print(f"reset_instance_password Error: {str(e)}")
            return None


    def wait_instance_status(self, instance_id, status):
        # status = 'Running'/'Stopped'
        try:
            while True:
                current_status = self.get_instance_status(instance_id)
                if current_status == status:
                    print(f'Instance {instance_id} is {status}.')
                    break
                print(f'Waiting for instance {instance_id} to be in a {status} state...')
                time.sleep(5)
        except Exception as e:
            raise e

    def get_instance_status(self, instance_id):
        try:
            request = DescribeInstancesRequest()
            request.set_InstanceIds(instance_id)
            request.set_InstanceIds(json.dumps([instance_id]))
            response = self.client.do_action_with_exception(request)
            instances = json.loads(response)['Instances']['Instance']
            if instances:
                return instances[0]['Status']
            return None
        except Exception as e:
            raise e

    def run_command(self, instance_id, command):
        request = RunCommandRequest()
        request.set_Type("RunShellScript")
        request.set_CommandContent(command)
        request.set_InstanceIds([instance_id])

        response = self.client.do_action_with_exception(request)
        invoke_id = json.loads(response)['InvokeId']
        return invoke_id

    def get_command_output(self, invoke_id):
        request = DescribeInvocationResultsRequest()
        request.set_InvokeId(invoke_id)
        
        while True:
            response = self.client.do_action_with_exception(request)
            result = json.loads(response)['Invocation']['InvocationResults']['InvocationResult'][0]
            if result['InvokeRecordStatus'] == 'Finished':
                # 解码Base64编码的输出
                decoded_output = base64.b64decode(result['Output']).decode('utf-8')
                return decoded_output
            time.sleep(10)

    def create_image(self, instance_id, image_name, image_description=''):
        request = CreateImageRequest.CreateImageRequest()
        request.set_InstanceId(instance_id)
        request.set_ImageName(image_name)
        request.set_Description(image_description)

        try:
            response = client.do_action_with_exception(request)
            image_id = json.loads(response)['ImageId']
            print(f"镜像创建成功，镜像ID: {image_id}")
            return image_id
        except Exception as e:
            print(f"创建镜像时发生错误: {str(e)}")
            return None

    def is_image_exist(self, image_name):
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_ImageName(image_name)
        request.set_Status("Available")

        try:
            response = client.do_action_with_exception(request)
            images = json.loads(response)['Images']['Image']
            return len(images) > 0
        except Exception as e:
            print(f"检查镜像是否存在时发生错误: {str(e)}")
            return False

    def delete_image(self, image_id):
        request = DeleteImageRequest.DeleteImageRequest()
        request.set_ImageId(image_id)

        try:
            response = client.do_action_with_exception(request)
            print(f"镜像 {image_id} 删除成功")
            return True
        except Exception as e:
            print(f"删除镜像时发生错误: {str(e)}")
            return False

    def list_custom_images(self):
        client = AcsClient(access_key_id, access_key_secret, region_id)

        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_ImageOwnerAlias('self')  # 只列出自定义镜像
        request.set_Status("Available")  # 只列出可用的镜像
        request.set_PageSize(100)  # 每页显示的镜像数量，最大100

        custom_images = []
        page_number = 1

        while True:
            request.set_PageNumber(page_number)
            try:
                response = client.do_action_with_exception(request)
                images = json.loads(response)
                
                for image in images['Images']['Image']:
                    custom_images.append({
                        'ImageId': image['ImageId'],
                        'ImageName': image['ImageName'],
                        'CreationTime': image['CreationTime'],
                        'Size': image['Size']
                    })
                
                if len(custom_images) >= images['TotalCount']:
                    break
                
                page_number += 1
            except Exception as e:
                print(f"获取自定义镜像列表时发生错误: {str(e)}")
                break

        return custom_images