import frida
import time
import argparse


def selectDevice():
	enum_devices = frida.enumerate_devices()
	time.sleep(1)
	devices = []
	counter = 1
	for device in enum_devices:
		print("(\x1b[0;34m{counter}\x1b[0;0m)\tName: \x1b[0;32m{name}\x1b[0;0m\t- Type: \x1b[0;31m{type}\x1b[0;0m\t- Id: \x1b[0;35m{id}\x1b[0;0m".format(counter=counter, name=device.name, type=device.type, id=device.id))
		counter += 1
		devices.append(device)
	print("\n(\x1b[0;34m000\x1b[0;0m)\tExit.")

	if (len(devices) == 0):
		print("\x1b[0;34m\n[-] No device found. Exit\x1b[0;0m")
		exit(0)

	while True:
		try:
			choose = input("\x1b[0;34m\n Select Device > ")
			if choose == "000":
				exit("\x1b[0;0m")
			elif not (0 < int(choose) <= len(devices)):
				print ("\x1b[0;31m\n[-] {} is not in list\x1b[0;0m".format(choose))
			else:
				break
		except ValueError:
			print("\x1b[0;31m\n[-] Error value. Input is not a number\x1b[0;0m")

	print("\x1b[0;0m")
	return devices[int(choose)-1]


def selectApplication(Device):
	print("\n\x1b[0;0m")
	applications = Device.enumerate_applications()
	PackageName = []
	counter = 1

	for app in applications:
		print("(\x1b[0;34m{counter}\x1b[0;0m)\tIdentifier: \x1b[0;31m{id}\x1b[0;0m (\x1b[0;32m{name}\x1b[0;0m)".format(counter=counter, id=app.identifier, name=app.name))
		counter += 1
		PackageName.append(app)
	print("\n(\x1b[0;34m000\x1b[0;0m)\tExit.")

	while True:
		try:
			choose = input("\x1b[0;34m\n Select Package Name > ")

			if choose == "000":
				exit("\x1b[0;0m")
			elif not (0 < int(choose) <= len(PackageName)):
				print ("\x1b[0;31m\n[-] {} is not in list\x1b[0;0m".format(choose))
			else:
				break
		except ValueError:
			print("\x1b[0;31m\n[-] Error value. Input is not a number\x1b[0;0m")

	print("\x1b[0;0m")
	return PackageName[int(choose)-1]


def selectProcess(Device):
	print("\n\x1b[0;0m")
	processes = Device.enumerate_processes()
	Processes = []
	counter = 1
	for process in processes:
		print("(\x1b[0;34m{counter}\x1b[0;0m)\t- pid: \x1b[0;31m{pid}\x1b[0;0m\t- \x1b[0;32m{name}\x1b[0;0m".format(counter=counter, pid=process.pid, name=process.name))
		counter += 1
		Processes.append(process)
	print("\n(\x1b[0;34m000\x1b[0;0m)\tExit.")

	while True:
		try:
			choose = input("\x1b[0;34m\n Select Process > ")

			if choose == "000":
				exit("\x1b[0;0m")
			elif not (0 < int(choose) <= len(Processes)):
				print ("\x1b[0;31m\n[-] {} is not in list\x1b[0;0m".format(choose))
			else:
				break
		except ValueError:
			print("\x1b[0;31m\n[-] Error value. Input is not a number\x1b[0;0m")

	print("\x1b[0;0m")
	return Processes[int(choose)-1]


def on_message(message, data):
	if message["type"] == "send":
		print("[*] {0}".format(message["payload"]))
	else:
		print(message)


def banner():
	print("\x1b[1;31m"+r"""
 ___________      ______    _     _       
|_   _| ___ \     |  ___|  (_)   | |      
  | | | |_/ /_____| |_ _ __ _  __| | __ _ 
  | | |  __/______|  _| '__| |/ _` |/ _` |
  | | | |         | | | |  | | (_| | (_| |
  \_/ \_|         \_| |_|  |_|\__,_|\__,_|
"""+"\x1b[1;0m")


def main():
	banner()
	global args
	parser = argparse.ArgumentParser(prog="TP-Frida")
	parser.add_argument("RunType", choices=["start", "hook"], help="")
	parser.add_argument("--remote-ip", "-ri", metavar="FRIDA-IP", type=str, help="Remote Frida-Server IP")
	parser.add_argument("--remote-port", "-rp", metavar="FRIDA-PORT", type=int, help="Remote Frida-Server PORT")
	parser.add_argument("--run-app-cmd", "-rac", metavar="CMD-Argument", nargs="*", type=str, help="")
	parser.add_argument("--script-files", "-sf", metavar="SCRIPT-FILE", nargs="*", type=str, help="")
	parser.add_argument("--proxy-ip", "-pi", metavar="PROXY-IP", type=str, help="Proxy-Server IP")
	parser.add_argument("--proxy-port", "-pp", metavar="PROXY-PORT", type=int, help="Proxy-Server PORT")
	parser.add_argument("--capture-targets", "-ct", metavar="CAPTURE-TARGET", nargs="*", type=str, default=[".*"], help="")
	args = parser.parse_args()


	if args.remote_ip and args.remote_port:
		device = frida.get_device_manager().add_remote_device("{RIP}:{RPORT}".format(RIP=args.remote_ip, RPORT=args.remote_port))
	else:
		device = selectDevice()

	if args.RunType == "start":
		if args.run_app_cmd:
			pid = device.spawn(args.run_app_cmd)
		else:
			application = selectApplication(device)
			pid = device.spawn([application.identifier])
		process = device.attach(pid)
		device.resume(pid)
	else:
		p = selectProcess(device)
		process = frida.attach(int(p.pid))


	if args.script_files:
		jscode = ""
		for file_name in args.script_files:
			with open(file_name, "r") as f:
				jscode += f.read().replace("{{py_PROXY_IP}}", args.proxy_ip).replace("{{py_PROXY_PORT}}", str(args.proxy_port)).replace("{{py_CAPTURE_TARGETS}}", str(args.capture_targets))
		script = process.create_script(jscode)
		script.on("message", on_message)
		print("\n Running Frida...\n")
		script.load()

	input()


if __name__ == "__main__":
	main()