SHELL := bash

all: trainNets

trainNets:
	find perks/netconfig -type f -name '*.json'  -printf 'python3 perks/perkstyle.py %p\n' -exec python3 -m perks.perkstyle {} \; | tee make.log

generateNetConfigs:
	cd perks; \
	python3 genPerkStyleConfigs.py;\
	python3 genPerkConfigs.py;
