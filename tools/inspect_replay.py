import win32com.client

app = win32com.client.Dispatch("CANoe.Application")

print("=" * 60)
print("Application")
print("=" * 60)

for name in dir(app):
    if "Replay" in name:
        print(name)

print("\n")

configuration = app.Configuration

print("=" * 60)
print("Configuration")
print("=" * 60)

for name in dir(configuration):
    if "Replay" in name:
        print(name)

print("\n")

measurement = app.Measurement

print("=" * 60)
print("Measurement")
print("=" * 60)

for name in dir(measurement):
    if "Replay" in name:
        print(name)

print("\n")

print("=" * 60)
print("Measurement attributes")
print("=" * 60)

for name in dir(measurement):
    if not name.startswith("_"):
        print(name)