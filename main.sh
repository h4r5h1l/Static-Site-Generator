python3 -m src.main

# Check if port 8888 is available (exit if in use)
python3 - <<'PY'
import socket,sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(("0.0.0.0", 8888))
    s.close()
    sys.exit(0)
except OSError:
    print("Port 8888 is already in use. Stop the process using it or change the port.")
    sys.exit(1)
PY
if [ $? -ne 0 ]; then
  exit 1
fi

cd public && python3 -m http.server 8888