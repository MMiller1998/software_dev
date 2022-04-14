XSERVER=xserver

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xserver "$$@"
endef

export SCRIPT
$(XSERVER): ../Other/venv/bin/xserver
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xserver: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XSERVER)
	$(MAKE) -C ../Other clean

.PHONY: clean
