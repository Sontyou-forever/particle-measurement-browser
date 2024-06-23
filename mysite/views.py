from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse

def generate_dummy_data():
    date_range = pd.date_range(start='2023-01-01', end='2023-12-31')
    values = np.random.randint(50, 200, size=len(date_range))
    data = pd.DataFrame({'Date': date_range, 'Value': values})
    return data

def index(request):
    current_data = generate_dummy_data()
    previous_data = generate_dummy_data()
    
    current_data['Date'] = pd.to_datetime(current_data['Date'])
    previous_data['Date'] = pd.to_datetime(previous_data['Date'])
    current_data.set_index('Date', inplace=True)
    previous_data.set_index('Date', inplace=True)

    today = pd.to_datetime("2023-06-23")
    same_day_last_year = today - pd.DateOffset(years=1)

    current_day_data = current_data.loc[today.strftime('%Y-%m-%d')]
    previous_day_data = previous_data.loc[same_day_last_year.strftime('%Y-%m-%d')]

    plt.figure(figsize=(10, 5))
    plt.plot(current_day_data.index, current_day_data['Value'], label='Current Year')
    plt.plot(previous_day_data.index, previous_day_data['Value'], label='Last Year')
    plt.xlabel('Time')
    plt.ylabel('Measurement Value')
    plt.title('Particle Measurement Comparison')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')
