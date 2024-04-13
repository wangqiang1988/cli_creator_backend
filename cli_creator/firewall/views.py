from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from firewall.forti import FirewallConfigurator
@api_view(['GET', 'POST'])  
def forticli(request):
    if request.method == 'POST':
        name = request.query_params.get('name')
        src_if = request.query_params.get('src_if')
        des_if = request.query_params.get('des_if')
        src_add = request.query_params.get('src_add')
        des_add = request.query_params.get('des_add')
        tcp_port = request.query_params.get('tcp_port')
        udp_port = request.query_params.get('udp_port')
        log = request.query_params.get('log')
        print(name, src_if, des_if, src_add, des_add, tcp_port, udp_port, log)
        config = FirewallConfigurator(name, src_if, des_if, src_add, des_add, tcp_port, udp_port, log)
        result_command = config.configure_address() + config.configre_port() + config.configure_policy()
        result_command_str = str(result_command)

        data = {
            'result': result_command_str,
            'message': 'Success'
        }

        return JsonResponse(data)

    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=400)

