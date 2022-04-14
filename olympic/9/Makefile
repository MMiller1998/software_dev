XMANAGER=xmanager

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xmanager "$$@"
endef

export SCRIPT
$(XMANAGER): ../Other/venv/bin/xmanager
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xmanager: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XMANAGER)
	$(MAKE) -C ../Other clean

.PHONY: clean
