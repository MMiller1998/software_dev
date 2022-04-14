XVISUALIZE=xvisualize

define SCRIPT
#!/bin/bash

source_dir=$$(dirname "$$(readlink -f "$$0")")
source $$source_dir/../Other/venv/bin/activate

exec xvisualize "$$@"
endef

export SCRIPT
$(XVISUALIZE): ../Other/venv/bin/xvisualize
	echo "$$SCRIPT" > $@
	chmod 755 $@

../Other/venv/bin/xvisualize: ../Other
	$(MAKE) -C $<

clean:
	$(RM) $(XMAP)
	$(MAKE) -C ../Other clean

.PHONY: clean
