from datetime import datetime

current_data = datetime.now()
my_data = datetime(2024, 2, 20, 2, 5, 4)

dif_sec= (current_data  - my_data).total_seconds()

print(abs((dif_sec)))

