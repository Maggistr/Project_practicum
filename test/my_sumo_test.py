import os
import sys

# Правильный путь к SUMO
sumo_path = r"C:\Program Files (x86)\Eclipse\Sumo"
os.environ['SUMO_HOME'] = sumo_path

# Добавляем tools в путь
tools_path = os.path.join(sumo_path, 'tools')
if os.path.exists(tools_path):
    sys.path.append(tools_path)
    print(f"✅ Tools path найден: {tools_path}")
else:
    print(f"❌ Tools path НЕ найден: {tools_path}")

# Проверяем наличие sumo-gui.exe
sumo_binary_path = os.path.join(sumo_path, 'bin', 'sumo-gui.exe')
if os.path.exists(sumo_binary_path):
    print(f"✅ sumo-gui.exe найден: {sumo_binary_path}")
else:
    print(f"❌ sumo-gui.exe НЕ найден: {sumo_binary_path}")
    sys.exit(1)

# Теперь можно импортировать traci
import traci


# Создаем простые файлы конфигурации прямо в коде
def create_sumo_files():
    # Создаем папку для файлов если её нет
    files_dir = os.path.join(os.path.dirname(__file__), "sumo_files")
    os.makedirs(files_dir, exist_ok=True)

    # ИСПРАВЛЕННЫЙ .net.xml файл с правильным форматом
    net_file = os.path.join(files_dir, "simple.net.xml")
    with open(net_file, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<net version="1.16" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/net_file.xsd">
    <edge id="edge1" from="node1" to="node2" priority="1" numLanes="1" speed="13.89">
        <lane id="edge1_0" index="0" speed="13.89" length="500.00" shape="0.00,0.00 500.00,0.00"/>
    </edge>

    <junction id="node1" type="dead_end" x="0.00" y="0.00" incLanes="" intLanes="">
        <request index="0" response="0" foes="0" cont="0"/>
    </junction>
    <junction id="node2" type="dead_end" x="500.00" y="0.00" incLanes="edge1_0" intLanes="">
        <request index="0" response="0" foes="0" cont="0"/>
    </junction>
</net>''')

    # ИСПРАВЛЕННЫЙ .rou.xml файл
    rou_file = os.path.join(files_dir, "simple.rou.xml")
    with open(rou_file, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<routes>
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5" maxSpeed="50"/>
    <vehicle id="car1" type="car" depart="0">
        <route edges="edge1"/>
    </vehicle>
</routes>''')

    # .sumocfg файл
    cfg_file = os.path.join(files_dir, "simple.sumocfg")
    with open(cfg_file, 'w') as f:
        f.write('''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <input>
        <net-file value="simple.net.xml"/>
        <route-files value="simple.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="100"/>
    </time>
</configuration>''')

    return cfg_file


# Создаем файлы конфигурации
sumo_config = create_sumo_files()
print(f"✅ Конфигурационный файл создан: {sumo_config}")

# Используем полный путь к бинарнику
sumo_binary = sumo_binary_path

try:
    print(f"🚀 Запуск SUMO с конфигурацией: {sumo_config}")
    print(f"🚀 Исполняемый файл: {sumo_binary}")

    # Добавляем bin в PATH для Windows
    os.environ['PATH'] = os.path.join(sumo_path, 'bin') + ';' + os.environ.get('PATH', '')

    # Запускаем traci
    traci.start([sumo_binary, "-c", sumo_config, "--start", "--quit-on-end"])
    print("✅ SUMO успешно запущен!")

    # Делаем несколько шагов симуляции
    step = 0
    while step < 50:
        traci.simulationStep()
        vehicles = traci.vehicle.getIDList()
        if vehicles:
            print(f"Шаг {step}: ТС: {vehicles}")
        step += 1

except Exception as e:
    print(f"❌ Ошибка при запуске SUMO: {e}")
    import traceback

    traceback.print_exc()
finally:
    try:
        traci.close()
        print("✅ Симуляция завершена")
    except:
        pass
