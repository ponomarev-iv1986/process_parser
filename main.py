import os
import subprocess
from datetime import datetime
from typing import Any

BASE_DIR = os.path.dirname(__file__)


def get_system_processes() -> list[dict[str, Any]]:
    process_list = []
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    out = result.stdout.split("\n")[1:-1]
    for proc in out:
        process = proc.split()
        user = process[0]
        cpu = float(process[2])
        mem = float(process[3])
        name = process[10]
        process_dict = dict(user=user, cpu=cpu, mem=mem, name=name)
        process_list.append(process_dict)
    return process_list


def get_process_users(processes: list[dict[str, Any]]) -> list[str]:
    users = []
    for process in processes:
        if process["user"] not in users:
            users.append(process["user"])
    return users


def get_count_of_user_process(processes: list[dict[str, Any]]) -> dict[str, int]:
    user_processes = {}
    for process in processes:
        user_processes[process["user"]] = (
            user_processes.setdefault(process["user"], 0) + 1
        )
    return user_processes


def get_memories_list(processes: list[dict[str, Any]]) -> list[float]:
    process_memories = []
    for process in processes:
        process_memories.append(process["mem"])
    return process_memories


def get_cpu_list(processes: list[dict[str, Any]]) -> list[float]:
    process_memories = []
    for process in processes:
        process_memories.append(process["cpu"])
    return process_memories


def get_biggest_mem_process(processes: list[dict[str, Any]]) -> str:
    processes.sort(key=lambda process: process["mem"], reverse=True)
    return processes[0]["name"][-20:]


def get_biggest_cpu_process(processes: list[dict[str, Any]]) -> str:
    processes.sort(key=lambda process: process["cpu"], reverse=True)
    return processes[0]["name"][-20:]


def main():
    processes = get_system_processes()
    system_users = " ".join(get_process_users(processes))
    system_users_string = f"Пользователи системы: {system_users}\n"
    process_count_string = f"Процессов запущено: {len(processes)}\n\n"
    count_of_user_process_string = "Пользовательских процессов:\n"
    for k, v in get_count_of_user_process(processes).items():
        count_of_user_process_string = (
            count_of_user_process_string + k + ": " + str(v) + "\n"
        )
    memory_string = (
        f"Всего памяти используется: {round(sum(get_memories_list(processes)), 1)}%\n"
    )
    cpu_string = f"Всего CPU используется: {round(sum(get_cpu_list(processes)), 1)}%\n"
    biggest_memory_process_string = (
        f"Больше всего памяти использует: {get_biggest_mem_process(processes)}\n"
    )
    biggest_cpu_process_string = (
        f"Больше всего CPU использует: {get_biggest_cpu_process(processes)}"
    )
    return (
        "Отчёт о состоянии системы:\n"
        + system_users_string
        + process_count_string
        + count_of_user_process_string
        + "\n"
        + memory_string
        + cpu_string
        + biggest_memory_process_string
        + biggest_cpu_process_string
    )


if __name__ == "__main__":
    filename = str(datetime.now().strftime("%d-%m-%Y-%H:%M-scan"))
    print(main())
    with open(os.path.join(BASE_DIR, f"{filename}.txt"), "w", encoding="utf-8") as file:
        print(main(), file=file)
