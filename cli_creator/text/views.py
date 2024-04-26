from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from firewall.forti import FirewallConfigurator
from firewall.juniper import j_creat_policy
from firewall.models import cli_logs
from django.db.models import Count
from datetime import datetime, timedelta



def save_cli_logs(ip_address, time, info):
    obj = cli_logs(ip_address=ip_address, time=time, info=info)
    obj.save()


@api_view(['GET', 'POST'])  
def duplicates(request):
    if request.method == 'POST':
        data = request.data  # 获取 JSON 格式的数据
        text = data.get('src_text')
        unique_lines = []
        seen_lines = set()

        for line in text.splitlines():
        # 如果行不在集合中，则将其添加到列表和集合中
            if line not in seen_lines:
                seen_lines.add(line)
                unique_lines.append(line)

    # 将列表中的行重新连接成文本
        result = '\n'.join(unique_lines)

        data = {
            'result': 'Success',
            'message': result
        }
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_info = "text_duplicates"
        save_cli_logs(ip_address="127.0.0.1", time=current_date, info=log_info)
        return Response(data)
        

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)
    