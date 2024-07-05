import click

from .SqLog import SQLOG, LogLevel
from .SqNetHelper import SqNetHelper
from .ConfigManager import ConfigManager

SQLOG.set_log_level(LogLevel.DEBUG)
SQLOG.set_console_output()


@click.group()
def cli():
    pass


@cli.command()
@click.option('--access-key', prompt=True, help='阿里云Access Key')
@click.option('--access-secret', prompt=True, help='阿里云Access Secret')
@click.option('--verbose', is_flag=True, help='打印输出log')
def setup(access_key, access_secret):
    """设置阿里云账号凭证"""
    if verbose:
        SQLOG.set_log_level(LogLevel.DEBUG)
        pass
            
    result = SqNetHelper.setup(access_key, access_secret, verbose)
    click.echo(result)

    config = ConfigManager()
    if not config.is_configured():
        click.echo("Error: 请先设置阿里云凭证!")
        return False

    regions = SqNetHelper.list_regions()
    if not regions:
        click.echo("Error: 获取region列表失败!")
        return False

    region_dict = {region['RegionId']: region['LocalName'] for region in regions}
    output = ["Available regions:"]
    region_choices = []
    for i, (region_id, local_name) in enumerate(region_dict.items(), start=1):
        region_choices.append(region_id)
        output.append(f"{i}. {local_name} ({region_id})")

    click.echo("\n".join(output))
    if region_choices:
        choice = click.prompt("请选择需要操作的region序号：", type=int)
        if choice < 1 or choice > len(region_choices):
            click.echo("Error: 无效选择!")
            return False
        selected_region_id = region_choices[choice - 1]
        result = SqNetHelper.set_region(selected_region_id)
        if result:
            click.echo("设置region: 成功!")
        else:
            click.echo("设置region:{selected_region_id} 失败!")


@cli.command()
@click.option('--verbose', is_flag=True, help='打印输出log')
def list(verbose):
    """列出所有网络服务器"""
    if verbose:
        SQLOG.set_log_level(LogLevel.DEBUG)
        pass

    result = SqNetHelper.list_instances()
    click.echo(result)

@cli.command()
@click.option('--region', is_flag=True, help='配置region')
@click.option('--verbose', is_flag=True, help='打印输出log')
def config(region, verbose):
    """修改当前账号的网络配置"""
    if verbose:
        SQLOG.set_log_level(LogLevel.DEBUG)
        pass

    if region:
        config = ConfigManager()
        if not config.is_configured():
            click.echo("Error: 请先设置阿里云凭证!")
            return False

        regions = SqNetHelper.list_regions()
        if not regions:
            click.echo("Error: 获取region列表失败!")
            return False
        
        region_dict = {region['RegionId']: region['LocalName'] for region in regions}
        output = ["Available regions:"]
        region_choices = []
        for i, (region_id, local_name) in enumerate(region_dict.items(), start=1):
            region_choices.append(region_id)
            output.append(f"{i}. {local_name} ({region_id})")

        click.echo("\n".join(output))
        if region_choices:
            choice = click.prompt("请选择需要操作的region序号：", type=int)
            if choice < 1 or choice > len(region_choices):
                click.echo("Error: 无效选择!")
                return False
            selected_region_id = region_choices[choice - 1]
            result = SqNetHelper.set_region(selected_region_id)
            if result:
                click.echo("设置region: 成功!")
            else:
                click.echo("设置region:{selected_region_id} 失败!")


@cli.command()
def create():
    """创建网络服务器"""
    result = SqNetHelper.create_instance()
    click.echo(result)

@cli.command()
def delete():
    """删除网络服务器"""
    instances_list, instances_choices = SqNetHelper.delete_instance()
    click.echo(instances_list)

    if instances_choices:
        choice = click.prompt("Enter the number of the instance you want to delete", type=int)
        result = SqNetHelper.confirm_delete_instance(choice, instances_choices)
        click.echo(result)

@cli.command()
def delete_all():
    """删除当前所有资源"""

if __name__ == '__main__':
    cli()