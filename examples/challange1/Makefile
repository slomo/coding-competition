BINDIR = $(PWD)/bin

all: build

build:
	echo "Nothing to build"

build-participant:
	cd src; $(MAKE); $(MAKE) install TARGET=$(BINDIR)

correctness-challange:
	priv/hello_check.sh $(INPUT) $(OUTPUT)

correctness-participant:
	bin/hello < $(INPUT) >> $(OUTPUT)
