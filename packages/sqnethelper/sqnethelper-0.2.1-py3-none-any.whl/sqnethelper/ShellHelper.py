
import time
import json
import base64
import paramiko
import sys

class ShellHelper:

    @staticmethod
    def ssh_connect_and_execute_with_password(hostname, username, password, command):
        # 创建 SSH 客户端对象
        client = paramiko.SSHClient()
        
        # 设置自动添加主机密钥策略
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        result = False
        try:
            # 连接到远程服务器
            client.connect(hostname=hostname, username=username, password=password)
            print(f"成功连接到 {hostname}")

            # 执行命令
            stdin, stdout, stderr = client.exec_command(command)
            
            # 实时输出结果
            while True:
                line = stdout.readline()
                if not line:
                    break
                print(line, end='')
            
            # 输出错误信息（如果有）
            for line in stderr:
                print(line, end='')

            # 获取命令执行的返回码
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("命令执行成功")
                result = True
            else:
                print(f"命令执行失败，退出状态码：{exit_status}")
        except paramiko.AuthenticationException:
            print("认证失败，请检查你的用户名和密码")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH连接失败: {str(ssh_exception)}")
        finally:
            # 关闭连接
            client.close()
            return result

    @staticmethod
    def ssh_download_file_with_password(hostname, username, password, remote_file_path, local_file_path):
        # 创建SSH客户端对象
        ssh_client = paramiko.SSHClient()
        
        # 设置自动添加主机密钥策略
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        result = None
        try:
            # 连接到远程服务器
            ssh_client.connect(hostname=hostname, username=username, password=password)
            print(f"成功连接到 {hostname}")
            # 创建SFTP客户端对象
            sftp_client = ssh_client.open_sftp()
            # 下载文件
            sftp_client.get(remote_file_path, local_file_path)
            result = local_file_path
            print(f"文件成功下载到: {local_file_path}")

        except paramiko.AuthenticationException:
            print("认证失败，请检查你的用户名和密码")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH连接失败: {str(ssh_exception)}")
        except IOError as io_error:
            print(f"文件传输错误: {str(io_error)}")
        finally:
            # 关闭SFTP连接
            if 'sftp_client' in locals():
                sftp_client.close()
            # 关闭SSH连接
            ssh_client.close()
            return result 

    @staticmethod
    def ssh_connect_and_execute_with_key(hostname, username, private_key_path, command):
        # 创建 SSH 客户端对象
        client = paramiko.SSHClient()
        
        # 设置自动添加主机密钥策略
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        result = False
        try:
            # 连接到远程服务器
            client.connect(hostname=hostname, username=username, key_filename=private_key_path)
            print(f"成功连接到 {hostname}")

            # 执行命令
            stdin, stdout, stderr = client.exec_command(command)
            
            # 实时输出结果
            while True:
                line = stdout.readline()
                if not line:
                    break
                print(line, end='')
            
            # 输出错误信息（如果有）
            for line in stderr:
                print(line, end='')

            # 获取命令执行的返回码
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("命令执行成功")
            else:
                print(f"命令执行失败，退出状态码：{exit_status}")

        except paramiko.AuthenticationException:
            print("认证失败，请检查你的用户名和密钥")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH连接失败: {str(ssh_exception)}")
        finally:
            # 关闭连接
            client.close()
            return result 

    @staticmethod
    def ssh_download_file_with_key(hostname, username, private_key_path, remote_file_path, local_file_path):
        # 创建SSH客户端对象
        ssh_client = paramiko.SSHClient()
        
        # 设置自动添加主机密钥策略
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        result = None
        try:
            # 连接到远程服务器
            ssh_client.connect(hostname=hostname, username=username, key_filename=private_key_path)
            print(f"成功连接到 {hostname}")

            # 创建SFTP客户端对象
            sftp_client = ssh_client.open_sftp()
            
            # 下载文件
            sftp_client.get(remote_file_path, local_file_path)
            
            print(f"文件成功下载到: {local_file_path}")
            result = local_file_path
        except paramiko.AuthenticationException:
            print("认证失败，请检查你的用户名和密钥")
        except paramiko.SSHException as ssh_exception:
            print(f"SSH连接失败: {str(ssh_exception)}")
        except IOError as io_error:
            print(f"文件传输错误: {str(io_error)}")
        finally:
            # 关闭SFTP连接
            if 'sftp_client' in locals():
                sftp_client.close()
            # 关闭SSH连接
            ssh_client.close()
            return result

