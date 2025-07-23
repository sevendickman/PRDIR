import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

# 设置随机种子，确保结果可复现
np.random.seed(42)
random.seed(42)

# 创建数据目录（如果不存在）
os.makedirs('d:\\数智化测试数据\\data723\\data', exist_ok=True)

# 生成日期范围（半年数据）
start_date = datetime.now() - timedelta(days=180)
date_range = [start_date + timedelta(days=i) for i in range(180)]

# 地铁线路
lines = ['1号线', '2号线', '3号线', '4号线', '5号线', '6号线', '7号线', '8号线', '9号线', '14号线', '21号线']

# 生成基础数据
data = []
for date in date_range:
    for line in lines:
        # 基础客流量（10,000 - 80,000）
        base_passengers = np.random.randint(10000, 80000)
        # 添加随机波动
        passengers = int(base_passengers * (1 + np.random.normal(0, 0.1)))
        
        # 票务收入（人均4元）
        ticket_income = passengers * 4 * (1 + np.random.normal(0, 0.05))
        
        # 运营成本（收入的60-80%）
        operation_cost = ticket_income * np.random.uniform(0.6, 0.8)
        
        # 维护费用（收入的10-20%）
        maintenance_cost = ticket_income * np.random.uniform(0.1, 0.2)
        
        # 计算其他收入 (票务收入的5-15%)
        other_income = ticket_income * np.random.uniform(0.05, 0.15)
        total_revenue = ticket_income + other_income
        
        # 拆分运营成本为固定成本和变动成本
        fixed_cost_ratio = np.random.uniform(0.4, 0.6)
        fixed_cost = operation_cost * fixed_cost_ratio
        variable_cost = operation_cost * (1 - fixed_cost_ratio)
        total_cost = fixed_cost + variable_cost + maintenance_cost
        net_profit = total_revenue - total_cost
        
        # 准点率 (95-100%，偶尔异常)
        punctuality_rate = np.random.uniform(0.95, 1.0) if np.random.random() > 0.02 else np.random.uniform(0.8, 0.95)
        
        # 能耗 (与客流量相关)
        energy_consumption = passengers * np.random.uniform(0.5, 2.0)
        
        # 平均票价
        average_ticket_price = ticket_income / passengers if passengers > 0 else 0
        
        # 日期相关字段
        day_of_week = date.weekday()  # 0=周一, 6=周日
        month = date.month
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'line': line,
            'passengers': passengers,
            'ticket_income': round(ticket_income, 2),
            'other_income': round(other_income, 2),
            'total_revenue': round(total_revenue, 2),
            'fixed_cost': round(fixed_cost, 2),
            'variable_cost': round(variable_cost, 2),
            'maintenance_cost': round(maintenance_cost, 2),
            'total_cost': round(total_cost, 2),
            'net_profit': round(net_profit, 2),
            'punctuality_rate': round(punctuality_rate, 4),
            'energy_consumption': round(energy_consumption, 2),
            'average_ticket_price': round(average_ticket_price, 2),
            'day_of_week': day_of_week,
            'month': month
        })

# 转换为DataFrame
df = pd.DataFrame(data)

# 随机插入缺失值（约2%的数据）
for col in ['passengers', 'ticket_income', 'other_income', 'total_revenue', 'fixed_cost', 'variable_cost', 'maintenance_cost', 'total_cost', 'net_profit', 'punctuality_rate', 'energy_consumption', 'average_ticket_price']:
    # 随机选择5%的行设置为缺失值
    mask = np.random.choice([True, False], size=len(df), p=[0.05, 0.95])
    df.loc[mask, col] = np.nan

# 随机插入异常值（约1%的数据）
# 1. 异常高客流量
mask = np.random.choice([True, False], size=len(df), p=[0.01, 0.99])
df.loc[mask, 'passengers'] = df.loc[mask, 'passengers'] * 3

# 2. 负收入
mask = np.random.choice([True, False], size=len(df), p=[0.005, 0.995])
df.loc[mask, 'ticket_income'] = -df.loc[mask, 'ticket_income']

# 保存为CSV文件
df.to_csv('d:\\数智化测试数据\\data723\\data\\subway_operation_data_v2.csv', index=False, encoding='utf-8-sig')
print('数据生成完成，已保存至 data/subway_operation_data_v2.csv')