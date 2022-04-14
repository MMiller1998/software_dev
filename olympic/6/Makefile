XSTRATEGY=xstrategy

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xstrategy "$$@"
endef

export SCRIPT
$(XSTRATEGY): ../Other/venv/bin/xstrategy
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xstrategy: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XSTRATEGY)
	$(MAKE) -C ../Other clean

.PHONY: clean
