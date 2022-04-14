XMAP=xmap

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xmap "$$@"
endef

export SCRIPT
$(XMAP): ../Other/venv/bin/xmap
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xmap: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XMAP)
	$(MAKE) -C ../Other clean

.PHONY: clean
