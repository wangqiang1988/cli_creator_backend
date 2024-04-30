from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from firewall.forti import FirewallConfigurator
from firewall.juniper import j_creat_policy,j_address
from firewall.models import cli_logs, foodlist
from django.db.models import Count
from datetime import datetime, timedelta



def save_cli_logs(ip_address, time, info):
    obj = cli_logs(ip_address=ip_address, time=time, info=info)
    obj.save()


def food_add_log(userid, name, des, history, make, tips, time):
    obj = foodlist(userid=userid, name=name, des=des, history=history, make=make, tips=tips, time=time)
    obj.save()

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
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_info = "forticli_create"
        save_cli_logs(ip_address="127.0.0.1", time=current_date, info=log_info)
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
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_info = "forticli_modify"
        save_cli_logs(ip_address="127.0.0.1", time=current_date, info=log_info)
        return Response(data)

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)

@api_view(['GET', 'POST'])  
def juniper_policy_create(request):
    if request.method == 'POST':
        data = request.data  # 获取 JSON 格式的数据
        name = data.get('name')
        from_zone = data.get('from_zone')
        to_zone = data.get('to_zone')
        src_add = data.get('src_add')
        des_add = data.get('des_add')
        tcp_port = data.get('tcp_port')
        udp_port = data.get('udp_port')
        action = data.get('action')
        log = data.get('log')
        print(name, from_zone, to_zone, src_add, des_add, tcp_port, udp_port, log)
        # 调用相应的方法进行处理
        config = j_creat_policy(name, src_add, des_add, tcp_port, udp_port, from_zone, to_zone, action)
        result_command_str = str(config)

        data = {
            'result': result_command_str,
            'message': 'Success'
        }
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_info = "juniper_create"
        save_cli_logs(ip_address="127.0.0.1", time=current_date, info=log_info)
        return Response(data)
        

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)
    
@api_view(['GET', 'POST'])  
def juniper_address_create(request):
    if request.method == 'POST':
        data = request.data  # 获取 JSON 格式的数据
        address_list = data.get('address_list')
        # 调用相应的方法进行处理
        config = j_address(address_list)
        result_command_str = str(config)

        data = {
            'result': result_command_str,
            'message': 'Success'
        }
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_info = "juniper_address_create"
        save_cli_logs(ip_address="127.0.0.1", time=current_date, info=log_info)
        return Response(data)
        

    else:
        return Response({'message': 'Only POST requests are allowed'}, status=400)

@api_view(['GET', 'POST'])  
def food_add(request):
    if request.method == 'POST':
        data = request.data  # 获取 JSON 格式的数据
        userid = data.get('userid')
        name = data.get('name')
        des = data.get('des')
        history = data.get('history')
        make = data.get('make')
        tips = data.get('tips')

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(id, name, des, history, make, tips)
        try:
            food_add_log(userid, name, des, history, make, tips, current_date)
        # 调用相应的方法进行处理
            data = {
                'result': '已提交',
                'message': 'Success'
            }
            return Response(data)
        except:
            data = {
                'result': '提交失败',
                'message': 'Success'
            }
            return Response(data)
        
@api_view(['GET', 'POST'])  
def print_foodlist(request):
    # 获取foodlist模型的所有实例
    if request.method == 'POST':
        food_items = foodlist.objects.all()
        content =""
        
    # 遍历所有实例并打印它们的数据
        for food_item in food_items:
            print("Userid:", food_item.userid)
            print("Name:", food_item.name)
            print("Description:", food_item.des)
            print("History:", food_item.history)
            print("Make:", food_item.make)
            print("Tips:", food_item.tips)
            print("Time:", food_item.time)
            print("\n")  # 为了在输出中添加空行
            content+= str(food_item.userid+'\n'+food_item.name +'\n'+ food_item.des +'\n' + food_item.history +'\n' + food_item.make + '\n' + food_item.tips + '\n' + str(food_item.time) + '\n')
        
        data ={
            'result':content,
            'message':'Success'
            }

    # 返回一个简单的 HTTP 响应，内容为 "Data printed"，也可以根据需要返回其他内容
        return Response(data)