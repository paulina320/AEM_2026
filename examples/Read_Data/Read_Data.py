import time
import csv
import serial

PORT = "COM8"
BAUDRATE = 115200 # is actually completely ignored as we use CDC over USB OTF FS
TIMEOUT = 0.2
CSV_FILE = "serial_output.csv"


def main() -> None:
	total_bytes = 0
	total_lines = 0
	bytes_window = 0
	lines_window = 0
	window_start = time.time()
	pending_line = b""

	with open(CSV_FILE, "a", newline="", encoding="utf-8") as csv_file, serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT) as ser:
		writer = csv.writer(csv_file)
		print(f"Reading continuously from {PORT} baud. Press Ctrl+C to stop.")
		while True:
			chunk = ser.read(ser.in_waiting or 1)
			if chunk:
				total_bytes += len(chunk)
				bytes_window += len(chunk)

				lines_in_chunk = chunk.count(b"\n")
				total_lines += lines_in_chunk
				lines_window += lines_in_chunk

				pending_line += chunk
				parts = pending_line.split(b"\n")
				pending_line = parts.pop()
				for raw_line in parts:
					writer.writerow([raw_line.rstrip(b"\r").decode("utf-8", errors="replace")])
				csv_file.flush()
				
			now = time.time()
			elapsed = now - window_start
			if elapsed >= 1.0:
				bps = bytes_window / elapsed
				lps = lines_window / elapsed
				print(
					f"\n[speed] {bps:.1f} B/s | {lps:.1f} lines/s | total: {total_bytes} B, {total_lines} lines"
				)
				window_start = now
				bytes_window = 0
				lines_window = 0


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nStopped.")
