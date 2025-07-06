import torch
import psutil

print("🔧 SYSTEM CHECK\n")

# CPU
cpu_usage = psutil.cpu_percent(interval=1)
print(f"🧠 CPU Usage: {cpu_usage}%")

# RAM
ram = psutil.virtual_memory()
print(f"💾 RAM Total: {round(ram.total / (1024 ** 3), 2)} GB")
print(f"💾 RAM Used: {round(ram.used / (1024 ** 3), 2)} GB")
print(f"💾 RAM Usage: {ram.percent}%")

# GPU
print("\n🎮 GPU INFO")
if torch.cuda.is_available():
    print("✅ CUDA is available")
    print(f"🧮 GPU Count: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"\n  🔹 GPU {i + 1}: {torch.cuda.get_device_name(i)}")
        props = torch.cuda.get_device_properties(i)
        print(f"     Total Memory: {round(props.total_memory / (1024 ** 3), 2)} GB")
        print(f"     Allocated:    {round(torch.cuda.memory_allocated(i) / (1024 ** 3), 2)} GB")
        print(f"     Reserved:     {round(torch.cuda.memory_reserved(i) / (1024 ** 3), 2)} GB")
else:
    print("❌ CUDA is NOT available")
    print("   Возможно, у вас нет NVIDIA GPU или не установлена поддержка CUDA.")
