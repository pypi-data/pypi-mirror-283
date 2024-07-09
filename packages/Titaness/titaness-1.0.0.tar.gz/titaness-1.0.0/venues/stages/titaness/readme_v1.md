

## certificate

Bravo!  You have received a Medical Diploma in "titaness" from      
the Orbital Convergence University International Air and Water   
Embassy of the Tangerine Planet 🍊.  

You are now officially certified to include "titaness" in your   
practice.    

---

# titaness

---
 
[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/EGXocrWNVJE6QWAifHn6r3/XP6tKC6Z4p7cTe8uyzgEjb/tree/performance.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/EGXocrWNVJE6QWAifHn6r3/XP6tKC6Z4p7cTe8uyzgEjb/tree/performance)

---


## 🥧 description
This module can monitor the health status of a python3 `.py` biome. 

---

## ⛲ licensing
`GNU General Public License v3.0 - GNU Project - Free Software Foundation (FSF)`

The complete license is included in the module  
in the "./__license/options" directory.
 		
---		
		
## ⛑️ install

This utilizes:     
[https://pypi.org/project/xonsh](https://pypi.org/project/xonsh)   

```
[xonsh] pip install titaness
```

 ---	
	
## ⚕️ internal status monitor of the module

To monitor the internal status of the "titaness" module:

```
[xonsh] titaness internal-status
```
	
These checks are run with pypi "body_scan";   
"titaness" is built from a fork of "body_scan".  

The "body_scan" checks are written with "unittest". 
   
---
	
## 📖 documentation   
```
[xonsh] titaness help 
```

This opens a server process that can be opened in a browser. 
	
---

## 🌌 Tutorial

### The structure
```
📁 performance
	📜 status_1.py
```

### The checks
```		
# status_1.py

def check_1 ():
	print ("check 1")
	
def check_2 ():
	print ("check 2")
	
def check_3 ():
	raise Exception ("not 110%")

checks = {
	"check 1": check_1,
	"check 2": check_2,
	"check 3": check_3
}
```
		
### The procedure
From the `performance` directory,   
```
[xonsh] titaness status
```

#### The report
This is the report that is (hopefully) written to the terminal.  

```
paths: [
	{
		"path": "status_1.py",
		"empty": false,
		"parsed": true,
		"stats": {
			"passes": 2,
			"alarms": 1
		},
		"checks": [
			{
				"check": "check 1",
				"passed": true,
				"elapsed": [
					4.054199962411076e-05,
					"seconds"
				]
			},
			{
				"check": "check 2",
				"passed": true,
				"elapsed": [
					1.72930003827787e-05,
					"seconds"
				]
			},
			{
				"check": "check 3",
				"passed": false,
				"exception": "Exception('not 110%')",
				"exception trace": [
					"Traceback (most recent call last):",
					"  File \"/titaness/processes/scan/process/keg/check.py\", line 68, in start",
					"    checks [ check ] ()",
					"  File \"<string>\", line 13, in check_3",
					"Exception: not 110%"
				]
			}
		]
	}
]
alarms: [
	{
		"path": "status_1.py",
		"checks": [
			{
				"check": "check 3",
				"passed": false,
				"exception": "Exception('not 110%')",
				"exception trace": [
					"Traceback (most recent call last):",
					"  File \"/titaness/processes/scan/process/keg/check.py\", line 68, in start",
					"    checks [ check ] ()",
					"  File \"<string>\", line 13, in check_3",
					"Exception: not 110%"
				]
			}
		]
	}
]
stats: {
	"alarms": 0,
	"empty": 0,
	"checks": {
		"passes": 2,
		"alarms": 1
	}
}
```
	
### Notes
- Checks are started simultaneously, unless `--simultaneous no`
	- `[xonsh] titaness status --simultaneous no`

- The fractory glob pattern is "**/status_*.py", but can be changed with `--glob-string`  
    - `[xonsh] titaness status --glob-string "**/performance_*.py"`  	
	
---

## 🐍 Advanced Tutorial   

It's recommended to run titaness in a .py script.    

An example of this can be found in the "_book/advanced tutorial"  
section of the documentation.   

---

```
from titaness.topics.show.variable import show_variable
show_variable ({}, mode = "pprint")
show_variable ({}, mode = "condensed")
```

---

## 📡 Contacts
Bryan@Status600.com
	
# 🌑 🌘 🌗 🌖 🌕 🌔 🌓 🌒 🌑 
# 🌑 🌒 🌓 🌔 🌕 🌖 🌗 🌘 🌑 
# 🌑 🌘 🌗 🌖 🌕 🌔 🌓 🌒 🌑 
		
	
