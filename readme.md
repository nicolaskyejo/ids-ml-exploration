# Network Setup (VMs)

Boxes are set up into
- Attacker
- Defender
- Target (Vulnerable server setup with [Damn Vulnerable Web Application](https://github.com/digininja/DVWA))
  All boxes have Kali linux; _DVWA_ is installed using existing [scripts](https://gitlab.com/kalilinux/packages/dvwa/-/tree/kali/master/dvwa) in Kali linux packages

Note that the attacker in this scenario is in the same network just to make implementation easier

## Commands
- Bring up machines
`vagrant up`
- Connect to machine using your shell
`vagrant ssh {box_name}`
- Stop machines running
`vagrant halt`
- Remove all machines
`vagrant destroy`
- Manually start _DVWA_
`vagrant ssh vulnerable-target` and `sudo dvwa-start`

## Credentials
- All boxes have default user _vagrant_ and pass _vagrant_

# Python Environment Setup
- Requires Python 3.10+
- Install [poetry](https://python-poetry.org/docs/#installation)
- Install dependencies (same directory as 'pyproject.toml') `poetry install` or with dev dependencies `poetry install --dev`

- Alternatively, install dependencies via a `requirements` file
  - `python -m venv venv` 
  - `source venv/bin/activate`
  - `pip install -r requirements.txt`

# Thanks to the following software projects
- [Vagrant](https://www.vagrantup.com/)
- [Damn Vulnerable Web Application](https://github.com/digininja/DVWA)
- [scikit-learn](https://scikit-learn.org/stable/)
- [cicflowmeter](https://gitlab.com/hieulw/cicflowmeter) which is a Python version of [CICFlowMeter](https://www.unb.ca/cic/research/applications.html#CICFlowMeter)
- Numpy and Pandas
