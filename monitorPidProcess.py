import time, os,sys, psutil


def banner(c1,c2):
    banner = f'''
        {c1}
            ▄▄▄              ▪
            ▀▄ █·▪     ▪    ▄██
            ▐▀▀▄  ▄█▀▄  ▄█▀▄ ▐█·
            ▐█•█▌▐█▌.▐▌▐█▌.▐▌▐█▌
            .▀  ▀ ▀█▄▀▪ ▀█▄▀▪▀▀▀

                  Monitor{c2}
    '''
    print(banner)
    pass


gr = "\033[1;32m"
rd = "\033[1;31m"
r  = "\033[0m"


def getProcessesInfo(appNames):
    processes = []
    appStatus = {appName: f'{rd}off{r}' for appName in appNames}

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            if proc.info['name'] in appNames:
                procInfo = proc.info
                processes.append(procInfo)
                appStatus[procInfo['name']] = f'{gr}on{r}'
                pass
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        pass

    return processes, appStatus

def cpu_percents():
    return psutil.cpu_percent()


def get_disk():
    divi = " / "
    disk_usage = psutil.disk_usage("/")
    return disk_usage
def to_gb(byte):
    return byte / 1024**3


def get_ram_usage():
    real_memory = int(psutil.virtual_memory().total - psutil.virtual_memory().available)
    return real_memory


def get_ram_memory():
    memory_usage = int(psutil.virtual_memory().total)
    return memory_usage


def get_cpu_temp():
    cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0]
    return cpu_temp.current


def status_server():
    print("\nStatus do servidor:")
    print(f"{gr}RAM: {int(get_ram_usage() / 1024 / 1024 )} / {int(get_ram_memory() / 1024 /1024):<10} DISK: {to_gb(get_disk().used):<1.2f}Gb / {to_gb(get_disk().free):<1.2f}Gb : {to_gb(get_disk().total):<1.2f}Gb{r}{gr:<10} CPU: {cpu_percents()} : {get_cpu_temp():<1.1f}°C {r}")
    pass


def displayProcessesInfo(processes, appStatus):
    os.system('clear')
    print('Status dos aplicativos: ')
    for appName, status in appStatus.items():
        print(f"{appName:<25} {status}")
        pass
    status_server()
    print("\nDetalhes dos processos:\n")

    if processes:
        print(f"{gr}{'PID':<8} {'Name':<25} {'User':<15} {'CPU%':<10} {'Memory%':<10}{r}")
            #print("="*69)
        for proc in processes:
            print(f"{proc['pid']:<8} {proc['name']:<25} {proc['username']:<15} {proc['cpu_percent']:<10.2f} {proc['memory_percent']:<10.2f}")
            pass
        pass
    else:
        print("Nenhum dos aplicativos especificados está em execução.")
        pass
    pass


def execute():
    banner(gr,r)
    time.sleep(1)
    appNames = []
    set_elemento = int(input(f"Quantidade de elementos {gr}>>{r} "))
    for i in range(0, set_elemento):
        app = input(f"Nome do app {gr}>>{r} ")
        appNames.append(app)
        pass
    try:
        while True:
            processes, appStatus = getProcessesInfo(appNames)
            displayProcessesInfo(processes, appStatus)
            time.sleep(0.1)
    except KeyboardInterrupt:
        banner(rd,r)
        print(f"{rd} Monitoramento interropido pelo usuário.{r}")
        pass
    pass


def main():
    execute()
    pass


if __name__ == '__main__':
    main()
    pass
