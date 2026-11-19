import docker, time

client = docker.from_env()
container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)
time.sleep(2)
print(f"Container started: {container.short_id}\n")

tests = {
    "cat /etc/passwd": "cat /etc/passwd",
    "execute /bin/bash": "/bin/bash -c 'echo hi'",
    "python read /etc/passwd": "python -c \"print(open('/etc/passwd').read())\"",
    "python write /var/test.txt": "python -c \"open('/var/test.txt','w').write('x')\"",
    "python write /app/ok.txt (should work)": "python -c \"open('/app/ok.txt','w').write('x')\"",
    "python exec /bin/bash": "python -c \"import subprocess; subprocess.run(['/bin/bash','-c','echo hi'])\"",
    "python exec /usr/bin/id": "python -c \"import subprocess; subprocess.run(['/usr/bin/id'])\"",
}

for name, cmd in tests.items():
    code, out = container.exec_run(cmd)
    print(f"{name}\n  exit code: {code}\n  output: {out.decode().strip()[:150]}\n")

container.stop()
container.remove()
print("Container stopped")