import psutil


def get_stats() -> dict:
    try:
        cpu_temperature = psutil.sensors_temperatures(
            fahrenheit=False)["cpu_thermal"][0].current
    except:
        cpu_temperature = "N/A"

    try:
        cpu_load = int(psutil.cpu_percent())
    except:
        cpu_load = "N/A"

    try:
        ram_load = int(psutil.virtual_memory().percent)
    except:
        ram_load = "N/A"
    
    return {"cpu_temperature": cpu_temperature, "cpu_load": cpu_load, "ram_load": ram_load}