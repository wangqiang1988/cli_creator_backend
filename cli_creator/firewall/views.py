from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from firewall.forti import FirewallConfigurator

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

        return Response(data)

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)