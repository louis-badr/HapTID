from nicegui import ui, events

import serial
import struct
import time


ser = serial.Serial('COM3', 115200, timeout=1)
ser.close()

# Initialize variables
motor = 1
tone_freq = 170
tone_volume = 10
tone_duration = 2
noise_volume = 10
noise_duration = 3
clicks_volume = 10
clicks_nb = 1
clicks_spacing = 0.1

def play_tone():
    data = struct.pack('iiiff', motor, 1, tone_freq, tone_volume, tone_duration)
    ser.open()
    ser.write(data)
    ser.close()

def play_noise():
    data = struct.pack('iiiff', motor, 2, 0, noise_volume, noise_duration)
    ser.open()
    ser.write(data)
    ser.close()

def play_clicks():
    data = struct.pack('iiiff', motor, 3, clicks_nb, clicks_volume, clicks_spacing)
    ser.open()
    ser.write(data)
    ser.close()

@ui.page('/testing')
def testing():
    ui.icon('arrow_back').classes('text-5xl').on('click', lambda: ui.open('/'))
    with ui.column().classes('w-full items-center'):
        ui.toggle({1:'Finger',2:'Wrist'}, value=1).bind_value_to(globals(), 'motor')
        with ui.tabs() as tabs:
            ui.tab('Tone')
            ui.tab('White Noise')
            ui.tab('Clicks')
        with ui.tab_panels(tabs, value='Tone').classes('w-1/2'):
            with ui.tab_panel('Tone'):
                ui.label('Frequency (Hz)')
                tone_freq_slider = ui.slider(min=20, max=1000, step = 1, value=tone_freq).bind_value_to(globals(), 'tone_freq').props('label')
                ui.label('Volume (%)')
                tone_volume_slider = ui.slider(min=0, max=100, step = 0.001, value=tone_volume).bind_value_to(globals(), 'tone_volume').props('label')
                ui.label('Duration (s)')
                tone_duration_slider = ui.slider(min=0, max=30, step = 0.01, value=tone_duration).bind_value_to(globals(), 'tone_duration').props('label')
                ui.button('Start', on_click=lambda:play_tone()).classes('bg-red')
            with ui.tab_panel('White Noise'):
                ui.label('Volume (%)')
                noise_volume_slider = ui.slider(min=1, max=100, step = 1, value=noise_volume).bind_value_to(globals(), 'noise_volume').props('label')
                ui.label('Duration (s)')
                noise_duration_slider = ui.slider(min=0, max=30, step = 0.01, value=noise_duration).bind_value_to(globals(), 'noise_duration').props('label')
                ui.button('Start', on_click=lambda:play_noise()).classes('bg-red')
            with ui.tab_panel('Clicks'):
                ui.label('Volume (%)')
                clicks_volume_slider = ui.slider(min=1, max=100, step = 1, value=clicks_volume).bind_value_to(globals(), 'clicks_volume').props('label')
                ui.label('Number of clicks')
                clicks_nb_slider = ui.slider(min=1, max=10, step = 1, value=clicks_nb).bind_value_to(globals(), 'clicks_nb').props('label')
                ui.label('Spacing (s)')
                clicks_spacing_slider = ui.slider(min=0, max=3, step = 0.01, value=clicks_spacing).bind_value_to(globals(), 'clicks_spacing').props('label')
                ui.button('Start', on_click=lambda:play_clicks()).classes('bg-red')

@ui.page('/threshold')
def threshold():
    ui.icon('arrow_back').classes('text-5xl').on('click', lambda: ui.open('/'))

@ui.page('/')
def menu():
    with ui.column().classes('w-full items-center'):
        ui.label('Menu').classes('text-2xl font-bold')
        ui.button('Testing', on_click=lambda: ui.open('/testing'))
        ui.button('Thresholds detection', on_click=lambda: ui.open('/threshold'))

ui.run(title='HapticS - Demo', native=False)