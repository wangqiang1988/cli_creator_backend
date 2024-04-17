from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from firewall.forti import FirewallConfigurator
from firewall.models import cli_logs
from django.db.models import Count
from datetime import datetime, timedelta

@api_view(['GET']) 
def logs_count(request):
    if request.method == 'GET':
        today = datetime.now().date()
    # 计算昨天的日期
        data_count_list=[]
        for i in range(0, 7):
    # 计算当前日期的前 i 天日期
            date = today - timedelta(days=6-i)
    
    # 查询当天的数据量
            data_count = cli_logs.objects.filter(time__date=date).count()
    
    # 打印结果
            print(f"前{i}天的数据量：", data_count)
            data_count_list.append(data_count)

        return Response(data_count_list)

@api_view(['GET', 'POST'])  
def forticli(request):
    if request.method == 'POST':
        data = request.data  # 获取 JSON 格式的数据

        # 从 JSON 数据中提取需要的字段
        name = data.get('name')
        src_if = data.get('src_if')
        des_if = data.get('des_if')
        src_add = data.get('src_add')
        des_add = data.get('des_add')
        tcp_port = data.get('tcp_port')
        udp_port = data.get('udp_port')
        log = data.get('log')

        print(name, src_if, des_if, src_add, des_add, tcp_port, udp_port, log)

        # 调用相应的方法进行处理
        config = FirewallConfigurator(name, src_if, des_if, src_add, des_add, tcp_port, udp_port, log)
        result_command = config.configure_address() + config.configre_port() + config.configure_policy()
        result_command_str = str(result_command)

        data = {
            'result': result_command_str,
            'message': 'Success'
        }
        obj = cli_logs(ip_address="127.0.0.1", time="2024-04-17", info="forticli_create")
        obj.save()
        return Response(data)
        

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)
    
@api_view(['GET', 'POST'])  
def forticli_modify(request):
    if request.method == 'POST':
        data = request.data  # 获取 JSON 格式的数据

        # 从 JSON 数据中提取需要的字段
        policy_id = data.get('policy_id')
        select = data.get('select')
        src_add = data.get('src_add')
        des_add = data.get('des_add')
        tcp_port = data.get('tcp_port')
        udp_port = data.get('udp_port')

        print(src_add, des_add, tcp_port, udp_port)

        # 调用相应的方法进行处理
        config = FirewallConfigurator('', '', '', src_add, des_add, tcp_port, udp_port, '')
        result_command = config.configure_address() + config.configre_port() + config.configure_policy_modify(policy_id, select)
        result_command_str = str(result_command)

        data = {
            'result': result_command_str,
            'message': 'Success'
        }
        obj = cli_logs(ip_address="127.0.0.1", time="2024-04-17", info="forticli_create")
        obj.save()
        return Response(data)

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)