
all: 3/xmap 4/xvisualize 5/xlegal 6/xstrategy 8/xref 9/xmanager 10/xserver

3/xmap:
	make -C $(@D)

4/xvisualize:
	make -C $(@D)

5/xlegal:
	make -C $(@D)

6/xstrategy:
	make -C $(@D)

8/xref:
	make -C $(@D)

9/xmanager:
	make -C $(@D)

10/xserver:
	make -C $(@D)

clean:
	make -C 3/ clean
	make -C 4/ clean
	make -C 5/ clean
	make -C 6/ clean
	make -C 8/ clean
	make -C 9/ clean
	make -C 10/ clean

.PHONY: clean all
