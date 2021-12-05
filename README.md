# Direction and Magnitude - Warehouse Navigation System

## Setup
 - Move the warehouse data file into the same folder as “main.exe”
 - Make a new folder called “inputs” and move the warehouse data file into the new folder
    - Your directory should look like this:
```bash
inputs/
├─ qvBox-warehouse-data-f20-v01_1041763401.txt
├─ qvBox-warehouse-data-test.txt
├─ qvBox-warehouse-orders-list-part01.txt
main.exe
```
If the warehouse file is not named like the file above, rename it to match “qvBox-warehouse-data-f20-v01_1041763401.txt”

## Usage

Double click `main.exe` to start the program.

To run the raw code, use python 3.8 or above and run `python main.py`

## Building from source

Install PyInstaller using the command - pip install pyinstaller

Using pyinstaller, run the command - pyinstaller --onefile [filename] to create an executable file. This command will output two new directories DIST and BUILD and a .spec file with the same name as the filename. Inside the DIST directory, you will find the executable named [filename].exe

## Milestones

- [x] Basic UI
- [x] Reading and parsing warehouse file
- [x] Find any item
- [x] Basic pathfinding 
- [x] Print path
- [x] Start pathfinding from any open space
