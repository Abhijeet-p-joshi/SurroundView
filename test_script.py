import win32com.client

canoe = win32com.client.Dispatch("CANoe.Application")

ns = canoe.System.Namespaces.Item("_SPACommon")

var = ns.Variables.Item("UBControl")

print("Current value =", var.Value)

var.Value = 3

print("Written 3")