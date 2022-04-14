XLEGAL=xlegal

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xlegal "$$@"
endef

export SCRIPT
$(XLEGAL): ../Other/venv/bin/xlegal
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xlegal: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XLEGAL)
	$(MAKE) -C ../Other clean

.PHONY: clean
