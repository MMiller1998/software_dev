XREF=xref

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xref "$$@"
endef

export SCRIPT
$(XREF): ../Other/venv/bin/xref
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xref: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XREF)
	$(MAKE) -C ../Other clean

.PHONY: clean
